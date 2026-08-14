# Experiment 016: Verification-major batching

**Research question:** Could exact batching, grouped expert work, triangular MLA and DCP break the E015 verifier ceiling?

**Verdict:** `FAIL`

The strongest retained path reached 2.6691 tok/s/user, 1.222× over the E015 oracle. Local block scaling was useful, but the whole-verifier 5 tok/s target remained unreachable.

## Audit paths

- [Full technical report](REPORT.md)
- [`evidence/summary.json`](evidence/summary.json)
- [`evidence/failure-log.json`](evidence/failure-log.json)
- [`evidence/charts/`](evidence/charts/)

The root [claim ledger](../../docs/CLAIMS.md) states exactly which claims from this experiment are admissible and which are not.
