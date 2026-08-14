# Experiment 021: Physical timing-model falsification

**Research question:** Does the event model predict ordered execution of the actual shard path?

**Verdict:** `MODEL_INVALID`

No. Median timing-model error was 95.54%, with p90 and maximum near 100%. The performance claims built on that model were invalidated.

## Audit paths

- [Full technical report](REPORT.md)
- [`evidence/summary.json`](evidence/summary.json)
- [`evidence/failure-log.json`](evidence/failure-log.json)
- [`evidence/charts/`](evidence/charts/)

The root [claim ledger](../../docs/CLAIMS.md) states exactly which claims from this experiment are admissible and which are not.
