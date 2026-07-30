# DreamZero FBFM LIBERO-40 Results Before `kp` Optimization

This directory records the completed DreamZero FBFM evaluation at `cb08c9e`,
before the separate proportional state-feedback gain was introduced and tuned.

## Result Snapshot

| Suite | Successes / episodes | Success rate |
| --- | ---: | ---: |
| LIBERO-Spatial | 153 / 200 | 76.50% |
| LIBERO-Object | 143 / 200 | 71.50% |
| LIBERO-Goal | 146 / 200 | 73.00% |
| LIBERO-10 | 111 / 200 | 55.50% |
| **LIBERO-40** | **553 / 800** | **69.125%** |

All 40 tasks contain exactly 20 official trials. The raw ledgers contain 800
unique `(suite, task_id, trial_id)` records, zero duplicate trials, and finite
actions in every episode.

## Protocol And Provenance

- Mode: `FBFM`
- Route commit: `cb08c9e552730d26cc446885e79a3e270a270d0c`
- Outer integration runner: `8d4184f0ada01911d874853bdb3abacd6b536e04`
- External DreamZero base: `ab790c198fbce33503358efbbd4187ce9a89adf3`
- Checkpoint: `RLinf-DreamZero-WAN2.2-5B-LIBERO-SFT-Step26000`
- State weight: `56/9600 = 0.005833333333333334`
- Suites: `libero_spatial`, `libero_object`, `libero_goal`, `libero_10`
- Trials: official IDs `0-19`, 20 per task, 800 total
- Seeds: environment seed 0; fixed model seed 0
- Horizon: 480 environment steps for every suite
- Solver release policy: uniform
- Source result root:
  `/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_feedback_cb08c9e_20260726/runs/formal_libero40_fbfm_l1mass_20_cb08c9e`

See `runtime/RUN_RECORD.md` for the route checkout, external source snapshots,
preflight validation, and the stride-3 live-audit contract used by this run.

## Included Records

| Path | Contents |
| --- | --- |
| `summary.json` | final benchmark aggregate |
| `task_summary.csv` | all 40 task-level rates |
| `trials.csv` | normalized 800-episode ledger |
| `shards/` | shard manifests, summaries, per-task episode ledgers, and trial tables |
| `workers/gpu*/ready.json` | exact server mode and runtime protocol evidence |
| `runtime/` | launch, monitor, audit validator, and provenance record used by the run |
| `SHA256SUMS` | hashes for every packaged file except the checksum file itself |

## External Artifacts

Following the repository result policy, simulator trajectories, verbose logs,
PID files, and full solver audits remain in the source workspace. They are not
required to reproduce the reported counts from the committed episode ledgers.
The excluded source material comprises 800 trajectory files (5,484,698 bytes),
8 solver audits (710,194,681 bytes), and 18 logs (9,409,067 bytes).
