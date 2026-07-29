# DreamZero NONE LIBERO-40 Results

This directory records the completed DreamZero `NONE` evaluation on the four
standard LIBERO suites. It is the matched no-feedback reference for the
`cb08c9e` FBFM run.

## Result Snapshot

| Suite | Successes / episodes | Success rate |
| --- | ---: | ---: |
| LIBERO-Spatial | 157 / 200 | 78.50% |
| LIBERO-Object | 146 / 200 | 73.00% |
| LIBERO-Goal | 137 / 200 | 68.50% |
| LIBERO-10 | 121 / 200 | 60.50% |
| **LIBERO-40** | **561 / 800** | **70.125%** |

All 40 tasks contain exactly 20 official trials. The raw ledgers contain 800
unique `(suite, task_id, trial_id)` records, zero duplicate trials, and finite
actions in every episode.

## Protocol And Provenance

- Mode: `NONE`
- Route commit: `cb08c9e552730d26cc446885e79a3e270a270d0c`
- Checkpoint: `RLinf-DreamZero-WAN2.2-5B-LIBERO-SFT-Step26000`
- Suites: `libero_spatial`, `libero_object`, `libero_goal`, `libero_10`
- Trials: official IDs `0-19`, 20 per task, 800 total
- Seeds: environment seed 0; fixed model seed 0
- Horizon: 480 environment steps for every suite
- Solver release policy: uniform
- Source result root:
  `/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_none_cb08c9e_20260726/runs/formal_libero40_none_20_cb08c9e`

The recorded state weight is ignored in `NONE` mode. See
`runtime/RUN_RECORD.md`, `manifest.json` files, and `final_audit.json` for the
deployment and independent integrity audit.

## Included Records

| Path | Contents |
| --- | --- |
| `summary.json` | final benchmark aggregate |
| `task_summary.csv` | all 40 task-level rates |
| `trials.csv` | normalized 800-episode ledger |
| `shards/` | shard manifests, summaries, per-task episode ledgers, and trial tables |
| `workers/gpu*/ready.json` | exact server mode and runtime protocol evidence |
| `FINAL_REPORT.md` and `final_audit.json` | independent final validation |
| `runtime/` | launch, aggregation, and provenance record used by the run |
| `SHA256SUMS` | hashes for every packaged file except the checksum file itself |

## External Artifacts

Following the repository result policy, simulator trajectories, verbose logs,
PID files, and full solver audits remain in the source workspace. They are not
required to reproduce the reported counts from the committed episode ledgers.
The excluded source material comprises 800 trajectory files (5,527,121 bytes),
8 solver audits (422,242,404 bytes), and 18 logs (9,408,016 bytes).
