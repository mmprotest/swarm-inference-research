# Public-bundle sanitization and curation

This repository was generated from the uploaded runtime repository snapshot and the Experiment 016–022 artifact archive.

For public release:

1. Absolute local user/repository/model paths were replaced with placeholders such as `<local-repo>`, `<user-home>`, and `<local-kimi-k3-checkpoint>`.
2. No model weights are redistributed.
3. No credentials are intentionally included. The source Experiment 020 security receipt itself records `api_key_in_artifacts=false` and `hf_token_in_artifacts=false`.
4. Very large duplicate traces, temporary directories, repeated inventory copies, and generated placement payloads were excluded from the Git-friendly bundle.
5. A complete source-archive member index, including ZIP CRC32 and uncompressed size, is retained under `provenance/`.
6. A SHA-256 manifest of every file in this curated public repository is generated after sanitization.

Sanitization changes path strings only. It does not alter numerical measurement fields, verdicts, hashes of model/checkpoint content, or benchmark metrics. The E019 compact full-93 correctness receipt is explicitly marked as derived and contains the SHA-256 of its original 36 MB source member.
