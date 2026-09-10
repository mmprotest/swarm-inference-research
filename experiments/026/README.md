# Experiment 026: Physical Qwen3.8-27B over a three-machine WAN

**Research question:** Did the integrated architecture make Qwen3.8-27B Q4_K_M practical on one local GPU plus two heterogeneous rented GPUs connected over genuine WAN links?

**Verdict:** `WAN_SWARM_NOT_VIABLE_UNDER_TESTED_CONDITIONS`

Experiment 026 is the first physical heterogeneous multi-machine WAN result in this public series. The model did execute across all three machines, short target-only runs matched the local greedy stream, exact disk-warm shard verification was 103.19x faster than the same fully uncached shard acquisition, and a controlled stage-process kill recovered in 9.508 seconds without prompt replay or token loss/duplication.

The integrated serving gates failed. The best exact development run reached 1.615 committed tokens/s against an 8 tokens/s gate. The sealed run reached 0.590 tokens/s, first diverged from the local greedy stream at zero-based token 178, and ended on a transport reset after 282 of 512 requested tokens. Native MTP was rejected after diverging on four of six development prompts. The measured bottleneck was serial response wait across the WAN, not remote GPU compute or the 20 KiB decode-boundary activation.

## Audit paths

- [Full technical report](REPORT.md)
- [`evidence/summary.json`](evidence/summary.json)
- [`evidence/final-receipt.json`](evidence/final-receipt.json)
- [`evidence/metrics.jsonl`](evidence/metrics.jsonl), containing 71 physical run/prompt records
- [`evidence/validation/final-evidence.source.json`](evidence/validation/final-evidence.source.json), containing the source bundle's 19/19 validation result
- [`evidence/remote-collected-final-002/`](evidence/remote-collected-final-002/), containing the complete 31-file final remote collection and its receipt
- [`evidence/source-manifest.json`](evidence/source-manifest.json), documenting public curation and source/public hashes

Machine-local paths and one email-shaped identity string were replaced in the public report and canonical data. Numerical fields, verdicts, prompt/model hashes, and measured results were not changed. The original 831-file artifact bundle is indexed by path, byte size, and SHA-256 in [`provenance/experiment-026-source-files.csv`](../../provenance/experiment-026-source-files.csv).

The root [claim ledger](../../docs/CLAIMS.md) distinguishes the successful primitives from the failed integrated serving claim.
