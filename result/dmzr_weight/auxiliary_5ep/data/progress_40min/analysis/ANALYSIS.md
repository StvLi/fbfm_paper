# DreamZero FBFM Three-Weight Auxiliary Results

Verification status: `incomplete`; episodes: `286/300`.

## Aggregate results

| Weight | Success | Micro | 95% Wilson CI | Mean steps | Mean seconds | Action norm max | Correction max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `1` | 0/100 | 0.0% | 0.0%-3.7% | 480.0 | 148.14 | 25453960.778 | 1238662656.000 |
| `sqrt(56/9600)` | 59/100 | 59.0% | 49.2%-68.1% | 300.1 | 93.56 | 9028.948 | 469042.344 |
| `56/9600` | 65/86 | 75.6% | 65.5%-83.4% | 233.6 | 73.39 | 1.608 | 16.316 |

## Suite results

| Weight | Suite | Success | Rate | 95% Wilson CI | Mean seconds |
| --- | --- | ---: | ---: | ---: | ---: |
| `binary` | `libero_spatial` | 0/50 | 0.0% | 0.0%-7.1% | 148.92 |
| `binary` | `libero_object` | 0/50 | 0.0% | 0.0%-7.1% | 147.36 |
| `rms` | `libero_spatial` | 30/50 | 60.0% | 46.2%-72.4% | 88.39 |
| `rms` | `libero_object` | 29/50 | 58.0% | 44.2%-70.6% | 98.73 |
| `l1_mass` | `libero_spatial` | 40/50 | 80.0% | 67.0%-88.8% | 66.04 |
| `l1_mass` | `libero_object` | 25/36 | 69.4% | 53.1%-82.0% | 83.60 |

## Per-task results

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

## Pairwise episode comparisons

| A | B | Pairs | A-only | B-only | B-A | Exact McNemar p |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `binary` | `rms` | 86 | 0 | 48 | 55.8% | 0.000000 |
| `binary` | `l1_mass` | 86 | 0 | 65 | 75.6% | 0.000000 |
| `rms` | `l1_mass` | 86 | 4 | 21 | 19.8% | 0.000911 |

## Weight-design interpretation

The support matrix `W` is binary hard overlap in all three runs. Only the separate state preconditioner `P_Z` changes.

- `P_Z=1` leaves each active state coordinate unattenuated. With 9,600 state coordinates and 56 action coordinates, the state residual has about 13.09 times the expected L2 norm and 171.43 times the coefficient mass under equal per-coordinate errors. It is the clean strong-feedback stress test, but it is likely to leave the cached Jacobian's local validity region.
- `P_Z=sqrt(56/9600)` equalizes expected state/action residual L2 norms under isotropic equal-variance errors and an identity-like Jacobian. This is the most direct Euclidean/VJP normalization, but it does not account for DreamZero's anisotropic state-to-action Jacobian gain.
- `P_Z=56/9600` equalizes total coefficient mass. Under the same isotropic model its state residual L2 norm is 13.09 times weaker than the action residual, making it a conservative preconditioner. It can suppress positive feedback but may underuse reliable state evidence.

The preconditioner enters the residual once before `J^T e`, so local VJP corrections scale linearly with `P_Z`. Squared-energy arguments are useful for selecting RMS scaling, but the actual correction is controlled by the full cross-modal Jacobian, not coordinate count alone.

Five episodes per task are screening evidence. A 0/5 versus 1/5 difference is not a stable task-level estimate; suite aggregates, paired outcomes, and numerical-tail checks should drive follow-up selection.

## Warnings

- incomplete sweep: 286/300 episodes
