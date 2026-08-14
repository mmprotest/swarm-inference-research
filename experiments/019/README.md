# Experiment 019: Fine-grained capacity decomposition

**Research question:** Can the complete Kimi K3 graph be expressed without any worker owning a whole layer or expert, under consumer-scale memory caps?

**Verdict:** `MODEL_INVALID`

Capacity/correctness succeeded: the 8 GiB-cap candidate used 376 worker placement units with a 4.495 GiB maximum peak and passed a full 93-layer shard traversal. The 20.8836 tok/s timing output was invalid because serial reconstruction missed by 103.9%.

## Audit paths

- [Full technical report](REPORT.md)
- [`evidence/summary.json`](evidence/summary.json)
- [`evidence/failure-log.json`](evidence/failure-log.json)
- [`evidence/charts/`](evidence/charts/)

The root [claim ledger](../../docs/CLAIMS.md) states exactly which claims from this experiment are admissible and which are not.
