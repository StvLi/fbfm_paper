# DreamZero FBFM LIBERO-40 Results (`kp=0.0486968`)

This directory records the completed DreamZero FBFM evaluation after applying
the selected proportional state-feedback gain.

## Result Snapshot

| Suite | Successes / episodes | Success rate |
| --- | ---: | ---: |
| LIBERO-Spatial | 154 / 200 | 77.00% |
| LIBERO-Object | 144 / 200 | 72.00% |
| LIBERO-Goal | 142 / 200 | 71.00% |
| LIBERO-10 | 126 / 200 | 63.00% |
| **LIBERO-40** | **566 / 800** | **70.75%** |

All 40 tasks contain exactly 20 official trials. The raw ledgers contain 800
unique `(suite, task_id, trial_id)` records, zero duplicate trials, and finite
actions in every episode.

## Protocol And Provenance

- Mode: `FBFM`
- Route commit: `a051933e2b058d74bb268e94080464569d99ce39`
- Outer integration runner: `8d4184f0ada01911d874853bdb3abacd6b536e04`
- Checkpoint: `RLinf-DreamZero-WAN2.2-5B-LIBERO-SFT-Step26000`
- State weight: `56/9600 = 0.005833333333333334`
- State feedback gain: `kp=0.0486968`
- Effective state weight: `0.0002840646666666667`
- Suites: `libero_spatial`, `libero_object`, `libero_goal`, `libero_10`
- Trials: official IDs `0-19`, 20 per task, 800 total
- Seeds: environment seed 0; fixed model seed 0
- Horizon: 480 environment steps for every suite
- Solver release policy: uniform
- Source result root:
  `/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_feedback_a051933_kp00486968_20260727/runs/formal_libero40_fbfm_kp00486968_20_a051933`

The run was resumed from a contiguous 37-episode prefix after its development
container stopped. Resume validation found no duplicate trials, and the final
ledger completed normally at 800 episodes. See `runtime/RUN_RECORD.md` for the
launch, online solver audit, and recovery evidence.

## Included Records

| Path | Contents |
| --- | --- |
| `summary.json` | final benchmark aggregate |
| `task_summary.csv` | all 40 task-level rates |
| `trials.csv` | normalized 800-episode ledger |
| `shards/` | shard manifests, summaries, per-task episode ledgers, and trial tables |
| `workers/gpu*/ready.json` | exact server mode, `kp`, and effective-weight evidence |
| `runtime/` | launch, monitor, audit validator, and provenance record used by the run |
| `SHA256SUMS` | hashes for every packaged file except the checksum file itself |

## External Artifacts

Following the repository result policy, simulator trajectories, verbose logs,
PID files, and full solver audits remain in the source workspace. They are not
required to reproduce the reported counts from the committed episode ledgers.
The excluded source material comprises 800 trajectory files (5,429,363 bytes),
8 solver audits (760,193,529 bytes), and 19 logs (9,174,202 bytes).
