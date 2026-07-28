# Experiment Results

This directory stores compact, reviewable LingBot-VA evaluation artifacts.
Large videos, checkpoints, simulator caches, and server logs remain in the
experiment workspaces and are not committed to the paper repository.

| Directory | Experiment | Included result state |
| --- | --- | --- |
| `lbva_fbfm/` | LingBot-VA with FBFM on RoboTwin, CPU rendering | 45 complete 10-episode cells |
| `lbva_none/` | LingBot-VA without feedback on RoboTwin, CPU rendering | 37 complete 10-episode cells |
| `lbva_fbfm_gpu/` | LingBot-VA with FBFM on RoboTwin `demo_clean`, GPU rendering | 12 complete 20-episode tasks |

Each directory contains its own protocol, provenance, validation, and integrity
record. The CPU snapshots retain all planned cells in normalized ledgers and use
only cells satisfying `status == complete && trials == 10`. The GPU result
contains episode-level records for 240 strictly validated trials.

Coverage, rendering mode, and episode identities differ across these result
packages. Their pooled rates are descriptive and must not be treated as a
matched FBFM-versus-NONE comparison.
