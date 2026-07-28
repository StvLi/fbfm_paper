# Raw Ledgers

The `episodes.jsonl` files are direct copies of the completed A6000 experiment
ledgers. Each line contains one official LIBERO initial state, success label,
executed steps, timing, seed metadata, protocol metadata, and the original
trajectory path. The corresponding `summary.json` files are direct runner
outputs.

The absolute paths inside these records describe the source deployment and are
not expected to resolve on another machine. Use `../paired_trials.csv` and
`../weight_summary.csv` for compact analysis.

Full solver audits and trajectories are intentionally not committed. Their
source locations and SHA-256 hashes are recorded in `../manifest.json` and
`../checksums.sha256`.
