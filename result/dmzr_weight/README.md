# DreamZero FBFM State-Weight Diagnosis

This directory records the controlled A6000 diagnosis of DreamZero FBFM state
weights on one LIBERO task. The abbreviation `dmzr` means DreamZero.

It also contains the subsequent Pro6000 search that fixes the selected
L1-mass alignment weight and varies a separate proportional state-feedback gain
`kp`. See [`kp_search_pro6000/`](kp_search_pro6000/README.md) for the complete
protocol, valid trial ledgers, exclusion rule, and handoff analysis. After
excluding LIBERO-90 because the RLinf checkpoint was not trained on that suite,
the best tested point estimate is `kp=0.04869675251658631` with `64/80 = 80%`
over eight tasks. The neighboring points obtain `56/80 = 70%` and
`60/80 = 75%`; these differences are screening evidence, not a statistically
conclusive superiority claim.

## Formal LIBERO-40 Result In This Branch

[`formal_libero40_fbfm_kp00486968_20_a051933/`](formal_libero40_fbfm_kp00486968_20_a051933/README.md)
contains the complete DreamZero FBFM evaluation with `kp=0.0486968`: 40 tasks,
20 trials per task, and `566/800 = 70.75%` overall success. The directory
includes all compact episode ledgers, per-task summaries, manifests, runtime
provenance, and recovery records.

## Scope

```text
suite/task: libero_object / task_006
instruction: pick up the butter and place it in the basket
official init IDs: 0-19
checkpoint: RLinf-DreamZero-WAN2.2-5B-LIBERO-SFT-Step26000
environment seed: 0
model seed: fixed 0
horizon: 480 environment steps
hardware: NVIDIA RTX A6000 48 GB
```

The L1-mass and RMS runs differ only in the state preconditioner. Both retain
the corrected causal stride-3 feedback encoder, native 16-index UniPC schedule,
8 DreamZero DiT evaluations, native-velocity cache, and per-index residual/VJP
recomputation. This is therefore the clean weight comparison in this directory.

The A6000 native base uses `native_sync`, while FBFM uses
`pseudo_async_overlap`. It shares task, init IDs, checkpoint, seeds, and horizon,
but is not a mask-only ablation.

## Main Results

| Method | State weight | Success | 95% Wilson CI | Mean steps | Mean episode time |
| --- | ---: | ---: | ---: | ---: | ---: |
| L1-mass FBFM | `56/9600 = 0.00583333` | **8/20 (40%)** | 21.9%-61.3% | 378.95 | 116.50 s |
| RMS FBFM | `sqrt(56/9600) = 0.0763763` | 4/20 (20%) | 8.1%-41.6% | 426.85 | 131.28 s |
| A6000 native base | n/a | 5/20 (25%) | 11.2%-46.9% | 427.95 | 64.29 s |

L1 succeeds on trials `0,2,5,6,7,8,12,19`; RMS succeeds on `2,6,7,13`;
the A6000 native base succeeds on `0,6,8,13,18`.

For the clean L1-versus-RMS comparison, there are 3 joint successes, 5 L1-only
successes, 1 RMS-only success, and 11 joint failures. The two-sided exact
McNemar p-value is `0.21875`. The point estimate favors L1 by 20 percentage
points, but 20 trials on one task are not enough to claim a benchmark-level or
statistically conclusive improvement.

## Numerical Stability

| Metric | L1-mass FBFM | RMS FBFM | A6000 native base |
| --- | ---: | ---: | ---: |
| Executed actions | 7,579 | 8,537 | 8,559 |
| Action norm mean | 1.168 | 1.292 | 1.161 |
| Action norm P95 | 1.409 | 1.387 | 1.423 |
| Action norm max | **1.612** | **168.370** | 1.566 |
| Max absolute coordinate | 1.165 | 152.813 | 1.150 |
| Guided action velocity max | 68.68 | 46,455.02 | n/a |
| Action correction max | 11.27 | 11,260.61 | n/a |
| Server errors | 0 | 0 | 0 |

RMS trial 18 enters a positive-feedback block while reusing a cached Jacobian:
the action correction grows `138 -> 700 -> 2929 -> 11261` over scheduler indices
6-9, producing eight physical actions with norms above 100. L1 has no comparable
tail event across its 20 trials. Its maximum action norm remains close to the
native base.

Both FBFM runs have stable memory: L1 averages `26.003 GiB` over its first 200
solver evaluations and `26.094 GiB` over its last 200, with a `27.249 GiB`
peak. The result is not caused by retaining autograd graphs across waves.

## Interpretation

The earlier statement that `56/9600` simply made DreamZero state feedback too
weak was incomplete. That older result was confounded by causal-target,
training-stride, and guided-cache bugs. After fixing those issues:

1. `56/9600` still is 13.1 times weaker than RMS in expected Euclidean norm
   under an equal-variance, identity-Jacobian approximation.
2. DreamZero's real state-to-action Jacobian does not satisfy that approximation.
   RMS coordinate balancing can overdrive the joint solver and leave the cached
   Jacobian's local linearization domain.
3. L1 remains strong enough to alter closed-loop outcomes: it adds successes
   not present in either RMS or the A6000 native base.
4. Within this diagnostic, `56/9600` is the best tested default because it passes
   both the success-rate and action-tail gates. It is not proven globally optimal.

The action/state support matrix `W` remains binary hard overlap. The fractional
coefficient should be described as a separate modality preconditioner `P`, not
as a soft support mask.

## Critical Baseline Gap

The existing paper record at
`docs/exp_result/dreamzero_Libero_base_results.md` reports DreamZero base
`18/20 = 90%` on the same named object task 6. The A6000 `native_sync` control in
this directory obtains only `5/20 = 25%`.

These results must not be merged or used interchangeably. The current weight
comparison is internally useful because L1 and RMS share one A6000 runner, but
it is not yet externally aligned with the paper's official base evaluation.
Before using the 40% figure in the manuscript, reproduce the 90% runner on the
A6000 path or run L1/RMS FBFM inside that official evaluator. Record at least:

- exact checkpoint and tokenizer revisions;
- observation preprocessing and causal history;
- action normalization and executed chunk slice;
- model/noise seed rule;
- batching and environment reset behavior;
- rollout horizon and success termination semantics.

## Files

| File | Purpose |
| --- | --- |
| `weight_summary.csv` | Aggregate success, timing, action, and interval metrics |
| `paired_trials.csv` | Trial-level paired success labels and executed steps |
| `solver_metrics.csv` | Compact VJP, velocity, memory, and error statistics |
| `manifest.json` | Protocol, checkpoint, revisions, and source locations |
| `checksums.sha256` | Versioned ledger hashes and external solver-audit hashes |
| `DMZR_FBFM_VELOCITY_JACOBIAN.md` | Exact feedback velocity and Jacobian/VJP implementation |
| `raw/` | Direct episode and summary outputs from the A6000 runner |
| `kp_search_pro6000/` | Pro6000 logarithmic `kp` search and 240 valid episode records |

## Code Handoff

```text
repository: https://github.com/StvLi/FBFM
branch: experiment/dreamzero-l1mass-state-weight
commit: cb08c9e552730d26cc446885e79a3e270a270d0c
```

This branch changes the default to `56/9600`; the completed L1 experiment is
numerically equivalent to revision `13de791` launched with explicit
`--state-weight 0.0058333333333333336`.
