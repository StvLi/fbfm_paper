# Lingbot-VA RTC RoboTwin short-task clean-20 run

## Goal

Evaluate Lingbot-VA in RTC mode on the selected 12 RoboTwin `demo_clean` tasks with
exactly 20 accepted episodes per task, for 240 accepted episodes in total. The model
checkpoint and inference protocol remain frozen; no training or weight update is
allowed.

The result is split into two independent batches:

| Batch | Candidate seed block | Episodes per task | Output root | State |
| --- | ---: | ---: | --- | --- |
| Stage 1 | 10000 (`ROBOTWIN_EVAL_SEED=0`) | 10 | `robotwin_outputs/rtc_short_le800_clean_10` | complete |
| Stage 2 | 20000 (`ROBOTWIN_EVAL_SEED=1`) | 10 | `robotwin_outputs/rtc_short_le800_clean_stage2_seed20000_10` | complete |

Stage 2 starts only after Stage 1 is complete and its three server/simulator shards have
exited. It uses a separate output and paper directory and does not import, link, truncate,
or overwrite Stage-1 artifacts.

## Tasks

1. `place_burger_fries`
2. `place_empty_cup`
3. `place_shoe`
4. `scan_object`
5. `adjust_bottle`
6. `beat_block_hammer`
7. `click_alarmclock`
8. `click_bell`
9. `grab_roller`
10. `lift_pot`
11. `move_can_pot`
12. `move_pillbottle_pad`

## Runtime And Protocol

- Mode: `RTC`, previous-action constraint only; state guidance disabled
- Checkpoint: `/home/oem/tmp_ws/checkpoints/lingbot-va-posttrain-robotwin`
- Config: RoboTwin `demo_clean`, SAPIEN GPU rendering
- Parallelism: three isolated policy-server/simulator shards at most
- Stage-1 launcher: PID `197163`, started `2026-07-26T12:11:25+08:00`
- Stage-1 monitor: PID `197463`
- Stage-2 launcher: PID `264065`, started `2026-07-26T21:16:57+08:00` via
  `script/run_robotwin_short_le800_clean_rtc_stage2_seed20000_10.sh`
- Stage-2 monitor: PID `264368`, 1,800-second interval
- Training or weight updates: none

Expert-scene validation may reject candidate seeds before rollout acceptance. Final
identity therefore comes from each client log's accepted `current seed`; nominal
`stseed + video_index` values are not used for pairing or uniqueness checks.

## Polling

The experiment-level record is checked every 30 minutes at `:00` and `:30`. Each poll
records the two aggregates, status JSONL, launcher/monitor/worker/server/client process
state, GPU memory/utilization, active task names, and OOM/NaN/Traceback/killed-process
health. The Stage-1 monitor was launched earlier at a 15-minute interval; its additional
local snapshots are retained, while this combined record uses the requested 30-minute
reporting cadence. No running process is restarted merely to change that cadence.

An OOM, NaN/non-finite value, CUDA failure, unrecovered process exit, result-count
mismatch, or repeated task failure is reported immediately. The protocol is not changed
automatically in response.

## Final Gates

- each stage contains exactly 12 tasks and exactly 10 accepted episodes per task;
- each merged task contains exactly 20 accepted episodes;
- the merged total is exactly 240 and successes plus failures equal 240;
- all `(task, actual_seed)` identities and resolved nonempty video paths are unique;
- source counts, success labels, and videos are mutually consistent;
- no fatal runtime anomaly or incomplete condition remains;
- per-task Wilson 95% intervals, micro success rate, macro task success rate, and anomaly
  statistics are regenerated from the final merged artifacts.

After all gates pass, the final RTC package is committed once to
`fbfm_paper:exp/lbva_rtc_gpurender_result` under `result/lbva_rtc/` and pushed to
`origin`. Running snapshots are not pushed periodically.

## Baseline Before First 30-Minute Poll

At the Stage-1 monitor boundary `2026-07-26T12:45:00+08:00`, the aggregate was
`10/120`, with 10 successes and 0 failures. Active tasks were `scan_object`,
`place_empty_cup`, and `move_pillbottle_pad`; GPU memory was 73,229 MiB, relaunches were
zero, and active logs contained no OOM, NaN/non-finite value, RuntimeError, Traceback, or
killed process.

## 30-Minute Polling Log

| Boundary | Stage | Complete tasks | Episodes | Success / failure | Micro | Active tasks | GPU used / util | Relaunches | Health |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |
| 13:00 | Stage 1 | 0/12 | 14/120 | 14 / 0 | 100.0% | `scan_object`, `place_empty_cup`, `move_pillbottle_pad` | 76880 MiB / 62% | 0 | clean |
| 13:30 | Stage 1 | 2/12 | 26/120 | 25 / 1 | 96.15% | `scan_object`, `lift_pot`, `place_shoe` | 72341 MiB / 82% | 0 | one caught expert-check scene rejection; no fatal anomaly |
| 14:00 | Stage 1 | 3/12 | 37/120 | 36 / 1 | 97.30% | `scan_object`, `beat_block_hammer`, `place_shoe` | 75917 MiB / 0% | 0 | clean |
| 14:30 | Stage 1 | 3/12 | 43/120 | 42 / 1 | 97.67% | `beat_block_hammer`, `place_shoe`, `scan_object` | 78240 MiB / 38% | 0 | clean |
| 15:00 | Stage 1 | 3/12 | 44/120 | 42 / 2 | 95.45% | `beat_block_hammer`, `place_shoe`, `scan_object` | 79422 MiB / 0% | 0 | clean |
| 15:30 | Stage 1 | 3/12 | 49/120 | 45 / 4 | 91.84% | `beat_block_hammer`, `place_shoe`, `scan_object` | 78070 MiB / 2% | 0 | clean |
| 16:00 | Stage 1 | 4/12 | 57/120 | 51 / 6 | 89.47% | `click_alarmclock`, `place_shoe`, `scan_object` | 74714 MiB / 97% | 0 | clean |
| 16:30 | Stage 1 | 5/12 | 64/120 | 58 / 6 | 90.62% | `place_shoe`, `scan_object` | 53641 MiB / 0% | 0 | clean |
| 17:00 | Stage 1 | 6/12 | 73/120 | 66 / 7 | 90.41% | `click_bell`, `place_shoe` | 49639 MiB / 0% | 0 | clean |
| 17:30 | Stage 1 | 7/12 | 83/120 | 75 / 8 | 90.36% | `move_can_pot`, `place_shoe` | 48752 MiB / 97% | 0 | clean |
| 18:00 | Stage 1 | 8/12 | 89/120 | 81 / 8 | 91.01% | `adjust_bottle`, `place_shoe` | 48146 MiB / 0% | 0 | clean |
| 18:30 | Stage 1 | 8/12 | 98/120 | 89 / 9 | 90.82% | `adjust_bottle`, `place_shoe` | 46499 MiB / 96% | 0 | clean |
| 19:00 | Stage 1 | 11/12 | 110/120 | 101 / 9 | 91.82% | `place_burger_fries` | 24385 MiB / 34% | 0 | clean |
| 19:30 | Stage 1 | 11/12 | 113/120 | 104 / 9 | 92.04% | `place_burger_fries` | 24886 MiB / 0% | 0 | clean |
| 20:00 | Stage 1 | 11/12 | 116/120 | 107 / 9 | 92.24% | `place_burger_fries` | 25998 MiB / 0% | 0 | clean |
| 20:30 | Stage 1 | 11/12 | 119/120 | 110 / 9 | 92.44% | `place_burger_fries` | 25484 MiB / 0% | 0 | clean |
| 21:30 | Stage 2 | 0/12 | 4/120 | 4 / 0 | 100.00% | `scan_object`, `place_empty_cup`, `move_pillbottle_pad` | 73444 MiB / 34% | 0 | clean |
| 22:00 | Stage 2 | 0/12 | 17/120 | 17 / 0 | 100.00% | `scan_object`, `place_empty_cup`, `move_pillbottle_pad` | 75134 MiB / 0% | 0 | clean |
| 22:30 | Stage 2 | 2/12 | 27/120 | 27 / 0 | 100.00% | `scan_object`, `lift_pot`, `place_shoe` | 75453 MiB / 36% | 0 | clean |
| 23:00 | Stage 2 | 3/12 | 39/120 | 39 / 0 | 100.00% | `scan_object`, `beat_block_hammer`, `place_shoe` | 76983 MiB / 30% | 0 | clean |
| 23:30 | Stage 2 | 3/12 | 45/120 | 44 / 1 | 97.78% | `scan_object`, `beat_block_hammer`, `place_shoe` | 77944 MiB / 0% | 0 | clean |
| 00:00 | Stage 2 | 3/12 | 45/120 | 44 / 1 | 97.78% | `scan_object`, `beat_block_hammer`, `place_shoe` | 81074 MiB / 0% | 0 | clean |
| 00:30 | Stage 2 | 3/12 | 49/120 | 46 / 3 | 93.88% | `scan_object`, `beat_block_hammer`, `place_shoe` | 76926 MiB / 88% | 0 | clean |
| 01:00 | Stage 2 | 3/12 | 53/120 | 48 / 5 | 90.57% | `scan_object`, `beat_block_hammer`, `place_shoe` | 77862 MiB / 35% | 0 | clean |
| 01:30 | Stage 2 | 5/12 | 67/120 | 61 / 6 | 91.04% | `beat_block_hammer`, `move_can_pot`, `place_shoe` | 76246 MiB / 0% | 0 | clean |
| 02:00 | Stage 2 | 7/12 | 89/120 | 82 / 7 | 92.13% | `click_alarmclock`, `grab_roller`, `move_can_pot` | 72116 MiB / 97% | 0 | clean |
| 02:30 | Stage 2 | 10/12 | 104/120 | 97 / 7 | 93.27% | `adjust_bottle`, `place_burger_fries` | 49309 MiB / 44% | 0 | clean |
| 03:00 | Stage 2 | 10/12 | 108/120 | 101 / 7 | 93.52% | `adjust_bottle`, `place_burger_fries` | 51990 MiB / 0% | 0 | clean |
| 03:30 | Stage 2 | 11/12 | 116/120 | 108 / 8 | 93.10% | `place_burger_fries` | 25996 MiB / 31% | 0 | clean |
| 04:00 | Stage 2 | 11/12 | 119/120 | 111 / 8 | 93.28% | `place_burger_fries` | 25941 MiB / 0% | 0 | clean |
| 04:30 | Stage 2 | 12/12 | 120/120 | 112 / 8 | 93.33% | none | 17 MiB / 0% | 0 | complete; experiment processes exited cleanly |

At the 13:30 boundary, `scan_object` had one accepted rollout that ran to its normal
500-step limit and was recorded consistently as a failure with a nonempty video. The
`lift_pot` client also logged one `AssertionError` while validating an expert scene
before rollout acceptance (`target_pose cannot be None for move action`). The client
caught the exception in its `expert_check` loop, advanced the candidate seed, and
continued running; this did not consume an accepted episode and requires no episode
replacement. All three clients and servers remained alive, result counts were
consistent, relaunches remained zero, and no OOM, CUDA failure, NaN/non-finite value, or
killed process was found.

At the 14:00 boundary, `lift_pot` had completed 10/10 successfully and its shard had
advanced to `beat_block_hammer`. The three active logs were clean; the caught
`lift_pot` expert-scene rejection remains retained in the final anomaly audit as an
expected skipped candidate rather than disappearing from provenance. GPU utilization
was sampled at 0% at the exact boundary while all three client/server pairs were alive
and producing work; this is a momentary sampling value, not evidence of an idle or
stopped experiment.

At `2026-07-26T20:45:00+08:00`, the Stage-1 monitor recorded `complete`: 12/12 tasks,
120/120 accepted episodes, 111 successes and 9 failures (92.50% micro success), with
the launcher, workers, clients, and servers all exited and zero relaunches. The strict
pre-handoff audit confirmed exactly 10 accepted episodes for every task, 120 unique
`(task, actual_seed)` identities, 120 unique nonempty videos, and no validation error,
incomplete condition, or fatal runtime event. Provenance retains one expected caught
`lift_pot` expert-scene rejection and the 12 expected post-client server SIGTERM traces;
neither consumed or invalidated an accepted episode.

At `2026-07-26T21:16:57+08:00`, after Stage-1 teardown and validation, Stage 2 was
started in its independent `stseed-20000` output root. Launcher PID `264065` created
three worker/server shards for `scan_object`, `place_empty_cup`, and
`move_pillbottle_pad`; monitor PID `264368` started at `21:16:58` with a 1,800-second
interval. The initial status snapshot reported all three server shards alive, 0/120
accepted episodes, zero relaunches, and no OOM, CUDA error, NaN/non-finite value,
RuntimeError, Traceback, or killed process.

At the 21:30 boundary, the Stage-2 aggregate and status snapshot agreed on 4/120
accepted episodes, all successful: `scan_object` 1/1, `place_empty_cup` 1/1, and
`move_pillbottle_pad` 2/2. The three launcher workers, policy servers, and simulator
clients were alive; accepted seeds had begun at 20000 as required, relaunches remained
zero, and active logs contained no fatal anomaly.

At `2026-07-27T04:30:00+08:00`, the Stage-2 monitor recorded `complete`: 12/12 tasks,
120/120 accepted episodes, 112 successes and 8 failures (93.33% micro success), with
zero relaunches. The launcher, workers, policy servers, and simulator clients had all
exited; only the monitor remained long enough to write the terminal snapshot. The
aggregate completed successfully, active-log health was clean, and the OOM/CUDA-OOM,
NaN/non-finite, RuntimeError, Traceback, and killed-process counters were all zero.

## Final Validation

At `2026-07-28T12:41:16+08:00`, the strict two-stage combiner completed successfully.
All 16 final gates passed: each stage contributed exactly 12 tasks and 120 accepted
episodes, every merged task contained exactly 20 episodes, and the combined result was
223 successes and 17 failures out of 240 (92.92% micro and macro success). The micro
Wilson 95% confidence interval was 88.95%-95.53%.

The audit confirmed 240 unique `(task, actual_seed)` identities, 240 unique nonempty
videos, 24 unique result sources, aggregate/source consistency, RTC provenance for all
sources, zero validation errors, zero incomplete conditions, and zero fatal runtime
events. Its 25 retained runtime events were all expected: 24 post-client server SIGTERM
shutdowns and one pre-rollout `lift_pot` expert-scene rejection.
