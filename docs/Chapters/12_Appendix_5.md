# Appendix E: DreamZero State-Feedback Gain Search

## Parameterization and Stability Motivation

DreamZero applies state and action constraints inside one joint solver. The
state residual used by the VJP is

\[
\mathbf e_j^Z
=k_p P_Z\mathbf W_j^Z
(\mathbf Y_j^Z-\hat{\mathbf Z}_j^1),
\]

where the binary support \(\mathbf W_j^Z\), modality preconditioner \(P_Z\), and
proportional gain \(k_p\) have distinct roles. The support selects measured
coordinates, \(P_Z\) balances the 9,600 active state coordinates against 56
active action coordinates, and \(k_p\) controls the remaining state-feedback
loop gain. Neither \(P_Z\) nor \(k_p\) changes the action-overlap residual.

The off-diagonal blocks of the local joint endpoint Jacobian can transmit
corrections in both directions and may partially compensate dimensional scale
differences. They do not include the generally nonlinear physical transition
\(P(s_{t+1}\mid s_t,a_t)\). Consequently, reciprocal scaling inside one solver
linearization does not guarantee stability after actions are executed and their
consequences return as later state measurements.

## State-Preconditioner Screening

We first compared three values of \(P_Z\) while leaving the binary support mask
unchanged. The controlled sweep used the ten LIBERO-Spatial and ten
LIBERO-Object tasks, official initial-state IDs 0--4, and the same A6000,
checkpoint, solver, and pseudo-asynchronous protocol for all settings. This
gives 100 episodes per setting and 300 episodes in total.

| State preconditioner \(P_Z\) | Interpretation | Success | Max action norm |
| ---: | --- | ---: | ---: |
| \(1\) | Unattenuated state residual | 0/100 (0%) | \(2.55\times10^7\) |
| \(\sqrt{56/9600}\) | RMS coordinate balance | 59/100 (59%) | \(9.03\times10^3\) |
| \(56/9600\) | L1 coefficient-mass balance | 73/100 (73%) | 1.608 |

On the 100 paired initial states, L1-mass scaling gains 21 successes over RMS
and loses seven (exact two-sided McNemar \(p=0.01254\)). The unattenuated and
RMS settings also exhibit large action-norm tails. We therefore fix
\(P_Z=56/9600\) for the subsequent gain search. This is an empirical
preconditioner selection, not a general stability proof.

## Logarithmic Screening of \(k_p\)

The proportional gain was searched over \([0.001,100]\) on a logarithmic scale.
The initial points were \(0.001\), \(1\), and \(100\); subsequent candidates
were geometric midpoints of the active interval. Each new screening point used
LIBERO-Spatial tasks 1 and 9, LIBERO-Object tasks 0 and 6, and official
initial-state IDs 0--4. The \(k_p=1\) row reuses a matching historical A6000
control and was not rerun on the Pro6000. The planned point \(0.0392419\) was
not executed and is not reported as a result.

| Order | \(k_p\) | Spatial 1 | Spatial 9 | Object 0 | Object 6 | Total | Source |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 0.001 | 3/5 | 4/5 | 2/5 | 2/5 | 11/20 (55%) | Pro6000 |
| 2 | 1 | 5/5 | 3/5 | 3/5 | 2/5 | 13/20 (65%) | Historical A6000 |
| 3 | 100 | 0/5 | 0/5 | 0/5 | 0/5 | 0/20 (0%) | Pro6000 |
| 4 | 0.0316228 | 5/5 | 4/5 | 5/5 | 2/5 | 16/20 (80%) | Pro6000 |
| 5 | 0.177828 | 5/5 | 4/5 | 1/5 | 2/5 | 12/20 (60%) | Pro6000 |
| 6 | 0.0749894 | 4/5 | 4/5 | 3/5 | 3/5 | 14/20 (70%) | Pro6000 |
| 7 | 0.0486968 | 4/5 | 4/5 | 4/5 | 4/5 | 16/20 (80%) | Pro6000 |

These screening rates are used only to choose candidates for expansion. In
particular, the historical \(k_p=1\) control is not used for same-machine
ranking.

## Expanded Paired Comparison

The three selected candidates were expanded to eight eligible tasks with ten
official initial states per task. The first five trials of the four screening
tasks are exact reuse of the corresponding screening records; they were not
rerun or counted twice.

| Suite | Task | \(k_p=0.0316228\) | \(k_p=0.0486968\) | \(k_p=0.0749894\) |
| --- | ---: | ---: | ---: | ---: |
| LIBERO-Spatial | 1 | 8/10 | 9/10 | 9/10 |
| LIBERO-Spatial | 9 | 7/10 | 8/10 | 8/10 |
| LIBERO-Object | 0 | 9/10 | 9/10 | 8/10 |
| LIBERO-Object | 6 | 6/10 | 8/10 | 7/10 |
| LIBERO-Goal | 0 | 8/10 | 9/10 | 9/10 |
| LIBERO-Goal | 6 | 6/10 | 7/10 | 7/10 |
| LIBERO-10 | 0 | 4/10 | 7/10 | 6/10 |
| LIBERO-10 | 6 | 8/10 | 7/10 | 6/10 |
| **Total** | -- | **56/80 (70%)** | **64/80 (80%)** | **60/80 (75%)** |

| \(k_{p,a}\) | \(k_{p,b}\) | \(a\)-only | \(b\)-only | \(b-a\) | Exact McNemar \(p\) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.0316228 | 0.0486968 | 4 | 12 | +10 points | 0.0768 |
| 0.0316228 | 0.0749894 | 9 | 13 | +5 points | 0.5235 |
| 0.0486968 | 0.0749894 | 12 | 8 | -5 points | 0.5034 |

The middle gain is the best tested point estimate, but neither paired
comparison establishes statistical superiority at the 0.05 level. It is
therefore selected as an operational candidate rather than a universal optimum.

## Eligibility and Integrity

The expanded analysis includes LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and
LIBERO-10. LIBERO-90 tasks 0 and 6 were executed during expansion but all 60
episodes are excluded because the RLinf checkpoint was not trained on that
suite. Each retained candidate has exactly 80 unique trial records. All 240
retained episodes contain finite executed actions, with maximum action L2 norms
of 1.719, 1.655, and 1.647 in ascending gain order; no benchmark-service or
server error was recorded.

The expanded run manifests record revision `0f2cc4f-dirty-fc420bc56cf5`. The
gain implementation and search configuration were subsequently standardized at
FBFM commit `a051933e2b058d74bb268e94080464569d99ce39`. The complete filtered
ledgers, source hashes, and verification report are retained under
`result/dmzr_weight/kp_search_pro6000/`.
