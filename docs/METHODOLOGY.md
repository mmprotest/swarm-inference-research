# Methodology and evidence discipline

## Experimental loop

The sequence follows a falsifiable loop: define the hypothesis and thresholds, implement the mechanism, run the benchmark, inspect the result, invalidate unsupported assumptions, and redesign only after the evidence is recorded.

Experiments 016–022 deliberately preserve failed gates. E019 retained a numerically attractive 20.8836 tok/s scheduler output but classified the model invalid. E021 then showed why: ordered physical shard replay disagreed with the event model by roughly 95.5% at the median. E022 rebuilt the resident service model and replay accounting, then passed its declared held-out timing gate without a global normalization multiplier.

## Physical versus modeled evidence

Physical measurements use real Kimi K3 checkpoint tensors and local CUDA execution on an RTX 5090. Model-based experiments combine these service curves with explicit resource scheduling and network assumptions. A shaped link is never treated as a measured remote link.

## Correctness

Sub-layer claims require numerical agreement with monolithic/reference execution, exact route agreement where applicable, checkpoint-byte accounting, and explicit worker ownership. A planner is not allowed to claim sub-layer placement while silently falling back to monolithic layer mathematics.

## Performance models

A scheduler model must be validated against an ordered physical replay of the same execution semantics. Post-hoc global multipliers are disallowed for the E022 gate. Component variability is reported separately from ordered-DAG prediction error.

## Frozen heterogeneous suite

E022 generated and froze 27 inventories before whole-layer versus adaptive comparison: 3 coarse-friendly controls and 6 each from memory-fragmented, compute-heterogeneous, network-heterogeneous, and full-mixed families. The suite hash is recorded in E022's `summary.json` and `run-result.json`. Whole and adaptive planners share the optimizer, objective, budgets, event engine, and seeds; only the allowed action set changes.

## Why failures are part of the dataset

A failed experiment is evidence about the hypothesis. E016/E017 identify a local-optimization ceiling. E019 establishes capacity/correctness while invalidating throughput. E021 invalidates a performance model. E022 repairs the timing model but still refuses the planner-value headline because two separate correctness/native-execution gates remain open.

This is intentional. The repository is designed to let a reviewer distinguish what happened from what the project hoped would happen.
