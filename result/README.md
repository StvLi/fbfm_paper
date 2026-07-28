# Experiment Results

This top-level directory stores compact, reviewable experiment artifacts. Large videos,
model checkpoints, simulator caches, and raw server logs remain in the experiment
workspace and are not committed to the paper repository.

| Current branch | Directory | Experiment | State |
| --- | --- | --- | --- |
| `exp/lbva_rtc_gpurender_result` | `result/lbva_rtc/` | Lingbot-VA, RTC, RoboTwin GPU rendering | **FINAL** |

The separate Lingbot-VA + FBFM result is stored on branch
`exp/lbva_fbfm_gpurender_result` under `result/lbva_fbfm/`; it is not duplicated on
this RTC result branch.

The RTC result is final: all 12 tasks and 240 accepted episodes passed the 16
validation gates, with 223 successes and 17 failures. Micro and macro success rates
are both 92.92%; the micro Wilson 95% confidence interval is 88.95%-95.53%. No fatal
runtime event was found.

Each experiment directory contains a README, machine-readable aggregate and trial
tables, validation or monitoring material, and a SHA-256 manifest. Generated artifacts
retain their original absolute source paths for provenance; those paths are not expected
to resolve on another workstation.
