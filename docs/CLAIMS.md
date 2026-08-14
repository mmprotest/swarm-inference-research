# Claim ledger

This file is the shortest path for a skeptical reviewer. Every public claim is classified as **admissible**, **diagnostic**, or **not proved**.

| ID | Claim | Status | Primary evidence |
|---|---|---|---|
| C016-1 | Verification-major + exact DCP improved the E015 oracle from 2.1838 to 2.6691 tok/s/user. | **Admissible within the E016 bridge model** | `experiments/016/evidence/summary.json`, `results/arm-results.csv` |
| C017-1 | The best retained exact block-16 path reached 3.0994 tok/s/user and did not reach 5. | **Admissible within the E017 experiment model** | `experiments/017/evidence/summary.json`, `results/exact-combined.csv` |
| C018-1 | Coarse wavefront + AttnRes cache reached 6.7022 tok/s/user, 2.16× versus corresponding serial, 83.8% pipeline efficiency. | **Admissible as validated independent-resource model** | `experiments/018/evidence/summary.json`, physical service CSVs, report |
| C018-2 | E018 is a physical 12-GPU or multi-machine result. | **Not proved** | Explicitly denied by E018 evidence class |
| C019-1 | The K3 checkpoint census covers 497,220 tensors / 1,560,860,324,864 payload bytes. | **Admissible** | E019 report, checkpoint/correctness receipts |
| C019-2 | An 8 GiB-cap sub-layer placement used 376 worker units with maximum accounted peak 4.4946 GiB and no whole layer/expert ownership. | **Admissible structural/capacity result** | E019 summary/report and placement receipts |
| C019-3 | The full 93-layer shard-only traversal passed with max relative L2 1.2708e-6, exact routes and greedy-token match. | **Admissible physical sequential correctness result** | `full-93-sharded-receipt.public.json` |
| C019-4 | The E019 system achieves 20.8836 tok/s/user. | **Invalid / diagnostic only** | Serial reconstruction missed by 103.9%; experiment verdict `MODEL_INVALID` |
| C020-1 | A 96-worker / 12-pod P8/depth-8 deployment candidate was frozen and rehearsed without renting GPUs. | **Admissible readiness result** | E020 summary, readiness, runtime receipts |
| C020-2 | The E020 nominal 15.31 tok/s projection is validated throughput. | **Invalid / diagnostic only** | Projection validation status `FAIL` |
| C021-1 | Ordered replay invalidated the timing model at 95.54% median error. | **Admissible falsification result** | E021 summary, ordered replay validation |
| C022-1 | The rebuilt ordered-DAG model achieved 2.7136% median, 3.7441% p90, 4.0017% max held-out error without normalization. | **Admissible model-validation result** | E022 `run-result.json`, `validation/model-validation.json` |
| C022-2 | In 27 frozen inventories, diagnostic adaptive placement unlocked 6 inventories that whole-layer placement could not place. | **Diagnostic until remaining gates pass** | E022 `analysis/capacity-unlocks.csv`, truth table |
| C022-3 | Adaptive sub-layer placement improved throughput when whole-layer placement was feasible. | **No, diagnostic result was 0% uplift** | E022 `analysis/throughput-uplift.csv` |
| C022-4 | E022 proves sub-layer planner value. | **Not proved** | Native-primitives and representative-full-93 gates failed; final verdict `MODEL_INVALID` |

## Rule for public use

If a claim's evidence class says **model**, say model. If a network is shaped, say shaped. If a gate failed, do not promote the diagnostic value into a result. If the experiment was single-device sequential correctness, do not describe it as a distributed physical run.
