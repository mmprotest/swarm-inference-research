# Limitations

The following boundaries apply to the public claims in this repository.

- **No physical heterogeneous multi-machine Kimi K3 swarm is measured in this repository.**
- E026 is a physical heterogeneous three-machine result for Qwen3.8-27B Q4_K_M, not Kimi K3 and not a general WAN topology sample.
- Most E026 WAN configurations contain one prompt/run. The sealed request ended on a transport reset after 282 of 512 tokens and first differed from the frozen local greedy stream at zero-based token 178.
- E026 protocol-byte counts exclude TCP/IP and SSH framing, and the local endpoint's geographic location was not independently verified.
- E026 recovery covers a controlled stage-process kill with a synchronously warm mirror. It does not establish recovery from machine, provider, coordinator, or network-partition failure.
- E018's 6.7022 tok/s/user result is a validated independent-resource model using physical K3 service and shaped links, not a physical 12-GPU result.
- E019's 20.8836 tok/s/user scheduler output is invalid and deliberately excluded from the headline performance series because the serial reconstruction gate failed by 103.9%.
- E019's full-93 correctness is sequential sub-layer worker execution on one RTX 5090. It proves the shard graph and numerical path, not networked throughput.
- E020 contains pre-spend deployment projections. No GPU was rented and the projection validation gate failed.
- E021 invalidates its own performance model with approximately 95.5% median ordered-replay error.
- E022 repairs timing prediction but its final planner-value verdict remains `MODEL_INVALID` because individual native primitive bindings and representative full-93 placement replay did not pass.
- The Kimi K3 checkpoint is not included. Full physical reproduction requires access to the model and compatible runtime/hardware.
- Shaped RTT/bandwidth models cannot reproduce all real congestion, contention, packet loss, topology, driver, collective, and straggler effects.
- Single-request throughput is not the same as multi-user serving goodput. Experiments 016–022 and 026 do not establish production SLO economics.
- The public evidence bundle is curated for auditability. Large duplicate traces, temp directories, generated placement payloads and repeated inventory copies are omitted. Experiments 016–022 remain indexed in `provenance/source-archive-members.csv`; all 831 supplied E026 artifacts are indexed in `provenance/experiment-026-source-files.csv`.
