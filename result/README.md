# Experiment Results

This directory stores versioned experiment records for paper review. Each
result package retains its protocol, compact ledgers, derived summaries, source
revisions, comparability limits, and integrity metadata when available. Large
videos, checkpoints, simulator caches, and full logs remain in the experiment
workspaces.

| Directory | Scope | Included result state |
| --- | --- | --- |
| `lbva_none/` | LingBot-VA without feedback on RoboTwin, CPU rendering | 37 complete 10-episode cells |
| `lbva_fbfm/` | LingBot-VA with FBFM on RoboTwin, CPU rendering | 45 complete 10-episode cells |
| `lbva_fbfm_gpu/` | LingBot-VA with FBFM on RoboTwin `demo_clean`, GPU rendering | 12 complete 20-episode tasks |
| `dmzr_weight/` | DreamZero FBFM state-weight diagnosis and proportional-gain search | Includes the valid 240-episode Pro6000 `kp` comparison |

The CPU snapshots use only cells satisfying
`status == complete && trials == 10`. The LingBot-VA GPU package contains
episode-level records for 240 strictly validated trials; Appendix D currently
reports only the first 10 accepted episodes per task. Coverage, rendering mode,
and episode identities differ across packages, so pooled rates must not be
treated as matched method comparisons.
