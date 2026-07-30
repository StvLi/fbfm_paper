# Experiment Results

This directory stores versioned experiment records for paper review. Each
result package retains its protocol, compact ledgers, derived summaries, source
revisions, comparability limits, and integrity metadata when available. Large
videos, checkpoints, simulator caches, and full logs remain in the experiment
workspaces.

| Directory | Scope | Included result state |
| --- | --- | --- |
| `lbva_none/` | LingBot-VA without feedback on RoboTwin, CPU rendering | 37 complete 10-episode cells |
| `lbva_fbfm/` | LingBot-VA with FBFM on RoboTwin, CPU rendering | Original 45-cell snapshot plus a seed-audited under-900 follow-up |
| `lbva_fbfm_gpu/` | LingBot-VA with FBFM on RoboTwin `demo_clean`, GPU rendering | 12 complete tasks, 216/240 successes |
| `lbva_rtc/` | LingBot-VA with RTC on RoboTwin `demo_clean`, GPU rendering | 12 complete tasks, 223/240 successes |
| `lbva_fbfm_auxiliary_mechanism/` | LingBot-VA FBFM state/action mechanism pilot on RoboTwin | 4 paired units and 8 cache-intervention probes; no added rollouts |
| `dmzr_weight/` | DreamZero FBFM state-weight diagnosis and proportional-gain search | Includes the valid 240-episode Pro6000 `kp` comparison |
| `dmzr_weight/formal_libero40_fbfm_kp00486968_20_a051933/` | DreamZero FBFM on the four selected LIBERO suites with selected `kp` | Complete; 566/800 (70.75%) |
| `dmzr_weight/formal_libero40_none_20_cb08c9e/` | DreamZero NONE on the same four selected LIBERO suites | Complete; 561/800 (70.125%) |
| `dmzr_weight/formal_libero40_fbfm_l1mass_20_cb08c9e/` | DreamZero FBFM before separate `kp` optimization | **Archived/superseded; excluded from manuscript statistics**; 553/800 (69.125%) |
| `wan2.2_real_video/` | Wan2.2 Base versus visual-only FBFM on real videos | RealSense ball-stopping package complete; includes videos, frames, audits, and runtime snapshot |

The CPU snapshots use only cells satisfying
`status == complete && trials == 10`. The LingBot-VA GPU packages contain
episode-level records for 240 strictly validated trials per method; Appendix D
currently reports only the first 10 accepted FBFM episodes per task. Coverage,
rendering mode, and episode identities differ across packages, so pooled rates
must not be treated as matched method comparisons without checking the package
protocols and trial identities.
