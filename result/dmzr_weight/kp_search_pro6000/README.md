# DreamZero FBFM State-Feedback Gain Search

This directory records the 2026-07-27 logarithmic search for the proportional
state-feedback gain `kp` on the RTX PRO 6000 workstation. The state alignment
weight remains fixed at the interpretable L1-mass coefficient

```text
state_weight = 56/9600 = 0.005833333333333334
effective_state_weight = state_weight * kp
```

`kp` scales only the aligned state-feedback residual. It does not alter the
binary action-overlap support, action residual, checkpoint, scheduler, or
rollout protocol.

## Valid Evaluation Scope

The final analysis contains only suites covered by the RLinf DreamZero LIBERO
training distribution:

```text
libero_spatial: tasks 1 and 9
libero_object:  tasks 0 and 6
libero_goal:    tasks 0 and 6
libero_10:      tasks 0 and 6
official init/trial IDs: 0-9
```

This gives 8 tasks x 10 episodes = 80 valid episodes per `kp`, or 240 valid
episodes in total. The execution plan initially included LIBERO-90 tasks 0 and
6, but the RLinf checkpoint was not trained on LIBERO-90. All 60 LIBERO-90
episodes are therefore excluded from every rate, ranking, comparison, and
committed trial ledger in this directory. They must not be restored when these
tables are used in the paper.

## Search Procedure

The search interval was `[0.001, 100]` on a logarithmic scale. The initial
points were `0.001`, `1`, and `100`; later points were geometric midpoints,

```text
next_kp = sqrt(lower_kp * upper_kp).
```

Each newly evaluated screening point used the same four tasks (spatial 1 and 9;
object 0 and 6) and five official init IDs per task. The `kp=1` point reused the
matching L1-mass rows from the earlier A6000 auxiliary sweep, so it is a
historical control rather than a same-machine rerun.

| Order | `kp` | Success | Rate | Role |
| ---: | ---: | ---: | ---: | --- |
| 1 | `0.001` | 11/20 | 55% | initial lower endpoint |
| 2 | `1` | 13/20 | 65% | historical A6000 control |
| 3 | `100` | 0/20 | 0% | initial upper endpoint |
| 4 | `0.0316227766` | 16/20 | 80% | geometric refinement |
| 5 | `0.1778279410` | 12/20 | 60% | geometric refinement |
| 6 | `0.0749894209` | 14/20 | 70% | geometric refinement |
| 7 | `0.0486967525` | 16/20 | 80% | geometric refinement |

The three best completed screening points were expanded. The planned
`0.0392418976` midpoint was not run after the protocol changed to a broader
comparison of the top three points; it is not an experimental result.

## Final Valid Results

| `kp` | Effective state weight | Spatial | Object | Goal | LIBERO-10 | Total | 95% Wilson CI |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.0316227766` | `0.000184466197` | 15/20 | 15/20 | 14/20 | 12/20 | 56/80 (70%) | 59.2%-78.9% |
| **`0.0486967525`** | **`0.000284064390`** | **17/20** | **17/20** | **16/20** | **14/20** | **64/80 (80%)** | **70.0%-87.3%** |
| `0.0749894209` | `0.000437438289` | 17/20 | 15/20 | 16/20 | 12/20 | 60/80 (75%) | 64.5%-83.2% |

Per-task outcomes are:

| Suite | Task | `kp=0.0316228` | `kp=0.0486968` | `kp=0.0749894` |
| --- | ---: | ---: | ---: | ---: |
| `libero_spatial` | 1 | 8/10 | 9/10 | 9/10 |
| `libero_spatial` | 9 | 7/10 | 8/10 | 8/10 |
| `libero_object` | 0 | 9/10 | 9/10 | 8/10 |
| `libero_object` | 6 | 6/10 | 8/10 | 7/10 |
| `libero_goal` | 0 | 8/10 | 9/10 | 9/10 |
| `libero_goal` | 6 | 6/10 | 7/10 | 7/10 |
| `libero_10` | 0 | 4/10 | 7/10 | 6/10 |
| `libero_10` | 6 | 8/10 | 7/10 | 6/10 |

The best point estimate is `kp=0.04869675251658631`. Relative to
`kp=0.03162277660168379`, it gains 12 paired episodes and loses four; the exact
two-sided McNemar p-value is `0.076812744`. Relative to
`kp=0.07498942093324558`, it gains 12 and loses eight (`p=0.503444672`). The
80-episode sweep supports `kp=0.04869675251658631` as the operational candidate
for the larger evaluation, but the pairwise differences are not statistically
conclusive at the 0.05 level.

## Integrity Checks

- Each candidate has exactly 80 eligible rows: eight task cells and continuous,
  unique trial IDs `0`-`9` in every cell.
- All 240 valid trial records report finite executed actions.
- Direct inspection of all committed valid trajectory sources found finite
  actions. Maximum physical-action L2 norms were `1.718534`, `1.655287`, and
  `1.647330` in ascending `kp` order.
- All three benchmark services exited successfully. No server error lines were
  observed during the runs.
- The first 20 episodes of every expanded candidate are exact reuse of the
  corresponding screening rows (four screening tasks x five trials). No reused
  episode was rerun or double-counted.

## Reproducibility

```text
checkpoint: RLinf-DreamZero-WAN2.2-5B-LIBERO-SFT-Step26000
hardware: NVIDIA RTX PRO 6000 Blackwell Workstation Edition
environment seed: 0
model seed rule: fixed (seed 0)
maximum environment steps: 480
rollout protocol: pseudo_async_overlap
action horizon: 16
inference delay / executed suffix: 8 / 8
scheduler steps / DiT evaluations: 16 / 8
solver release policy: uniform
feedback encoding: training-aligned stride-3 prefix
```

The run manifests identify the launch tree as
`0f2cc4f-dirty-fc420bc56cf5` for the expanded runs. The `kp` implementation and
search configuration were subsequently standardized and pushed to the FBFM
branch at commit `a051933e2b058d74bb268e94080464569d99ce39`:

```text
repository: https://github.com/StvLi/FBFM
branch: experiment/dreamzero-l1mass-state-weight
```

## Files

| File | Purpose |
| --- | --- |
| `protocol.json` | Search, rollout, eligibility, reuse, and source revisions |
| `screening_summary.csv` | Ordered screening points and aggregate outcomes |
| `screening_task_summary.csv` | Four-task screening breakdown |
| `valid_weight_summary.csv` | Eligible aggregate rates, intervals, timing, and action checks |
| `valid_suite_summary.csv` | Eligible suite-level outcomes |
| `valid_task_matrix.csv` | Eligible task-level comparison matrix |
| `paired_comparison.csv` | Paired outcome counts and exact McNemar tests |
| `verification.json` | Machine-readable integrity and exclusion report |
| `data/*/trials.csv` | Compact 80-row valid trial ledger for each candidate |
| `data/*/task_summary.csv` | Original eight-task summaries for each candidate |
| `ledger_checksums.sha256` | Hashes of the committed, eligibility-filtered ledgers |
| `source_checksums.sha256` | Hashes of the full source ledgers before eligibility filtering |

Trajectories and solver audits remain in the Pro6000 experiment workspace under
`FBFM-a6000/results/kp_search_pro6000`. The committed ledgers intentionally
contain no LIBERO-90 rows.
