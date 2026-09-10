# E026: Qwen3.8-27B Q4 WAN Swarm Integrated Proof

## 1. Canonical verdict

`WAN_SWARM_NOT_VIABLE_UNDER_TESTED_CONDITIONS`

## 2. Executive result

No. E026 did not prove practical WAN swarm inference for Qwen3.8-27B Q4_K_M under the tested architecture.

The target model did execute physically across three heterogeneous machines on genuine, unshaped WAN links. Short development runs produced the same greedy token stream as the local reference, exact shard caching exceeded the startup gate, and an intentional production-stage kill recovered in 9.508 seconds without replaying the prompt or losing or duplicating a token. Those are useful primitive-level results.

The integrated gates nevertheless failed. The fastest exact WAN target run reached 1.615 committed tokens/s, below both the 5 tokens/s lower interpretation boundary and the 8 tokens/s interactive gate. Native MTP reached 2.667 committed tokens per target verification and 1.732 tokens/s on one WAN prompt, but it diverged from target-only greedy decoding on four of six development prompts and was rejected. The sealed target-only run reached only 0.590 tokens/s, first differed from the sealed local greedy stream at zero-based token 178, and ended on a transport reset after 282 of the required 512 tokens. A valid negative run is not `INFRASTRUCTURE_INVALID` merely because transport reliability was poor.

All decision claims below are `PHYSICAL`. The canonical dataset contains 71 run/prompt records and passed 19 of 19 final evidence checks. No shaped-network or projected throughput result is used for the verdict.

## 3. Best configuration

The sealed configuration prioritized correctness and transport longevity over the fastest development result:

| Order | Physical node | Hardware | Coarse region | Contiguous ownership |
|---:|---|---|---|---|
| 0 | Vast 50478198 | RTX 3080 Ti 12 GB; Ryzen 5 3500; 15,912 MiB RAM | Japan | layers 0-8; 2,424,279,168 cached tensor bytes |
| 1 | Vast 50478207 | RTX 3060 12 GB; Xeon E5-2680 v4; 64,284 MiB RAM | South Korea | layers 9-16; 2,150,593,792 cached tensor bytes |
| 2 | local coordinator | RTX 5090 32 GB; Core Ultra 7 265K; 97,749 MiB RAM | user-local; Australia/Sydney timezone, not independently geolocated | embedding, layers 17-63, output |

No single machine executed the complete distributed target path. Application RTT was 290.064 ms from local to worker A, 355.119 ms from local to worker B, and 65.172 ms from A to B. Measured throughput was 6.469/15.263 Mbit/s local-to-A/A-to-local, 2.898/9.432 Mbit/s local-to-B/B-to-local, and 17.228/120.908 Mbit/s A-to-B/B-to-A.

The frozen runtime used contiguous layer splitting, `tensor-split=1,1,6`, exact content-addressed shard validation, pipelined cache validation, ordered asynchronous cross-worker copies, persistent connections, a Vast-managed A-to-B SSH proxy, greedy decoding, no speculation, no activation compression, flash attention, context size 12,288, batch and micro-batch 512, and `--ctx-checkpoints 0`. Direct A-to-B routing was faster in development but its SSH path repeatedly expired after roughly four minutes, so the managed proxy was frozen before the sealed prompt was opened.

The exact coordinator invocation was:

```text
"<local-repo>\.runtime\experiment-026\build\bin\llama-server.exe" -m "<local-repo>\.runtime\experiment-026\models\Qwen3.8-27B-Q4_K_M.gguf" --host 127.0.0.1 --port 42626 -ngl 99 -c 12288 -b 512 -ub 512 -np 1 -fa on --fit off --metrics --spec-type none --no-webui --ctx-checkpoints 0 --rpc 127.0.0.1:42646 --split-mode layer --tensor-split 1,1,6
```

Each remote stage ran `ggml-rpc-server -H 127.0.0.1 -p 50101 -d CUDA0 -c`; the router exposed A and the tunneled B endpoint to the local RPC frontend. Instrumentation set `E026_TRACE=1` and `GGML_RPC_NO_RDMA=1`.

Model provenance was [ggml-org/Qwen3.8-27B-GGUF](https://huggingface.co/ggml-org/Qwen3.8-27B-GGUF), revision `0669b98607d47046c7c2b3f801011d54a08cfccf`, file `Qwen3.8-27B-Q4_K_M.gguf`, 18,973,870,432 bytes, SHA256 `31629f53165ab6a7dad8c9847dcfd1fdf55829dac1e6e748f4a68581b0033d34`. The runtime was llama.cpp tag `b10886`, commit `f1b6fbf35cfa010b0a8d6301fdfccbb7f41bd903`, with instrumentation diff SHA256 `eed261160912740fb76dc325cc48c2b89cdce136ec915fb615a758312a94c539`.

The local Release build used MSVC 14.44, CUDA 13.0.88, driver 591.86, Ninja, `GGML_CUDA=ON`, `GGML_RPC=ON`, `CMAKE_CUDA_ARCHITECTURES=120`, tests/examples off, and OpenSSL off. Remote Release builds used GCC 13.3.0, CUDA 13.0.88, drivers 595.84 and 580.159.03, Ninja, compute architecture `86-real`, RPC/CUDA on, server/tests/examples and OpenSSL off. The sealed configuration hash is `cdc4ddbfb54c0e7dd07e21b0c51a5abae352a5e5bf5f0edb9020b9b733047b7c`.

## 4. Performance table

Decode rate is committed output tokens divided by the measured decode interval. TTFT includes prompt processing. TPOT is the inter-arrival time between committed tokens; speculative rows emit bursts, so their near-zero median TPOT is not representative and committed tokens/s is the comparison metric. One expensive target traversal is one verification pass through all target stages; it crosses two physical WAN stage boundaries in this topology.

| Physical run | Output | TTFT (s) | Decode tok/s | Median / p95 TPOT (s) | Tokens / target traversal | Correctness and validity |
|---|---:|---:|---:|---:|---:|---|
| Local sealed target | 512 | 0.086 | 61.777 | 0.016 / 0.017 | 1.000 | sealed local reference |
| Ordinary WAN target control | 64 | 76.221 | 0.974 | 0.972 / 1.311 | 1.000 | exact 64-token stream |
| Best target-only WAN, direct peer | 32 | 13.593 | 1.615 | 0.494 / 0.774 | 1.000 | exact 32-token stream; 1.658x control |
| Target-only WAN, managed proxy | 32 | 20.244 | 0.593 | 1.577 / 1.779 | 1.000 | exact 32-token stream |
| Native MTP K=3, direct peer | 64 | 12.171 | 1.732 | 0.001 / 1.578 | 2.667 | exact on this prompt only; method rejected by corpus |
| Native MTP K=3, managed proxy | 64 | 17.016 | 0.768 | 0.002 / 3.254 | 2.667 | exact on this prompt only; 1.295x matched proxy target |
| Native MTP K=8, managed proxy | 64 | 16.904 | 0.519 | 0.001 / 11.915 | 3.048 | exact on this prompt only; slower than target-only proxy |
| Warm-replica control, no kill | 64 | 23.707 | 0.460 | 2.231 / 2.374 | 1.000 | exact 64-token stream |
| Warm replica, stage killed | 64 | 22.375 | 0.448 | 2.226 / 2.375 | 1.000 | exact; recovery passed |
| Sealed WAN target, managed proxy | 282 / 512 | 23.060 | 0.590 | 1.565 / 2.113 | 1.000 | strict mismatch at 178; transport reset |

The trusted local corpus covered six categories and contexts from 54 to 7,974 tokens, with 256 generated tokens per prompt. Its decode range was 62.087-64.552 tokens/s and TTFT range was 0.155-2.923 seconds. The separate sealed 512-token local control sustained 61.777 tokens/s. Local full-model GPU residency increased VRAM use by 19,021 MiB, from 1,463 to 20,484 MiB.

## 5. Bottleneck decomposition

Synchronization wait, not remote computation or activation payload volume, dominated the critical path.

| Configuration | Median token cycle (ms) | Summed response wait (ms) | Cycle residual (ms) | Wait fraction |
|---|---:|---:|---:|---:|
| Ordinary WAN | 972.124 | 949.065 | 23.059 | 97.63% |
| Best direct target | 494.816 | 471.287 | 23.530 | 95.24% |
| Sealed managed-proxy target | 1,565.021 | 1,538.817 | 26.204 | 98.33% |

For the sealed run, worker A's 285 measured stage operations took a median 3.588 ms and worker B's took 7.189 ms. Their combined 10.777 ms is less than 1% of the 1,565 ms median token cycle. Time-aligned mean GPU utilization was 0.566% on A and 0.812% on B; maximum observed memory was 2,956 and 2,643 MiB. The system spent almost all wall time waiting on serial RPC/transport synchronization while the GPUs were idle.

The wait sums can overlap and therefore are diagnostic rather than an exact additive accounting. The residual combines local compute, serialization, orchestration, and unobserved transport work. That limitation does not change the ordering: the observed remote kernel time and residual are both tiny relative to response wait.

## 6. Synchronization result

The ordinary and sealed target-only paths committed 1.000 token per expensive target traversal: 1.000 target traversal/token and 2.000 physical WAN boundary traversals/token.

Native MTP K=3 made 70 proposals, accepted 38 (54.29%), and used 24 verification traversals for 64 committed tokens. That is 1.583 accepted draft tokens per verification, 2.667 committed tokens/target traversal, 0.375 target traversals/token, and 0.750 physical WAN boundary traversals/token. It improved the managed-proxy route by 1.295x, but improved the faster direct route by only 1.073x.

K=8 made 152 proposals, accepted 41 (26.97%), and used 21 verifications: 1.952 accepted draft tokens/verification, 3.048 committed tokens/target traversal, 0.328 target traversals/token, and 0.656 WAN boundary traversals/token. Despite meeting the mechanical 2.5 tokens/traversal target, it reached only 0.519 tokens/s, 12.5% below the matched target-only proxy. Verification waste and long tail stalls erased the traversal reduction.

Synchronization compression was therefore demonstrated only as a development mechanism, not as an exact retained result. The sealed policy used no speculation and returned to 1.000 committed token/traversal.

## 7. Compression result

Activation compression was not implemented because profiling falsified its priority. A decode boundary activation was 20,480 bytes. At the measured 17.228 Mbit/s A-to-B rate, raw payload time was approximately 9.5 ms, less than 2% of the 494.8 ms direct median cycle; even at the slower 6.469 Mbit/s local-to-A rate it was about 25.3 ms, roughly 5%. Q8 or Q4 activation transfer could not plausibly close the gap from 1.615 to 8 tokens/s while serial response waits consumed 95-98% of each cycle.

The sealed run measured 46,464 coordinator-link protocol bytes/token plus 43,728 peer-link bytes/token, or 90,192 steady RPC protocol bytes/committed token across both WAN boundaries. Including startup traffic, it moved 87,445,136 protocol bytes before failure, or 310,089 bytes per completed token. These counts exclude TCP/IP and SSH framing.

Lossless state compression also failed its wall-clock test. Zlib level 1 reduced a 683,866,044-byte hybrid state to 639,048,953 bytes, only 6.55%, while compression took 15.715 seconds and decompression 2.595 seconds. It was reverted. No lossy activation or state codec is included in the result.

## 8. Cold-start result

Exact, shard-local caching worked materially.

| Startup condition | Time (s) | Network bytes | Interpretation |
|---|---:|---:|---|
| Worker A initial shard acquisition | 36.692 | 2,396,815,360 | initial selected tensors |
| Worker B initial shard acquisition | 54.983 | 2,123,857,920 | initial selected tensors |
| A exact-cache metadata/tensor upgrade | 20.773 | 27,463,808 | completed exact 120-tensor cache |
| B exact-cache metadata/tensor upgrade | 19.757 | 26,735,872 | completed exact 106-tensor cache |
| Standby A shard, fully uncached | 432.571 | 2,424,279,168 | same exact shard later used for warm comparison |
| Standby A shard, disk-warm verification | 4.192 | 0 | 103.19x faster; strict cache gate passed |
| Best complete disk-warm server readiness | 63.320 | cached | process start, exact cache drain, GPU load, registration |
| Sealed disk-warm server readiness | 83.801 | cached | frozen managed-proxy deployment |
| GPU-warm relay registration | 5.133 | state resident | routing readiness only |

Full cold topology setup remained operationally poor: create request to stage launch took 1,386.531 seconds for A and 1,916.960 seconds for B. The critical-node ratio to the best disk-warm full-server start was 30.27x, but this is not the primary cache ratio because the cold interval includes provider provisioning and compilation while the warm interval does not. The like-for-like same-shard 432.571-to-4.192-second result is the defensible 103.19x cache measurement.

## 9. Churn result

Warm state-local failover passed its controlled development test. The standby synchronously mirrored every RPC command and buffer mutation, including attention state and Gated DeltaNet recurrent state. Worker A's production `ggml-rpc-server` process was killed without worker-side warning after output token 20.

The kill command took 3.716 seconds. Failure was detected 1.897 seconds after the kill signal completed, or 5.615 seconds after injection began. The gap between the last pre-failure token and first resumed token was 9.508 seconds; token 21 was the first resumed token, at derived wall time `2026-09-10T12:38:30.297085+00:00`. Reassignment, explicit restore, and tail replay were each 0 seconds because the replica was already current. All 64 tokens matched the no-kill control hash `cc8c89ca599f8dea96f311c0eee5590c607fbfc1e76b47a66b06af43bd7e5527`; duplicate tokens, lost tokens, and prompt replay were all zero. Throughput changed from 0.460 to 0.448 tokens/s, a 2.55% reduction in the kill run.

The two mirrored RPC streams recorded cumulative sends of 30.03 and 30.91 MB and receives of 1.68 and 2.48 MB, including setup; those totals demonstrate physical mirroring but are not an isolated incremental steady-state estimate. Separately, llama.cpp's sequence-state API saved the complete 8,038-position hybrid state as 683,866,044 bytes: 526,971,680 attention-state bytes plus 156,894,364 recurrent-state/header bytes. In-memory serialization took 0.063 seconds, GPU restore 0.066 seconds, disk-inclusive save/restore 0.545/0.604 seconds, and process restart to first resumed token 8.856 seconds with an exact 128-token continuation and zero prompt replay.

No point-in-time checkpoint file was transferred over the WAN in the retained strategy; continuous synchronous mirroring avoided a failover-time transfer. Consequently, a physical standalone checkpoint-transfer latency is unavailable and is not claimed.

Only 2 of 27 compared boundary tensors were byte-identical across heterogeneous kernels, yet the recovery token stream was exact. Boundary byte equality was therefore not used as the correctness criterion.

## 10. Correctness

The local target was frozen first. Six 256-token development prompts covered factual continuation, code, reasoning, long-context retrieval, repetitive structured text, and natural-language generation at short, approximately 2K, and approximately 8K contexts. A separate sealed prompt generated 512 local tokens with greedy decoding.

Short distributed target runs passed token identity: the ordinary WAN control matched all 64 tokens, and the best direct and managed-proxy target runs matched all 32 tested tokens. The controlled recovery run also matched its 64-token target reference exactly.

The sealed lane failed strict distributed correctness. It matched the local stream for 178 tokens and selected a different token at zero-based position 178. On the 179 identical-history positions, top-1 agreement was 178/179 = 99.441%; mean top-10 Jaccard was 97.461%; mean absolute common-top-10 log-probability delta was 0.04499 and the maximum was 0.28501. At the mismatch, local selected ` passes` over ` enters` with a 0.03976 log-probability margin, while WAN selected ` enters` over ` passes` with a 0.01600 margin. This is consistent with heterogeneous numerical ordering flipping a near tie, but the strict greedy gate still fails.

Native MTP was not exact enough to retain. At K=3 it diverged on factual token 160, code token 44, reasoning token 29, and generation token 87; only the structured and retrieval prompts matched. K=1 also failed four of six prompts, and the tested K=8 variants failed three or four of six. A 64-token WAN factual run happened to match, but that single prompt does not override the frozen corpus result.

No approximate or lossy method is described as exact. The final output-token hashes, logit comparison, prompt hash, model hash, and configuration hash are in the canonical proof receipt.

## 11. Cost

The experiment stayed far below budget. Vast credit fell from $45.805124 to $44.886929, an account-level decrease of $0.918195. The conservative ledger upper bound, including rental and reserved network charges, was $1.532202 against the $38 ceiling. Worker A cost $0.173148/hour and worker B $0.063056/hour.

Both instances were destroyed and the final provider snapshot verified that no E026 instances or paid storage remained. The teardown wrapper initially omitted Vast's required `--yes`, which produced a zero-exit “Aborted” response; that post-run bug was fixed, the deletion was repeated through the authenticated provider path, and absence was re-verified. It did not affect inference measurements or the spend limit.

## 12. Negative results

- Native MTP produced high local headline rates but failed exact greedy identity on most development prompts. It was removed from the sealed configuration.

- Increasing MTP depth from K=3 to K=8 raised committed tokens/verification from 2.667 to 3.048 but reduced proxy throughput from 0.768 to 0.519 tokens/s because acceptance fell to 26.97% and stalls grew.

- Direct A-to-B routing produced the best exact development rate, 1.615 tokens/s, but its SSH transport repeatedly expired after roughly four minutes. The managed proxy survived longer but reset during the sealed run after 282 tokens.

- Ordered asynchronous copy and pipelined exact-cache validation improved startup and routing behavior but did not remove the serial per-token RPC dependency.

- Disabling llama.cpp context checkpoints was not numerically neutral on two of six local development prompts relative to the original local reference. The sealed local and WAN controls nevertheless used the same frozen `--ctx-checkpoints 0` setting.

- Zlib state compression saved only 6.55% and cost 18.31 seconds for compression plus decompression. It was reverted.

- Activation compression was deliberately not tested after profiling showed that raw boundary payload time was a small fraction of the critical path. This is a measured deferral, not evidence that every codec would be useless.

- The sealed 512-token request did not complete, did not preserve strict greedy identity, and did not recover from the transport reset. No retry or post-seal tuning was performed.

## 13. Scientific interpretation

The evidence supports three limited claims. First, contiguous Qwen3.8-27B Q4_K_M stages can execute across these three heterogeneous physical machines and produce exact short greedy streams. Second, exact shard-local disk caching can turn repeated shard acquisition into a four-second verification operation. Third, synchronous replication of the complete attention and recurrent state can survive an unannounced stage-process kill within the 20-second recovery target without prompt replay.

The evidence does not support practical WAN serving. The best exact target path was 4.95x below the 8 tokens/s gate, and even the rejected inexact MTP result was 4.62x below it. The sealed route was 13.55x below the gate. Remote compute consumed roughly 11 ms while the median sealed cycle consumed 1,565 ms; adding faster GPUs or reducing a 20 KB activation does not attack that critical path. The architecture exposed llama.cpp RPC-scale serial synchronization and fragile long-lived SSH transport directly to every token.

This is a valid result on one three-machine topology, not a universal impossibility proof. WAN development ablations generally used one prompt/run, lower-layer byte framing was not measured, the local endpoint's geographic location was not independently verified, and the final request ended at 282 tokens. A standalone WAN checkpoint-transfer time and a clean isolated replication-bandwidth delta are also unavailable. These limitations weaken generalization, but none can turn 0.590-1.615 exact tokens/s into an observed interactive result or turn the failed sealed correctness/completion gates into passes.

The canonical dataset passed 19/19 independent lineage, schema, hash, calculation, state, recovery, and correctness checks. Earlier synthesis attempts with malformed inherited run IDs or incomplete byte semantics are retained and explicitly superseded; no raw run evidence was overwritten.

## 14. Next decision

**Continue solving a specific primitive:** build an exact, reconnectable, state-local multi-token verification protocol that removes per-token RPC round trips and survives transport reconnection. Do not proceed to volunteer-runtime engineering until that primitive completes a sealed 512-token three-machine WAN run with identical greedy output and at least 8 committed tokens/s.
