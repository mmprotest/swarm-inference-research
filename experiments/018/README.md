# Experiment 018: Wavefront swarm execution

**Research question:** Does concurrency across independent resident resources change the system-level critical path more than further local kernel optimization?

**Verdict:** `PASS_STRONG`

The complete coarse wavefront plus immutable AttnRes cache reached 6.7022 tok/s/user in a validated independent-resource model, 2.16× over the corresponding serial schedule, with 83.8% pipeline efficiency. This was not a physical 12-GPU run.

## Audit paths

- [Full technical report](REPORT.md)
- [`evidence/summary.json`](evidence/summary.json)
- [`evidence/failure-log.json`](evidence/failure-log.json)
- [`evidence/charts/`](evidence/charts/)

The root [claim ledger](../../docs/CLAIMS.md) states exactly which claims from this experiment are admissible and which are not.
