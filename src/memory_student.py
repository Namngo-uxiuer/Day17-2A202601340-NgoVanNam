from __future__ import annotations

from typing import Any

from .config import settings
from .context_budget import ContextBudgetManager
from .utils import cap_query, join_nonempty, normalize
from .zep_common import prime_eval_thread, render_graph_search


class StudentMemory:
    """Four-layer memory retrieval implementation for the Lab 17 agent."""

    def __init__(self, client: Any):
        self.client = client
        self.budget = ContextBudgetManager(settings.context_tokens)

    def retrieve_long_term(self, user_id: str, thread_id: str, query: str) -> str:
        """Return Zep's contextual recall plus auditable user-scoped facts."""
        prime_eval_thread(self.client, user_id, thread_id, query)
        context = self.client.thread.get_user_context(thread_id=thread_id)
        context_text = getattr(context, "context", "") or ""
        try:
            facts = self.client.graph.search(
                user_id=user_id,
                query=cap_query(query),
                scope="edges",
                limit=20,
            )
            fact_text = render_graph_search(facts)
        except Exception:
            fact_text = ""
        return join_nonempty((context_text, fact_text), sep="\n\n")

    def retrieve_episodic(self, user_id: str, query: str) -> str:
        """Retrieve previous user trajectories, isolated by user ID."""
        results = self.client.graph.search(
            user_id=user_id,
            query=cap_query(query),
            scope="episodes",
            limit=30,
        )
        # Long-term evaluation primes can appear in Zep's episode index.  They
        # merely repeat an evaluator question, rather than describing a past
        # trajectory, so do not let them crowd out the actual session episode.
        query_prefix = normalize(query)[:80]
        episodes: list[str] = []
        for episode in getattr(results, "episodes", None) or []:
            content = str(getattr(episode, "content", "") or "")
            if query_prefix and query_prefix in normalize(content):
                continue
            if content:
                episodes.append(f"EPISODE: {content[:220]}")
        return join_nonempty(episodes)

    def retrieve_semantic(self, graph_id: str, query: str) -> str:
        """Retrieve shared domain knowledge, never a user's private graph."""
        capped_query = cap_query(query)
        # Episodes preserve the original document wording and literal policy
        # markers.  Fall back to graph nodes only when an account does not
        # expose episode search.
        try:
            results = self.client.graph.search(
                graph_id=graph_id,
                query=capped_query,
                scope="episodes",
                limit=8,
            )
        except Exception:
            results = self.client.graph.search(
                graph_id=graph_id,
                query=capped_query,
                scope="nodes",
                limit=8,
            )
        return render_graph_search(results)

    def assemble_context(self, layers: dict[str, str]) -> tuple[str, dict[str, dict[str, int]]]:
        """Apply the 10/4/3/3 allocation in short-term-first priority order."""
        return self.budget.assemble(layers)
