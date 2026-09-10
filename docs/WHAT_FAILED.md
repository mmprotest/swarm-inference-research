# What failed, and why it matters

A public research repository should make the failures easier to find than the wins.

## E016: local gains did not clear the system target

Verification-major grouping and exact DCP improved the modeled oracle, but the whole-verifier speedup was only 1.222× against E015 and remained below 5 tok/s/user.

## E017: KDA optimization was not enough

The best exact block-16 result reached 3.099 tok/s/user. Further KDA-focused work could not plausibly close the remaining gap under the retained architecture.

## E019: the scheduler number outran its calibration

A 20.8836 tok/s/user worker-event result looked exciting, but the serial reconstruction missed block 16 by 103.9%. The throughput claim was rejected. Capacity decomposition and correctness survived because they depended on different evidence.

## E020: deployment was not ready to spend money

The experiment froze a physically plausible 96-worker deployment candidate but retained `NO_GO`. Production dispatch, distribution and projection validation still had unresolved gates.

## E021: ordered replay showed the model was fundamentally wrong

Median model error was 95.54%, with p90 and maximum near 100%. This was not a small calibration miss. The residency and production execution assumptions were wrong enough to invalidate the event model.

## E022: model repaired, final research question still unanswered

Held-out ordered-DAG error fell to low single digits without a global multiplier. But two independent gates remained false: production-native individual primitive bindings and representative full-93 plan replay. The experiment therefore still reports `MODEL_INVALID` rather than promoting the six capacity unlocks into a final claim.

## E026: physical distribution did not become practical WAN serving

The three-machine Qwen3.8-27B path executed physically, but the best exact development rate was 1.615 tok/s against an 8 tok/s gate. The sealed run fell to 0.590 tok/s, differed from the local greedy stream at token 178, and ended after 282/512 tokens on a transport reset. Native MTP reduced target traversals but failed the frozen exactness corpus. Serial response wait consumed 95–98% of the token cycle, so faster remote kernels and activation compression did not address the measured bottleneck.

The repeated pattern is the point: **a mechanism is not promoted merely because it produces a favorable number.**
