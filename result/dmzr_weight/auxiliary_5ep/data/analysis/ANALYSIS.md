# DreamZero FBFM Three-Weight Auxiliary Results

Verification status: `complete`; episodes: `300/300`.

## Aggregate results

| Weight | Success | Micro | 95% Wilson CI | Mean steps | Mean seconds | Action norm max | Correction max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `1` | 0/100 | 0.0% | 0.0%-3.7% | 480.0 | 148.14 | 25453960.778 | 1238662656.000 |
| `sqrt(56/9600)` | 59/100 | 59.0% | 49.2%-68.1% | 300.1 | 93.56 | 9028.948 | 469042.344 |
| `56/9600` | 73/100 | 73.0% | 63.6%-80.7% | 242.4 | 75.99 | 1.608 | 21.267 |

## Suite results

| Weight | Suite | Success | Rate | 95% Wilson CI | Mean seconds |
| --- | --- | ---: | ---: | ---: | ---: |
| `binary` | `libero_spatial` | 0/50 | 0.0% | 0.0%-7.1% | 148.92 |
| `binary` | `libero_object` | 0/50 | 0.0% | 0.0%-7.1% | 147.36 |
| `rms` | `libero_spatial` | 30/50 | 60.0% | 46.2%-72.4% | 88.39 |
| `rms` | `libero_object` | 29/50 | 58.0% | 44.2%-70.6% | 98.73 |
| `l1_mass` | `libero_spatial` | 40/50 | 80.0% | 67.0%-88.8% | 66.04 |
| `l1_mass` | `libero_object` | 33/50 | 66.0% | 52.2%-77.6% | 85.95 |

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
| `libero_object` | 7 | 0/5 | 2/5 | 0/5 |
| `libero_object` | 8 | 0/5 | 4/5 | 4/5 |
| `libero_object` | 9 | 0/5 | 5/5 | 4/5 |

## Pairwise episode comparisons

| A | B | Pairs | A-only | B-only | B-A | Exact McNemar p |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `binary` | `rms` | 100 | 0 | 59 | 59.0% | 0.000000 |
| `binary` | `l1_mass` | 100 | 0 | 73 | 73.0% | 0.000000 |
| `rms` | `l1_mass` | 100 | 7 | 21 | 14.0% | 0.012541 |

## Weight-design interpretation

The support matrix `W` is binary hard overlap in all three runs. Only the separate state preconditioner `P_Z` changes.

- `P_Z=1` leaves each active state coordinate unattenuated. With 9,600 state coordinates and 56 action coordinates, the state residual has about 13.09 times the expected L2 norm and 171.43 times the coefficient mass under equal per-coordinate errors. It is the clean strong-feedback stress test, but it is likely to leave the cached Jacobian's local validity region.
- `P_Z=sqrt(56/9600)` equalizes expected state/action residual L2 norms under isotropic equal-variance errors and an identity-like Jacobian. This is the most direct Euclidean/VJP normalization, but it does not account for DreamZero's anisotropic state-to-action Jacobian gain.
- `P_Z=56/9600` equalizes total coefficient mass. Under the same isotropic model its state residual L2 norm is 13.09 times weaker than the action residual, making it a conservative preconditioner. It can suppress positive feedback but may underuse reliable state evidence.

The preconditioner enters the residual once before `J^T e`, so local VJP corrections scale linearly with `P_Z`. Squared-energy arguments are useful for selecting RMS scaling, but the actual correction is controlled by the full cross-modal Jacobian, not coordinate count alone.

## Empirical conclusion

The results reject unattenuated binary state feedback for this DreamZero
integration: it achieves `0/100`, and its physical-action norm reaches
`25,453,960.78`. RMS scaling restores useful behavior (`59/100`) but retains a
rare unstable tail: 43 executed actions exceed norm 10, 24 exceed norm 100, and
the maximum reaches `9,028.95`. These tails show that coordinate-count L2
balancing alone does not control the anisotropic cross-modal VJP.

L1-mass scaling achieves the best result (`73/100`) and the cleanest numerical
profile: no action norm exceeds 10, its maximum action norm is `1.608`, and its
maximum action-correction norm is `21.267`. Against RMS on identical task and
initial-state pairs, it gains 21 episodes and loses seven, a net 14-point gain
with exact McNemar `p=0.01254095`. For subsequent large DreamZero FBFM sweeps,
`P_Z=56/9600` is therefore the recommended default among these three settings.

The exception pattern still matters. RMS wins on seven individual paired
episodes, including aggregate regressions on `libero_object` tasks 0, 7, and 9.
The result should be interpreted as a robust screening preference, not proof
that L1-mass scaling is optimal for every task or Jacobian regime.

## Reproducibility and integrity

- Final ledger: 300 episodes, 60 task-weight cells, exactly five official init
  IDs (`0`-`4`) per cell.
- Verification: no errors or warnings; no server errors or non-finite solver
  records for any weight.
- Code: integration revision `a37fcf5fc05147d7b9cf6a18beb70c8f991fd52f`;
  numerical-method revision `13de791f74139b165cff70ff8165b1cc4538ea64`.
- Storage: compact ledgers and summary tables are committed here. Trajectory
  arrays, logs, and solver audits remain on the A6000 and are represented by
  remote paths and checksums.

Five episodes per task are screening evidence. A 0/5 versus 1/5 difference is not a stable task-level estimate; suite aggregates, paired outcomes, and numerical-tail checks should drive follow-up selection.
