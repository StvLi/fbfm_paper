# Lingbot-VA FBFM RoboTwin Results

## Result

This is the confirmed final result for the selected 12 RoboTwin `demo_clean` tasks.
Each task has exactly 20 accepted episodes.

| Tasks | Episodes | Success / failure | Micro success | Macro success | Micro Wilson 95% CI |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 12/12 | 240/240 | 216 / 24 | 90.00% | 90.00% | 85.55%-93.19% |

The strict validator confirms 240 unique `(task, actual_seed)` identities, 240 unique
nonempty result videos, exact per-task counts, consistent success/failure totals, and no
fatal runtime anomaly. A `lift_pot` expert-scene assertion occurred before rollout
acceptance; the evaluator skipped that candidate seed, so it is not one of the 240
episodes. Server SIGTERM tracebacks occurred after completed clients during normal
teardown. No OOM, NaN/non-finite value, CUDA failure, or killed process affected a
counted episode.

## Protocol

- Model: Lingbot-VA post-trained RoboTwin checkpoint, weights frozen
- Mode: `FBFM`, state constraint plus previous-action constraint
- Simulator/config: RoboTwin `demo_clean`, SAPIEN GPU rendering
- Solver horizon: `H=32`, constrained prefix `d=16`, execution stride `s=16`
- Video flow: 25 numerical steps plus one cache-only evaluation
- Action flow: 50 numerical steps plus one cache-only evaluation
- Feedback schedule: 26 video evaluations deterministically assigned to 16 simulator
  steps; one feedback latent per four accepted observations
- Parallelism: at most three isolated policy-server/simulator shards
- Frozen inference revision: `a116e48d9c8956c7ee66360ae68007bc146abcc3`
- Training or weight updates: none

The 12-task result combines retained legacy results, a seed-10000 first batch, a
nonoverlapping seed-20000 second batch, and the omitted normal task
`place_burger_fries`. Actual environment seeds are recovered from client logs because
expert-scene rejection can skip candidate seeds.

## Files

| File | Contents |
| --- | --- |
| `summary.md` | human-readable final table and Wilson intervals |
| `task_summary.csv` | one row per task with success count, rate, and Wilson interval |
| `trials.csv` | all 240 accepted episodes with nominal and actual seeds |
| `aggregate.json` | complete structured aggregate and episode records |
| `validation.json` | strict gates, provenance checks, and runtime anomaly inventory |
| `implementation_record.md` | scheduling, constraint, sharding, recovery, and aggregation record |
| `SHA256SUMS` | integrity hashes for the packaged artifacts |

The JSON and CSV artifacts preserve their original workstation paths as provenance.
Videos and full logs are intentionally excluded from Git because of their size; the
resolved paths and validation results remain in the structured artifacts.
