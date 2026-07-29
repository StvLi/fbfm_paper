# Lingbot-VA FBFM RoboTwin short-task combined results

Updated: `2026-07-26T12:01:31+08:00`

Status: **COMPLETE**

Canonical 12-task merged view. All tasks use one publication denominator. This file is final only when status is `COMPLETE`; `RUNNING` and `INVALID` must not be used as paper results.

| Tasks | Episodes | Success / failure | Micro | Macro | Micro Wilson 95% CI |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 12/12 | 240/240 | 216 / 24 | 90.00% | 90.00% | 85.55%–93.19% |

| Task | Status | Success | Rate | Wilson 95% CI |
| --- | --- | ---: | ---: | ---: |
| `adjust_bottle` | complete | 20/20 | 100.00% | 83.89%–100.00% |
| `beat_block_hammer` | complete | 15/20 | 75.00% | 53.13%–88.81% |
| `click_alarmclock` | complete | 20/20 | 100.00% | 83.89%–100.00% |
| `grab_roller` | complete | 20/20 | 100.00% | 83.89%–100.00% |
| `click_bell` | complete | 20/20 | 100.00% | 83.89%–100.00% |
| `lift_pot` | complete | 20/20 | 100.00% | 83.89%–100.00% |
| `scan_object` | complete | 13/20 | 65.00% | 43.29%–81.88% |
| `place_empty_cup` | complete | 20/20 | 100.00% | 83.89%–100.00% |
| `move_can_pot` | complete | 19/20 | 95.00% | 76.39%–99.11% |
| `place_shoe` | complete | 11/20 | 55.00% | 34.21%–74.18% |
| `move_pillbottle_pad` | complete | 20/20 | 100.00% | 83.89%–100.00% |
| `place_burger_fries` | complete | 18/20 | 90.00% | 69.90%–97.21% |

## Validation

- Errors: 0
- Incomplete conditions: 0
- Runtime events: 21 total, 1 unexpected
- Episode identity uses `(task, actual_seed)` recovered from `client.log`.

The single historical non-cleanup runtime event is a recovered Stage-1 `lift_pot` scene-generation assertion, not an active model/server failure.

## Polling history

| Boundary | Tasks | Episodes | Success / failure | Micro | GPU used / util |
| --- | ---: | ---: | ---: | ---: | ---: |
| 11:15 | 10/12 | 233/240 | 209 / 24 | 89.70% | 52222 MiB / 85% |
| 11:30 | 11/12 | 236/240 | 212 / 24 | 89.83% | 29016 MiB / 0% |
| 11:45 | 11/12 | 238/240 | 214 / 24 | 89.92% | 28477 MiB / 0% |
| 12:00 | 11/12 | 239/240 | 215 / 24 | 89.96% | 28761 MiB / 0% |
| 12:01 | 12/12 | 240/240 | 216 / 24 | 90.00% | 17 MiB / 0% |

The run completed at 12:01. Relaunches and `.failed` markers are zero; the completed logs contain no OOM, NaN, CUDA error, or killed process.

The historical `lift_pot` assertion occurred while `TASK_ENV.play_once()` was validating an expert scene, before the rollout counter was incremented. The evaluator caught it, advanced the seed, and continued. It was therefore a skipped pre-rollout seed rather than a counted policy failure; `lift_pot` still has 20 complete rollout records and needs no replacement episode. The final `place_burger_fries` server `SignalException` occurred only after seed 10022 succeeded and the result was saved, during expected server teardown.
