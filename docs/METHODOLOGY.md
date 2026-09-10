# Methodology and evidence discipline

## Experimental loop

The sequence follows a falsifiable loop: define the hypothesis and thresholds, implement the mechanism, run the benchmark, inspect the result, invalidate unsupported assumptions, and redesign only after the evidence is recorded.

Experiments 016–022 deliberately preserve failed gates. E019 retained a numerically attractive 20.8836 tok/s scheduler output but classified the model invalid. E021 then showed why: ordered physical shard replay disagreed with the event model by roughly 95.5% at the median. E022 rebuilt the resident service model and replay accounting, then passed its declared held-out timing gate without a global normalization multiplier. E026 froze its topology, model, thresholds, transport, prompt, and correctness policy before the sealed request; its partial 282/512-token run remains valid negative evidence rather than being discarded after the transport reset.

## Physical versus modeled evidence

Experiments 016–022 use real Kimi K3 checkpoint tensors and local CUDA execution on an RTX 5090 for their physical inputs. Model-based experiments combine these service curves with explicit resource scheduling and network assumptions. A shaped link is never treated as a measured remote link. E026 is separately classified as physical heterogeneous execution: Qwen3.8-27B stages ran on three independent machines over measured, unshaped WAN paths.

## Correctness

Sub-layer claims require numerical agreement with monolithic/reference execution, exact route agreement where applicable, checkpoint-byte accounting, and explicit worker ownership. A planner is not allowed to claim sub-layer placement while silently falling back to monolithic layer mathematics.

## Performance models

A scheduler model must be validated against an ordered physical replay of the same execution semantics. Post-hoc global multipliers are disallowed for the E022 gate. Component variability is reported separately from ordered-DAG prediction error.

## Integrated physical WAN gate

E026 separates primitive success from integrated viability. Its frozen gates cover physical machine count, exact distributed correctness, interactive decode, synchronization compression, 512-token sealed completion, cached startup, controlled failure survival, and budget. A run may establish physical distribution, cache, or recovery behavior while the overall serving verdict remains negative. Throughput is computed from committed output tokens; speculative results that fail the frozen exactness corpus are labeled inexact and are not promoted into the sealed configuration.

## Frozen heterogeneous suite

E022 generated and froze 27 inventories before whole-layer versus adaptive comparison: 3 coarse-friendly controls and 6 each from memory-fragmented, compute-heterogeneous, network-heterogeneous, and full-mixed families. The suite hash is recorded in E022's `summary.json` and `run-result.json`. Whole and adaptive planners share the optimizer, objective, budgets, event engine, and seeds; only the allowed action set changes.

## Why failures are part of the dataset

A failed experiment is evidence about the hypothesis. E016/E017 identify a local-optimization ceiling. E019 establishes capacity/correctness while invalidating throughput. E021 invalidates a performance model. E022 repairs the timing model but still refuses the planner-value headline because two separate correctness/native-execution gates remain open. E026 establishes limited physical distribution, caching, and controlled recovery results while rejecting practical WAN serving on the tested topology because throughput, sealed correctness, completion, and transport reliability failed.

This is intentional. The repository is designed to let a reviewer distinguish what happened from what the project hoped would happen.
