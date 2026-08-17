# Lab 17 Submission

Trong practice set, long-term la layer quan trong nhat: no giai quyet E02, E03,
E08, E09 va dong gop cho E07; dac biet E08 cho thay preference moi cua
BLUEBIRD-42 (TypeScript/NestJS) duoc uu tien theo scope va recency. Context
Block cua Zep giam cong tu van hanh: ingestion, graph, provenance va recall da
duoc managed. Redis + Qdrant cho phep tu chon schema, latency va hosting, doi
lai can tu xay ingestion, embedding, ranking, conflict handling va xoa data.

Guardrail chong memory poisoning: chi ingest user da opt-in; redact PII truoc
khi ingest; luu provenance/source/timestamp; tach namespace theo `user_id`; va
khong de heartbeat tu them instruction hay quyen moi vao durable memory. Fact
mau thuan phai giu lich su de audit va uu tien fact moi hon trong dung scope.

Benchmark student dat 11/11 (100%); vi vay khong co layer nao thap hon layer
khac. E03 retrieve nhieu nhat, 1,320 token, do Context Block kem facts can
giu open-loop `benchmark report` va deadline 16:00. E07 can long-term (Python)
va semantic (`Idempotency-Key`); thieu mot trong hai thi huong dan khong con
ca nhan hoa hoac khong dung quy tac payment. Token reduction trung binh cua
student la 14.2%; no-memory giam context cao hon vi retrieve rong, nhung chi
dat 2/11, nen reduction khong thay the evidence hit rate.

E08 dung recency theo scope: Python van cho ORCHID-27, con BLUEBIRD-42 bat
buoc TypeScript/NestJS. E10 compact transcript thanh summary, durable notes va
recent turns, nhung giu `REVIEW-DEADLINE-1600`, Friday 16:00; buffer tuyen tinh
se ton context va lam giam chat luong recall.
