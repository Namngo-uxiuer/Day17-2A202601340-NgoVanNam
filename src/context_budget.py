from __future__ import annotations

from dataclasses import dataclass

from .utils import estimate_tokens


@dataclass(frozen=True)
class LayerBudget:
    short_term: float = 0.10
    long_term: float = 0.04
    episodic: float = 0.03
    semantic: float = 0.03


class ContextBudgetManager:
    """Trim memory context using the 10/4/3/3 teaching budget from the slide."""

    priority = ("short_term", "long_term", "episodic", "semantic")

    def __init__(self, total_context_tokens: int = 8000, budget: LayerBudget | None = None):
        self.total_context_tokens = total_context_tokens
        self.budget = budget or LayerBudget()

    def layer_limit(self, layer: str) -> int:
        return max(1, int(self.total_context_tokens * getattr(self.budget, layer)))

    def trim(self, text: str, max_tokens: int) -> str:
        if estimate_tokens(text) <= max_tokens:
            return text
        # Graph context begins with a useful summary but frequently appends the
        # newest facts at the tail.  Preserve both ends so recency updates do
        # not disappear when applying a bounded per-layer budget.
        max_chars = max_tokens * 4
        marker = "\n[...trimmed...]\n"
        available = max(1, max_chars - len(marker))
        # The summary at the head is usually the strongest relevance signal;
        # keep most of it, while retaining a tail slice for recent facts.
        head_chars = (available * 3) // 4
        tail_chars = available - head_chars
        return text[:head_chars] + marker + text[-tail_chars:]

    def assemble(self, layers: dict[str, str]) -> tuple[str, dict[str, dict[str, int]]]:
        rendered: list[str] = []
        breakdown: dict[str, dict[str, int]] = {}
        for layer in self.priority:
            raw = layers.get(layer, "") or ""
            limit = self.layer_limit(layer)
            trimmed = self.trim(raw, limit)
            breakdown[layer] = {
                "limit_tokens": limit,
                "raw_tokens": estimate_tokens(raw),
                "used_tokens": estimate_tokens(trimmed),
            }
            if trimmed.strip():
                rendered.append(f"<{layer.upper()}>\n{trimmed}\n</{layer.upper()}>")
        return "\n\n".join(rendered), breakdown
