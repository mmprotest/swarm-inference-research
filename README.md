# Swarm Inference Lab — Research Evidence

**Experiments 016–022: Kimi K3 inference, wavefront scheduling, fine-grained capacity decomposition, and model falsification.**

This repository is the public evidence package for a sequence of systems experiments asking one question:

> **Under what hardware, topology, and workload conditions should large-model inference use coarse stages, expert-level placement, or sub-layer decomposition?**

The target model is **Kimi K3**: a 93-layer MoE checkpoint with 896 routed experts and roughly 1.56 TB of declared checkpoint payload. The experiments were deliberately designed to distinguish physical measurement, validated modeling, shaped-network assumptions, and invalid diagnostic output.

The most important rule in this repository is simple: **a large number is not a result if its validation gate failed.**

![Research arc](figures/01-research-arc.png)

## Four results worth looking at

### 1. Scheduling changed the system-level result

Experiments 016 and 017 pushed exact local execution from the E015 2.18 tok/s/user oracle to 2.67 and then 3.10 tok/s/user, but still failed the 5 tok/s/user target. Experiment 018 changed the architecture instead of continuing to squeeze the same critical path. A coarse wavefront with immutable AttnRes caching reached **6.702 tok/s/user**, **2.16×** over its corresponding serial schedule, with **83.8% pipeline efficiency**.

That E018 headline is a **validated independent-resource model grounded in physical real-K3 service and shaped network assumptions**. It is not presented as a physical multi-GPU measurement.

### 2. A 1.56 TB checkpoint was decomposed below 4.5 GiB per worker

Experiment 019 constructed a complete K3 placement in which no worker owned a whole ordinary layer, routed expert, or shared expert. The 8 GiB-cap candidate used **376 independent worker placement units** with a maximum accounted peak of **4.495 GiB**. A complete 93-layer shard traversal executed sequentially on one RTX 5090 with **1.27e-6 maximum relative L2 error**, exact routes, and a matching greedy token.

![E019 capacity and correctness](figures/04-e019-capacity-correctness.png)

The scheduler also produced 20.8836 tok/s/user. That number is **not a result**. The timing model failed its serial reconstruction gate by 103.9%, so the experiment was classified `MODEL_INVALID`.

### 3. The bad performance model was caught and repaired

Experiment 021 replayed ordered shard execution and exposed a catastrophic mismatch: **95.54% median timing-model error**. The throughput model was invalidated instead of calibrated into agreement.

Experiment 022 rebuilt the resident service model and deterministic event accounting. On held-out ordered-DAG cases, error fell to **2.71% median, 3.74% p90, and 4.00% maximum**, with `normalization_applied=false` and no global correction multiplier.

![Model validation repair](figures/02-model-validation-repair.png)

### 4. Fine granularity currently looks like a capacity tool, not a speed tool

Experiment 022 froze **27 heterogeneous inventories** before whole-layer versus adaptive evaluation. The diagnostic planner results produced **6 whole-infeasible / adaptive-feasible capacity unlocks**. On the **21 inventories where whole-layer placement was already feasible, adaptive sub-layer placement produced 0% throughput uplift**.

![Capacity unlocks](figures/03-capacity-unlocks.png)

The final E022 verdict remains `MODEL_INVALID` because two required gates failed: individual production-native primitive bindings and representative full-93 placement replay. The capacity results are therefore diagnostic, not a product-performance claim.

## Experiment index

| Experiment | Question | Verdict | Headline |
|---|---|---|---|
| [016](experiments/016/) | Can exact verification-major batching break the verifier ceiling? | `FAIL` | 2.669 tok/s/user; local gains did not translate into enough whole-system speedup. |
| [017](experiments/017/) | Can the KDA-heavy critical path close the remaining gap? | `FAIL` | Best exact result 3.099 tok/s/user; KDA optimization path falsified. |
| [018](experiments/018/) | Does wavefront concurrency change the critical path? | `PASS_STRONG` | 6.702 tok/s/user validated independent-resource model; 83.8% pipeline efficiency. |
| [019](experiments/019/) | Can K3 be decomposed into genuinely sub-layer worker footprints? | `MODEL_INVALID` | 376-worker placement, 4.495 GiB max peak, 93-layer correctness PASS; timing model invalid. |
| [020](experiments/020/) | Is the architecture ready to justify a physical fleet spend? | `NOT_READY` | 96-worker deployment candidate; no GPU rented; projection gate failed. |
| [021](experiments/021/) | Does the scheduler predict ordered physical shard execution? | `MODEL_INVALID` | 95.54% median model error invalidated the performance model. |
| [022](experiments/022/) | Does adaptive sub-layer placement beat a strong whole-layer planner? | `MODEL_INVALID` | Model repaired to 2.71% median error; 6 diagnostic capacity unlocks, 0 throughput uplift where coarse placement fit; two correctness/native gates remain open. |

## Evidence classes

This repo uses evidence labels aggressively because these experiments mix physical execution with models and shaped networks.

| Evidence class | Meaning |
|---|---|
| **Physical local** | Real Kimi K3 weights and CUDA execution were measured on the local RTX 5090. |
| **Validated independent-resource model** | Service inputs are physically measured, resources are modeled as independently resident/executable, and the model passed its declared validation gate. |
| **Shaped network** | RTT/bandwidth behavior is imposed by an explicit model. It is not a physical WAN/LAN measurement. |
| **Diagnostic / model invalid** | The number is preserved for debugging or comparison but is not admitted as a performance result. |
| **Physical heterogeneous swarm** | Multiple independent physical machines execute the distributed graph. **Experiments 016–022 do not reach this evidence class.** |

See [Evidence methodology](docs/METHODOLOGY.md) and the [claim ledger](docs/CLAIMS.md).

## Audit the claims

The public bundle includes the aggregate receipts, calibration tables, validation outputs, correctness receipts, failure logs, charts, and representative raw service evidence needed to inspect the headlines. Very large duplicate traces, generated placement payloads, temporary directories, and repeated inventory copies were intentionally excluded from the Git-friendly package. Every member of the original 3.2 GB expanded experiment archive is still indexed by path, uncompressed size, and ZIP CRC32 in [`provenance/source-archive-members.csv`](provenance/source-archive-members.csv).

Run:

```bash
python scripts/verify_headlines.py
python scripts/verify_checksums.py
```

To regenerate the four root figures:

```bash
python -m pip install -r requirements.txt
python scripts/regenerate_figures.py
```

The Kimi K3 checkpoint is not redistributed. Re-running the physical benchmarks from scratch requires the model, compatible hardware, and the companion runtime source tree from the corresponding experiment revision. This repository is primarily an **audit and research-evidence package**, not a 1.56 TB turnkey reproduction image.

## Repository layout

```text
experiments/016..022/
  README.md             short public summary
  REPORT.md             full technical report
  evidence/             curated raw/aggregate evidence + original charts

data/                   cross-experiment tables
figures/                publication-facing synthesis figures
scripts/                headline/checksum verification and figure regeneration
docs/                   claims, methodology, limitations, sanitization notes
provenance/              source archive hashes and complete member inventory
```

## What is not proved

No experiment in this package physically executes Kimi K3 across a heterogeneous multi-machine swarm. The E018 wavefront result assumes independent resident resources and shaped network links. E019 proves fine-grained capacity decomposition and single-device sequential shard correctness, not distributed throughput. E022 repairs the event model but fails two preregistered gates, so its planner outputs remain diagnostic.

Those limitations are the research frontier, not footnotes. See [LIMITATIONS.md](docs/LIMITATIONS.md).

## License

Apache-2.0. Research artifacts retain the same license as the source project unless a third-party artifact states otherwise.
