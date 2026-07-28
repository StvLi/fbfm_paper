# Experiment Results

This directory stores versioned experiment records that are ready for review by
the paper team. Each experiment directory should contain its protocol, compact
raw ledgers, derived tables, source revisions, and known comparability limits.

| Directory | Scope | Status |
| --- | --- | --- |
| `dmzr_weight/` | DreamZero FBFM state-weight diagnosis and proportional-gain search | Complete; includes the 240-episode valid Pro6000 `kp` comparison |
| `dmzr_weight/formal_libero40_fbfm_kp00486968_20_a051933/` | DreamZero FBFM on LIBERO-40 with selected `kp` | Complete; 566/800 (70.75%) |

Large trajectories, checkpoints, videos, and full solver audits remain in the
experiment workspace. Their source paths and checksums are recorded in each
experiment manifest instead of being committed to the paper repository.
