# DreamZero FBFM Three-Weight Progress Checkpoint

Captured: `2026-07-26T22:12:59+08:00`

Sweep state: `running:l1mass_005833`; episodes: `286/300`; completed task-weight cells: `57/60`.

This is the user-requested in-progress cloud checkpoint. It is not the final three-weight result. The A6000 sweep continued without interruption after this commit.

## Aggregate progress

| Weight | Episodes | Success | Rate | Mean steps | Mean seconds | Action norm max | Norm > 10 | Norm > 100 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `1` | 100/100 | 0 | 0.0% | 480.0 | 148.14 | 25453960.778 | 11264 | 2265 |
| `sqrt(56/9600)` | 100/100 | 59 | 59.0% | 300.1 | 93.56 | 9028.948 | 43 | 24 |
| `56/9600` | 86/100 | 65 | 75.6% | 233.6 | 73.39 | 1.608 | 0 | 0 |

## Per-task progress

| Suite | Task | Binary | RMS | L1 mass |
| --- | ---: | ---: | ---: | ---: |
| `libero_spatial` | 0 | 0/5 | 4/5 | 4/5 |
| `libero_spatial` | 1 | 0/5 | 3/5 | 5/5 |
| `libero_spatial` | 2 | 0/5 | 5/5 | 5/5 |
| `libero_spatial` | 3 | 0/5 | 3/5 | 5/5 |
| `libero_spatial` | 4 | 0/5 | 0/5 | 1/5 |
| `libero_spatial` | 5 | 0/5 | 2/5 | 2/5 |
| `libero_spatial` | 6 | 0/5 | 4/5 | 5/5 |
| `libero_spatial` | 7 | 0/5 | 4/5 | 5/5 |
| `libero_spatial` | 8 | 0/5 | 4/5 | 5/5 |
| `libero_spatial` | 9 | 0/5 | 1/5 | 3/5 |
| `libero_object` | 0 | 0/5 | 4/5 | 3/5 |
| `libero_object` | 1 | 0/5 | 4/5 | 5/5 |
| `libero_object` | 2 | 0/5 | 2/5 | 3/5 |
| `libero_object` | 3 | 0/5 | 3/5 | 5/5 |
| `libero_object` | 4 | 0/5 | 0/5 | 2/5 |
| `libero_object` | 5 | 0/5 | 4/5 | 5/5 |
| `libero_object` | 6 | 0/5 | 1/5 | 2/5 |
| `libero_object` | 7 | 0/5 | 2/5 | 0/1 |
| `libero_object` | 8 | 0/5 | 4/5 | 0/0 |
| `libero_object` | 9 | 0/5 | 5/5 | 0/0 |

## Interpretation at checkpoint

The binary support matrix `W` remains hard 0/1 for every run. These experiments change only the separate state preconditioner `P_Z`.

- `P_Z=1` is an unattenuated stress test. Its result tests whether binary hard overlap alone is numerically sufficient.
- `P_Z=sqrt(56/9600)` is the isotropic Euclidean/RMS normalization. It balances expected residual norms but ignores anisotropic cross-modal Jacobian gain.
- `P_Z=56/9600` is the conservative coefficient-mass normalization. It is expected to suppress cached-Jacobian positive feedback at the cost of weaker state guidance.

Only completed 5-episode task cells should be read as task estimates. A running cell and all aggregate L1 values remain provisional at this checkpoint.

## Artifacts

- `data/progress_40min/analysis/ANALYSIS.md`: generated provisional analysis
- `data/progress_40min/analysis/verification.json`: explicit incomplete/complete status
- `data/control/latest_status.md`: latest synchronized monitor table
- `data/*/tasks/*/task_*/episodes.jsonl`: compact episode ledgers
