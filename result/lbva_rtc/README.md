# Lingbot-VA RTC RoboTwin Results

## State

**FINAL.** All 12 selected RoboTwin `demo_clean` tasks reached exactly 20 accepted
episodes, for 240/240 episodes in total. The final result contains 223 successes and 17
task failures: micro and macro success rates are both 92.92%, and the micro Wilson 95%
confidence interval is 88.95%-95.53%.

All 16 strict completion gates in `validation.json` are true. Validation found 240
unique `(task, actual_seed)` identities, 240 unique nonempty result videos, and zero
fatal runtime events. Per-task results and Wilson intervals are reported in
`summary.md` and `task_summary.csv`.

## Protocol

- Model: frozen Lingbot-VA post-trained RoboTwin checkpoint at
  `/home/oem/tmp_ws/checkpoints/lingbot-va-posttrain-robotwin`; no training or weight
  update
- Mode: `RTC`, previous-action constraint only; state feedback guidance disabled
- Simulator/config: RoboTwin `demo_clean`, SAPIEN GPU rendering
- Schedule: deterministic pseudo-asynchronous inference, with no wall-clock delay used
  to determine method variables
- Horizon and latent geometry: `H=32`, `d=16`, `s=16`
- Video flow: 25 numerical steps plus one cache-only evaluation, for 26 evaluations
  deterministically assigned to 16 simulator steps
- Action flow: 50 numerical steps plus one cache-only evaluation, for 51 evaluations
- Seed batches: independent `stseed-10000` and `stseed-20000` batches, each providing
  10 accepted episodes per task
- Parallelism: three isolated policy-server/simulator shards

## Result Files

| File | Contents |
| --- | --- |
| `aggregate.json` | final combined machine-readable aggregate |
| `summary.md` | final metrics, ordered per-task results, and anomaly summary |
| `task_summary.csv` | per-task counts, success rates, and Wilson 95% intervals |
| `trials.csv` | all 240 accepted episode records and actual seeds |
| `validation.json` | strict validation report with all 16 gates true |
| `runbook.md` | scope, launch metadata, protocol, and polling record |
| `stage1_status_reports.jsonl` | monitor history for the seed-10000 batch |
| `stage2_status_reports.jsonl` | monitor history for the seed-20000 batch |
| `SHA256SUMS` | integrity hashes for the packaged result |

Large videos, complete client/server logs, checkpoints, and simulator caches are not
committed to Git. Compact records retain the original workstation paths for provenance.

## Runtime Anomalies

The audit classified 24 post-client server `SIGTERM` traces as expected shard teardown
and one expert-scene rejection as expected candidate-seed filtering. The rejection is not
an accepted episode and is not counted among the 17 task failures. Fatal events: 0.
