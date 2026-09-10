# Public-bundle sanitization and curation

This repository was generated from the uploaded runtime repository snapshot, the Experiment 016–022 artifact archive, and the supplied Experiment 026 artifact directory.

For public release:

1. Absolute local user/repository/model paths were replaced with placeholders such as `<local-repo>`, `<user-home>`, and `<local-kimi-k3-checkpoint>`.
2. No model weights are redistributed.
3. No credentials are intentionally included. The source Experiment 020 security receipt itself records `api_key_in_artifacts=false` and `hf_token_in_artifacts=false`.
4. Very large duplicate traces, temporary directories, repeated inventory copies, and generated placement payloads were excluded from the Git-friendly bundle.
5. The Experiments 016–022 archive retains a complete member index with ZIP CRC32 and uncompressed size. The 831-file E026 source directory retains a separate path, byte-size, and SHA-256 index under `provenance/`.
6. E026's public metrics, summary, receipt, and report replace machine-local identity strings and record both source and public hashes in `experiments/026/evidence/source-manifest.json`.
7. A SHA-256 manifest of every file in this curated public repository is generated after sanitization.

Sanitization changes identity/path strings and public artifact bindings only. It does not alter numerical measurement fields, verdicts, hashes of model/checkpoint content, or benchmark metrics. The E019 compact full-93 correctness receipt and the E026 public summary/receipt are explicitly marked as derived and retain the SHA-256 of their source artifacts.
