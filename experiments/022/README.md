# Experiment 022: Adaptive granularity under frozen heterogeneity

**Research question:** Given exactly the same heterogeneous resources, does selective sub-layer placement materially improve the best system over whole-layer placement?

**Verdict:** `MODEL_INVALID`

The timing model was repaired to 2.71% median / 3.74% p90 / 4.00% maximum error with no global multiplier. Across 27 frozen inventories, diagnostics showed 6 capacity unlocks and zero throughput uplift when whole-layer placement was feasible. Native-primitives and representative full-93 gates still failed, so no final planner-value claim is admitted.

## Audit paths

- [Full technical report](REPORT.md)
- [`evidence/summary.json`](evidence/summary.json)
- [`evidence/failure-log.json`](evidence/failure-log.json)
- [`evidence/charts/`](evidence/charts/)

The root [claim ledger](../../docs/CLAIMS.md) states exactly which claims from this experiment are admissible and which are not.
