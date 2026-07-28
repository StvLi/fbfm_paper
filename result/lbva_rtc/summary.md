# Lingbot-VA + RTC Final Summary

## Final Result

**FINAL:** 12/12 tasks complete, with exactly 240/240 accepted episodes. Lingbot-VA +
RTC produced 223 successes and 17 failures on RoboTwin `demo_clean`.

| Metric | Result |
| --- | ---: |
| Micro success rate | 92.92% (223/240) |
| Micro Wilson 95% CI | 88.95%-95.53% |
| Macro success rate | 92.92% |
| Strict validation gates | 16/16 true |
| Fatal runtime events | 0 |

## Per-Task Results

| Task | Successes | Failures | Success rate | Wilson 95% CI |
| --- | ---: | ---: | ---: | ---: |
| `place_burger_fries` | 20/20 | 0 | 100.00% | 83.89%-100.00% |
| `place_empty_cup` | 20/20 | 0 | 100.00% | 83.89%-100.00% |
| `place_shoe` | 14/20 | 6 | 70.00% | 48.10%-85.45% |
| `scan_object` | 15/20 | 5 | 75.00% | 53.13%-88.81% |
| `adjust_bottle` | 19/20 | 1 | 95.00% | 76.39%-99.11% |
| `beat_block_hammer` | 15/20 | 5 | 75.00% | 53.13%-88.81% |
| `click_alarmclock` | 20/20 | 0 | 100.00% | 83.89%-100.00% |
| `click_bell` | 20/20 | 0 | 100.00% | 83.89%-100.00% |
| `grab_roller` | 20/20 | 0 | 100.00% | 83.89%-100.00% |
| `lift_pot` | 20/20 | 0 | 100.00% | 83.89%-100.00% |
| `move_can_pot` | 20/20 | 0 | 100.00% | 83.89%-100.00% |
| `move_pillbottle_pad` | 20/20 | 0 | 100.00% | 83.89%-100.00% |
| **Total** | **223/240** | **17** | **92.92%** | **88.95%-95.53%** |

## Protocol and Validation

RTC applies the previous-action constraint only, with state feedback guidance disabled.
The frozen Lingbot-VA post-trained RoboTwin checkpoint was evaluated without training or
weight updates under `demo_clean`, using deterministic pseudo-asynchronous scheduling,
`H=32`, `d=16`, and `s=16`. Video flow used 25 numerical steps plus one cache-only
evaluation (26 total); action flow used 50 numerical steps plus one cache-only evaluation
(51 total).

The run used three isolated server/simulator shards. Each task contributed 10 accepted
episodes from the `stseed-10000` batch and 10 from the independent `stseed-20000` batch.
Strict validation confirmed exactly 20 episodes per task, 240 unique
`(task, actual_seed)` identities, 240 unique nonempty videos, aggregate/source
consistency, and all 16 completion gates true.

## Anomalies

- Fatal runtime events: 0.
- Expected post-client server teardown traces: 24 `SIGTERM` events.
- Expected expert-scene rejections: 1 candidate seed, excluded before accepted-episode
  accounting.

Large videos and complete client/server logs are retained in the experiment workspace and
are not committed to Git.
