# Experiment 020: Full Pre-Spend Swarm Readiness

**Outcome: E021_NOT_READY**

Experiment 020 rented zero GPUs and mutated zero Vast resources. It freezes a 96-worker P8/depth-8 placement, but corrected simulator validation and the end-to-end production deployment path are not complete. The audit found six high-impact issues that can and must be solved without rental: required layer/span replays were summed rather than physically executed; the rendered controller-host-agent role is absent; bounded worker processes do not yet dispatch real shard tasks; the provisioning state machine has no guarded real Vast backend adapter; pod cache acquisition is not integrated into the host agent; and preflight cannot validate a supplied pinned registry image. The live marketplace snapshot is also incomplete: only 0 of 12 required homogeneous RTX 3090 P8 hosts were available. The E021 path remains fail-closed and spends $0.

| Question | Answer |
|---|---|
| Any GPU rented in E020? | NO |
| Any Vast resource mutated? | NO |
| Vast CLI authenticated? | YES |
| Live offers queried? | YES |
| Final worker count | 96 |
| Final pod count | 12 |
| Workers per pod | 8 |
| Max worker peak GiB | 16.979 |
| Whole layer on any worker? | NO |
| Whole expert on any worker? | NO |
| Full checkpoint covered? | YES |
| Full 93-layer sharded correctness? | PASS |
| Corrected simulator validation? | FAIL |
| sm86 build ready? | YES |
| Linux deployment ready? | NO |
| Model distribution ready? | NO |
| 96-worker dry run passed? | YES |
| Vast fleet currently feasible? | NO |
| E021 projected cost | $158.95 expected; $632.06 conservative |
| Remaining pre-rental-testable critical risks | 6 |
| E021 readiness | NOT READY |

## Decision and evidence hierarchy

The readiness decision is based on exact checkpoint placement, a complete 93-layer sharded oracle, an audit that rejected the incomplete single-resource replay method, event accounting, post-fusion physical shard services, real control-plane/transport dry runs, a locally built SM86 Linux image, real ranged model acquisition, a guarded read-only Vast snapshot, and injected rollback failures. Every throughput value in this report is **PREDICTED, NOT PHYSICALLY PROVEN**. RTX 3090 performance and the distributed critical path remain E021 measurements only after the pre-rental blockers close.

The old Experiment 019 value of 20.8836 tok/s remains **PROVISIONAL / UNVALIDATED**. E019 retains `MODEL_INVALID` under its preregistered gate. E020 does not rewrite that history.

## Methodological correction to E019

The invalid question was whether serial execution of a sharded implementation approximately equals a different optimized monolithic implementation. E020 instead asks: does the event model reproduce the physically executed sharded algorithm; are measured sharding costs present; does explicit resource scheduling create the correct critical path; and how sensitive is the result to hardware/network assumptions that cannot be tested without independent GPUs?

Two short-sample replay attempts failed (median errors 7.07% and 8.35%) with opposite span drift. The hypothesis was measurement instability. The redesign increased expert samples to 31 iterations and non-expert sampling to 15 complete repeats, kept calibration and held-out captures independent, and added no normalization. Primitive service stability then met the numeric targets: median 4.47%, p90 4.61%, maximum 6.78%. However, audit showed that full-layer and 2/4/8-layer "actual" walls were arithmetic sums of held-out calls, not one physically executed ordered shard workload. This is methodologically insufficient under the E020 definition, so corrected simulator validation is **FAIL**, irrespective of the low numeric errors.

| Workload | Predicted ms | Held-out ms | Error |
|---|---|---|---|
| expert_stripe | 0.1605 | 0.1606 | 0.06% |
| KDA_stripe | 0.2824 | 0.2794 | 1.07% |
| MLA_stripe | 0.1980 | 0.2124 | 6.78% |
| projection_stripe | 0.0468 | 0.0488 | 4.10% |
| shared_expert_stripe | 0.1056 | 0.1072 | 1.49% |
| complete_sharded_KDA_layer | 8.1669 | 7.8070 | 4.61% |
| complete_sharded_MLA_layer | 7.5114 | 7.1958 | 4.39% |
| two_layer_span | 16.3338 | 15.6140 | 4.61% |
| four_layer_span | 32.0121 | 30.6168 | 4.56% |
| eight_layer_span | 64.0730 | 61.2631 | 4.59% |

The accounting suite checked 9 block/chunk configurations. In every case the sum of worker event durations exactly reconciled with measured bottom-up compute work; network duration reconciled with latency, serialization, and protocol overhead; and collectives, state waits, queue waits, and launch-overhead policy remained explicit. Status: PASS.

## Placement decision

| Candidate | Workers | Pods | Peak GiB | Predicted tok/s | Utilization | Selected |
|---|---|---|---|---|---|---|
| P8/depth-2 | 376 | 47 | 4.775 | 25.34 | 4.3% | NO |
| P8/depth-4 | 192 | 24 | 9.014 | 22.53 | 7.6% | NO |
| P8/depth-8 | 96 | 12 | 16.979 | 16.86 | 11.3% | YES |
| P16/depth-4 | 384 | 24 | 4.565 | 19.01 | 5.8% | NO |
| P16/depth-8 | 192 | 12 | 8.806 | 14.11 | 8.6% | NO |

P8/depth-2 is fastest in the model but requires 376 GPUs. P8/depth-4 still requires 192. P16 candidates increase local pod width to a marketplace-hostile 16 GPUs. P8/depth-8 retains large modeled headroom with 96 GPUs and a directly searchable 12 x 8 topology; it is therefore the frozen economic/deployment choice, not the raw simulated-throughput winner.

The exact manifest covers 1,560,860,324,864 checkpoint payload bytes across 497,220 tensors with zero gap, zero overlap, and zero unintended weight replication. It emits 96 worker manifests across 12 pods. All 873 worker/source-file identity pairs carry authoritative SHA-256 values with zero placeholder hashes. Maximum peak is 16.979 GiB, maximum routed/shared expert fraction is 12.5%, and no worker owns a whole layer, routed expert, or shared expert.

## Complete sharded correctness

The frozen placement executed all 93 layers through worker-owned shard paths on the RTX 5090, including endpoint sharding, exact routes, KDA/MLA/AttnRes state, and grouped experts. It performed 3,983 explicit worker operations. Maximum relative L2 was 1.194e-06; greedy token 220 matched the canonical oracle; ownership failures were 0. Status: PASS.

## Grouped top-16 expert stripe

| P | Rows | Old launches | New launches | Old ceiling ms | New ceiling ms | Rel. L2 | Status |
|---|---|---|---|---|---|---|---|
| 8 | 1 | 17 | 2 | 0.4084 | 0.1803 | 4.21e-08 | PASS |
| 8 | 2 | 34 | 2 | 0.8203 | 0.3007 | 8.79e-08 | PASS |
| 8 | 4 | 68 | 2 | 1.6323 | 0.5419 | 8.69e-08 | PASS |
| 16 | 1 | 17 | 2 | 0.6281 | 0.1170 | 3.90e-08 | PASS |
| 16 | 2 | 34 | 2 | 1.2221 | 0.1871 | 8.65e-08 | PASS |
| 16 | 4 | 68 | 2 | 2.1308 | 0.3424 | 8.42e-08 | PASS |

The retained implementation maps 16 logical fragments to at most 2 expert launches per worker for a minimum 8x launch coalescing at one row, accumulates route weights locally, emits one partial latent vector, and remains numerically exact under the existing gate. All changed worker services were re-profiled with real K3 weights and fixtures.

## Bottom-up predicted performance

| Block | Chunk | Predicted pass ms | Predicted tok/s/user | Worker util. |
|---|---|---|---|---|
| 7 | 1 | 688.7 | 11.62 | 7.8% |
| 7 | 2 | 603.7 | 13.25 | 5.9% |
| 7 | 4 | 630.0 | 12.70 | 4.3% |
| 12 | 1 | 866.3 | 15.01 | 10.1% |
| 12 | 2 | 719.7 | 18.06 | 8.7% |
| 12 | 4 | 718.9 | 18.08 | 7.6% |
| 16 | 1 | 1008.3 | 16.86 | 11.3% |
| 16 | 2 | 798.4 | 21.29 | 10.1% |
| 16 | 4 | 766.5 | 22.18 | 8.9% |

| Scenario | Compute | Local link | Inter-pod link | Predicted tok/s |
|---|---|---|---|---|
| optimistic | 0.9x | 0.05 ms / 100.0 Gbps | 1.0 ms / 25.0 Gbps | 36.02 |
| nominal | 1.0x | 0.25 ms / 25.0 Gbps | 5.0 ms / 10.0 Gbps | 15.31 |
| conservative | 1.3x | 1.0 ms / 10.0 Gbps | 10.0 ms / 2.0 Gbps | 5.04 |

At block 16/chunk 1 the PREDICTED range is 5.04-36.02 tok/s/user, nominal 15.31. The +20% all-compute sensitivity remains above 5 tok/s. Because the corrected physical replay gate failed its methodology audit, these projections are **UNVALIDATED DIAGNOSTICS** and cannot justify spend yet. Work-inflation remains an economic metric and is not used as a validity gate.

## Concurrency and stragglers

| Requests | Per-user tok/s | Aggregate tok/s | Utilization | Queue p50 ms |
|---|---|---|---|---|
| 1 | 16.86 | 16.86 | 11.3% | 0.0 |
| 2 | 13.70 | 21.09 | 14.2% | 301.9 |
| 4 | 9.11 | 24.12 | 16.2% | 905.6 |
| 8 | 5.50 | 25.98 | 17.4% | 2113.1 |
| 16 | 3.08 | 27.03 | 18.1% | 4528.0 |

| Scenario | Affected workers | Predicted tok/s | Critical-path amplification |
|---|---|---|---|
| homogeneous | 0 | 16.86 | 1.000x |
| 10_percent_workers_25_percent_slower | 10 | 16.11 | 1.046x |
| 10_percent_workers_50_percent_slower | 10 | 15.39 | 1.096x |
| one_slow_worker_per_pod | 12 | 14.71 | 1.146x |
| network_jitter_20_percent | 0 | 16.74 | 1.007x |
| one_degraded_pod | 8 | 15.72 | 1.072x |

Concurrency is a secondary economic analysis. It does not replace the single-user physical gate. Straggler scenarios quantify critical-path amplification so E021 can interpret a weak result without changing the acceptance criterion.

## Speculative overhead

| Scenario | Mean output/cycle | Draft ms | Target ms | Predicted real tok/s | >=5? |
|---|---|---|---|---|---|
| conservative_scenario | 2.00 | 200.4 | 688.7 | 2.25 | NO |
| public_reference_scenario | 3.83 | 200.4 | 688.7 | 4.31 | NO |
| optimistic_scenario | 5.50 | 200.4 | 688.7 | 6.18 | YES |

Experiment 015 did not produce a swarm-valid acceptance distribution (measurement count 0); the public block-7 mean of 3.85 is only a scenario input. The exact E021 secondary measurement is frozen: real accepted-length histograms on preregistered coding, math, chat, and creative workloads for blocks 7/12/16 plus draft, rollback, and commit latency. Target-only remains primary, so this evidence gap does not conceal or replace the 5 tok/s architecture gate.

## Runtime, protocol, and security

The real TLS/framed lightweight controller dry run registered and exercised 96 workers in 12 pods. Stress runs passed at 376 and 1000 workers; the harness does not hardcode 96. The protocol uses persistent TLS connections, per-run HMAC credentials, binary framing, bounded buffers/backpressure, IDs, timeouts, checksums, and propagated errors. Security validation: PASS. This validates the control plane and wire format, not the missing production controller entrypoint or native shard-task dispatch.

## Linux/SM86 deployment and model distribution

The clean multi-stage CUDA 13.0.1 / Python 3.12 image built and passed health, native-library load, bundled-manifest, and eight-worker lifecycle tests. All three currently required Linux native libraries contain SM86 code and have recorded SHA-256 hashes; SM120 development binaries remain available. Runtime secrets are injected, never baked into the image or repository. Nevertheless the deployment gate is **FAIL**: lifecycle-only workers are not a production K3 data plane, the controller role rendered in the Vast command does not exist, pod acquisition is not wired into the host lifecycle, the real provisioning adapter is absent, and preflight cannot accept/verify a pinned registry digest.

Model acquisition used the authoritative `moonshotai/Kimi-K3` source. A real 64 KiB pair of HTTP range requests resumed correctly, returned HTTP 206, hash-matched immutable local bytes, and did not redownload the checkpoint. Pod bundles transfer 1,574,645,266,048 bytes fleet-wide, including 13,709,174,600 intentional bytes, with a largest pod disk requirement of 126.637 GiB. No worker or pod downloads a full checkpoint by design. Acquisition status: PASS.

## Provisional topology thresholds

- Intra-pod: RTT <= 1.000 ms and bandwidth >= 5.000 Gbps at that RTT.
- Inter-pod: RTT <= 10.000 ms and bandwidth >= 1.000 Gbps at that RTT.
- Jitter <= 10% in the preregistered gate model.

These numeric thresholds are diagnostic and **INVALID_PENDING_PHYSICAL_SINGLE_RESOURCE_REPLAY**. They must be re-derived and frozen before E021. Once valid, they are evaluated from live probes after deployment; Vast bandwidth metadata is never accepted as physical proof.

## Vast marketplace snapshot and cost

Snapshot at 2026-08-13T09:27:17.905348+00:00:

| GPU class | P8 hosts | Suitable GPUs | Host price min/median/max | Locations |
|---|---|---|---|---|
| RTX 3090 | 0 | 0 | None / None / None |  |
| RTX 3090 Ti | 0 | 0 | None / None / None |  |
| RTX A5000 | 0 | 0 | None / None / None |  |
| RTX A6000 | 0 | 0 | None / None / None |  |
| RTX 4090 | 16 | 128 | 2.3499074074074078 / 3.3089814814814806 / 4.803703703703704 | Alberta, CA, California, US, Croatia, HR, Minnesota, US, Romania, RO, Taiwan, TW, United Kingdom, GB, Utah, US, Virginia, US, Washington, US |

Primary RTX 3090 availability is NO: 0 complete P8 hosts versus 12 required. Those matching hosts were a snapshot, not reserved capacity. Offer IDs are ephemeral. E021 preflight requires a fresh complete homogeneous plan; unrelated single-GPU hosts are treated as WAN and are not substitutes.

Estimated cost is $158.95 expected, $632.06 conservative, and an unapproved suggested worst-case budget cap of $900.00. These include startup, model download, bootstrap, topology qualification, warmup, benchmark, artifact collection, failure allowance, disk, and exposed transfer costs. Rate basis: no matching host: explicit midpoint-of-policy scenario assumption; when no primary host matches, this is a policy-scenario budget rather than a live purchasable fleet quote. Actual E020 charge: $0.

The hard arming conjunction requires `SWARM_ALLOW_RENTAL=EXPERIMENT_021`, `--apply`, exact `experiment-021`, an approved plan digest, and a positive maximum-dollar budget. E020 additionally has a compile-time read-only lock. All create/launch/stop/destroy guard tests mock the subprocess boundary.

## Provisioning and rollback

The exact state machine passed a nominal 12-pod run and 11 injected failures: disappearing offer, pod provision failure, never-ready instance, wrong GPU count, insufficient disk, bootstrap failure, download failure, hash mismatch, slow network, worker health failure, and controller crash. Every case preserved a valid hash-chained ledger, included every conceptual rental in teardown, protected unrelated IDs, and ended without an orphan. The cost kill switch passed mock-time/rate tests.

## Risk register

| Risk | Probability | Impact | Tested? | Result / mitigation |
|---|---|---|---|---|
| actual RTX 3090 SM86 shard throughput | medium | high | NO | requires E021; measure worker services before headline run; abort if conservative gate fails |
| actual local eight-GPU collective latency | medium | high | NO | requires physical P8 host; measure all required intra-pod paths before READY |
| actual inter-host transport and jitter | medium | high | NO | requires independent hosts; topology gate rejects slow fleet before benchmark |
| actual Vast host behavior and throttling | medium | high | NO | requires rental; health, power, and sustained service qualification |
| full distributed critical path and cost/token | medium | high | NO | requires full swarm; E021 primary measurement and kill switch |
| 12 homogeneous P8 RTX 3090 hosts available simultaneously | high | high | YES | NO: 0 of 12 in snapshot; refresh snapshot; spend $0 unless all 12 satisfy policy |
| checkpoint byte placement or worker memory error | low | high | YES | PASS byte-exact coverage and 16.979 GiB peak; revalidate hashes and manifest on every pod |
| single-resource replay does not physically execute the ordered shard workload | high | high | YES | FAIL: numeric service sums pass thresholds but the required end-to-end physical wall was not measured; run resident-weight RTX 5090 replays for every primitive, full KDA/MLA layer, and 2/4/8-layer spans; then revalidate without normalization |
| remote shard acquisition, resume, or hash failure | low | high | YES | PASS real 64 KiB ranged/resumed proof and cache tests; content-addressed retry then clean abort |
| control-plane transport/security scaling | low | high | YES | PASS TLS/HMAC/bounds plus 96/376/1000 lightweight workers; retain the frozen framing, credentials, and bounds in the production data path |
| provisioning rollback leaves rentals | low | high | YES | PASS 11 injected failures and hash-chained ledger; ledger-only teardown plus verify-destroyed |
| production controller host-agent role missing | high | high | YES | FAIL: deployment audit found no controller-host-agent entrypoint; implement and loopback-test controller enrollment, registration, scheduling, and shutdown |
| production worker process has no native shard dispatch | high | high | YES | FAIL: lifecycle worker does not handle EXECUTE_SHARD; wire the frozen protocol to all native primitives and rerun full 93-layer correctness through worker processes |
| real Vast provisioning backend adapter missing | high | high | YES | FAIL: state machine currently has only a fake backend; implement the guarded real adapter and test every command with mocked subprocess boundaries while E020 stays read-only |
| host agent does not acquire and verify its pod model bundle | high | high | YES | FAIL: ShardCache and lifecycle are not integrated; make cache completion a prerequisite for registration and prove shared concurrent access |
| production DSpark acceptance distribution | medium | medium | YES | SCENARIO_ONLY_ACCEPTANCE_UNVALIDATED; run exact preregistered E021 secondary acceptance measurement after target-only pass |
| immutable registry image cannot be supplied and verified by preflight | high | high | YES | FAIL: local image build=PASS, preflight published flag is hardcoded false; add verified --image-ref input, then publish the corrected image by digest |
| no Vast SSH key registered | high | low | YES | detected by redacted CLI receipt; onstart bootstrap is noninteractive; add emergency key before E021 if policy requires |

No high-impact risk remains with `can_test_without_rental=true` and `tested=false`, but six such risks were tested and **failed**. They are pre-rental implementation blockers, not physical unknowns. Once closed, the legitimate rental-only unknowns are actual SM86 throughput, physical collectives/transport, Vast host behavior, the full distributed critical path, and physical cost/token.

## Readiness gates

| Gate | Requirement | Status |
|---|---|---|
| 1 | Final bounded-worker placement frozen | PASS |
| 2 | Entire checkpoint byte-exactly assigned | PASS |
| 3 | Peak worker memory <=20 GiB | PASS |
| 4 | No whole layer/expert | PASS |
| 5 | Complete 93-layer shard correctness | PASS |
| 6 | Corrected single-resource simulator validation | FAIL |
| 7 | Event accounting reconciliation | PASS |
| 8 | Grouped expert execution | PASS |
| 9 | All required SM86 binaries | PASS |
| 10 | Deployable Linux worker/controller environment | FAIL |
| 11 | Model acquisition mechanism | PASS |
| 12 | 96-worker controller dry-run | PASS |
| 13 | Vast CLI auth/read-only integration | PASS |
| 14 | Vast rental safety guard | PASS |
| 15 | Fleet plan or explicit availability condition | PASS |
| 16 | Full cost estimate | PASS |
| 17 | Mock provisioning and rollback | PASS |
| 18 | Network/topology gates preregistered | FAIL |
| 19 | E021 runbook complete | PASS |
| 20 | No high-impact pre-rental-testable risk untested | PASS |

The placement and prediction evidence are strong, but `E021_NOT_READY` means another bounded pre-rental validation/deployment pass is required before E021. No rental is authorized. After the six blockers close, the live preflight must still remain `NO_GO` until 12 compliant hosts and an explicitly approved budget exist.

## EXPERIMENT 021 READINESS VERDICT

E021_NOT_READY

> Have we done everything reasonably possible without paying for independent GPUs, such that the next experiment should be the full physical Kimi K3 swarm rather than another preparatory architecture experiment?

NO

Exact remaining pre-rental work: physically execute the exact ordered single-resource shard workload on RTX 5090 for every required primitive/layer/span and rerun the replay error gates; implement and loopback-test the controller-host-agent entrypoint rendered for pod 0; wire authenticated EXECUTE_SHARD frames to the real KDA/MLA/expert/projection/endpoint worker primitives and rerun the 93-layer graph through worker processes; implement the real Vast backend adapter for the already-tested provisioning state machine, keep it E020-disabled, and test every call at the mocked subprocess boundary; integrate the proven pod-bundle/ShardCache acquisition and hash verification into SwarmHostAgent before worker registration; make preflight accept and verify a user-supplied immutable registry image digest instead of hardcoding published=false; rebuild and publish the corrected image by immutable digest; rerun the complete zero-rental preflight and require 12 policy-compliant P8 hosts before any budget approval
