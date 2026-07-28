# Experiment Results

This top-level directory stores compact, reviewable experiment artifacts. Large videos,
model checkpoints, simulator caches, and raw server logs remain in the experiment
workspace and are not committed to the paper repository.

| Branch | Directory | Experiment | State |
| --- | --- | --- | --- |
| `exp/lbva_fbfm_gpurender_result` | `result/lbva_fbfm_gpu/` | Lingbot-VA, FBFM, RoboTwin GPU rendering | final |
| `exp/lbva_rtc_gpurender_result` | `result/lbva_rtc/` | Lingbot-VA, RTC, RoboTwin GPU rendering | running |

Each experiment directory contains a README, machine-readable aggregate and trial
tables, validation material, and a SHA-256 manifest. Generated artifacts retain their
original absolute source paths for provenance; those paths are not expected to resolve
on another workstation.
