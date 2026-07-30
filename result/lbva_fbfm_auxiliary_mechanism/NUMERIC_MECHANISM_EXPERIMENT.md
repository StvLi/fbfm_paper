# Numeric mechanism experiment: feedback-conditioned state and action

## Status and claim boundary

This analysis is complete. It reuses the frozen `rapid_paper_2x2` outputs and
does not add RoboTwin episodes. The independent unit is one `task x trial`
pair. There are four units: two tasks (`adjust_bottle` and
`pick_diverse_bottles`) and trials 20-21. The two CacheCut probes within each
unit are repeated measurements, not independent samples.

The evidence addresses two computation-level arrows:

1. `feedback -> predicted state`: compare the RTC and FBFM wave-0 next-state
   latent predictions with the state realized at wave 1 in each method's own
   rollout.
2. `predicted state/cache -> action`: hold real history, random noise, action
   constraints, and solver schedule fixed, switch only the RTC versus FBFM
   cache branch, and measure the resulting fresh-action difference against a
   same-branch repeat floor.

The analysis does not test `action -> episode success`. In the rapid pilot,
RTC, FBFM, and FBFM-CacheCut all achieved 3/4 successes (75%), so there is no
success-level mediation result to claim.

## Frozen inputs

| Field | Value |
|---|---|
| Rapid profile | 2 tasks x 2 trials x 3 methods |
| Independent units | 4 `task x trial` pairs |
| Mechanism probes | 8, two per independent unit |
| Method worktree commit | `5b6868cdf981dd7a019bcba7186c1b540e3d1cee` |
| Rapid protocol SHA256 | `27beb50db0ecd281a866fa8adce63ff1aa48ae21d3ff7f50e9b6ddc9e0c9e26f` |
| Added rollout episodes | 0 |

The exact result-file and metric-file SHA256 digests are recorded in
`aggregate/numeric_summary.json`; all derived artifacts are covered by
`artifact_manifest.json`.

## Arrow 1: feedback to predicted state

### Primary metric

For method `m` and paired unit `u`, let `z_pred(m,u)` be temporal slot 1 from
the saved final wave-0 latent and let `z_real(m,u)` be temporal slot 0 from the
next wave. The server represents one state slot as 23,040 values in its
standardized VAE latent space. The primary error is

```text
MSE(m,u) = mean((z_pred(m,u) - z_real(m,u))^2).
```

This is the same tensor comparison recorded online by the server under
`realized_future_from_previous_wave`. Offline tensor hashes match the online
source and target hashes for all 8 method records, and the recomputed values
match the online MSE exactly.

Wave 0 is the primary comparison because RTC and FBFM begin with paired task,
trial, simulator seed, prompt, and initial history. Each method is scored
against its own actual next state, rather than incorrectly borrowing a target
from a different rollout. Because the two methods may execute different
actions, this is a paired-initial-condition comparison, not a shared-target
comparison.

### Paired results

| Task | Trial | RTC MSE | FBFM MSE | Relative reduction | RTC cosine | FBFM cosine |
|---|---:|---:|---:|---:|---:|---:|
| `adjust_bottle` | 20 | 0.855469 | 0.854743 | 0.08% | 0.409147 | 0.411239 |
| `adjust_bottle` | 21 | 0.745658 | 0.728860 | 2.25% | 0.485218 | 0.494900 |
| `pick_diverse_bottles` | 20 | 0.534707 | 0.526566 | 1.52% | 0.645741 | 0.650550 |
| `pick_diverse_bottles` | 21 | 0.595501 | 0.590426 | 0.85% | 0.559356 | 0.563812 |
| **Mean** | | **0.682834** | **0.675149** | **1.13%** | **0.524866** | **0.530125** |

FBFM has lower latent MSE and higher cosine similarity in 4/4 paired units.
The mean absolute MSE reduction is 0.007685. The exact two-sided paired sign
test is `p = 0.125`; with only four independent units this is directionally
consistent evidence, not a population-level significance result. An
enumerated unit bootstrap is retained in the JSON for audit, but is not used
as inferential evidence because `n = 4` is too small.

The main plot is `figures/state_mse_paired.{png,pdf}`.

### Time trend and representation sensitivity

The saved model latent has only two temporal slots: current state and one
predicted state. It therefore cannot support an honest latent horizon-1-to-4
curve from a single wave. Two complementary views are reported instead:

- `figures/one_step_latent_trend.{png,pdf}` plots the one-step latent error at
  each available source wave. FBFM is lower in 34/44 matched unit-wave rows,
  with mean `RTC - FBFM = 0.001234`. Only the four wave-0 rows are strict
  paired-initial-condition evidence. After wave 0 the methods have different
  action/history trajectories, and the number of available units falls from 4
  to 3 and then 1, so those rows are descriptive repeated measurements only.
- `figures/rgb_frame_horizon_sensitivity.{png,pdf}` decodes the four RGB
  frames represented by the next-state slot and compares them with the saved
  three-camera observations. Cameras are averaged equally within a unit.

The RGB sensitivity result does not reinforce the latent result:

| Frame in next slot | RTC RGB MSE | FBFM RGB MSE |
|---:|---:|---:|
| 1 | 0.023116 | 0.023765 |
| 2 | 0.024366 | 0.024893 |
| 3 | 0.028475 | 0.028766 |
| 4 | 0.036243 | 0.036606 |

FBFM is lower in only 6/16 unit-frame comparisons. Thus the defensible claim
is specifically that FBFM is more consistent with the realized next state in
the model's encoded latent representation. The current data do not establish
better pixel reconstruction. This negative sensitivity check is retained to
avoid selecting only a favorable metric.

## Arrow 2: predicted state/cache to action

### Controlled intervention

Each FBFM-CacheCut probe generates fresh actions twice from the same inference
context: once with the RTC cache branch and once with the FBFM cache branch.
The real-history cache, video noise, action noise, action constraints, and
solver schedule hashes are invariant. A third pass repeats the selected RTC
branch under the same inputs. The metrics are:

```text
D_action = RMS(action_RTC_cache - action_FBFM_cache)
D_repeat = RMS(action_RTC_cache - repeated_action_RTC_cache)
```

Both are evaluated over the explicit fresh-action mask: 256 normalized action
values per probe. `D_repeat` is the numerical repeat floor, not an independent
method. CacheCut records two probes per unit, for 8 probes total; aggregation
first averages the two probes inside each unit and then averages the four
units.

### Final-action results

| Task | Trial | Cache-branch action RMS | Repeat-floor RMS | Ratio |
|---|---:|---:|---:|---:|
| `adjust_bottle` | 20 | 0.004131 | 0.000846 | 4.88x |
| `adjust_bottle` | 21 | 0.007675 | 0.001228 | 6.25x |
| `pick_diverse_bottles` | 20 | 0.011692 | 0.001485 | 7.87x |
| `pick_diverse_bottles` | 21 | 0.012102 | 0.001261 | 9.59x |
| **Mean** | | **0.008900** | **0.001205** | **7.39x** |

The 7.39x value is a ratio of mean normalized RMS values. It means that
changing only the cache branch moves the computed fresh action 7.39 times as
far as rerunning the selected branch under identical inputs. It is evidence
that the cache affects action computation above repeat-level numerical error;
it is not a claim that task success improves by 7.39x.

### Action denoising trajectory

The saved `velocity_differences` are 51 action diffusion/flow solver steps,
not 51 future robot-control timesteps. After clustering the two probes within
each independent unit:

| Quantity | Cache branch | Repeat floor | Ratio |
|---|---:|---:|---:|
| Solver-curve AUC | 0.894198 | 0.354747 | 2.52x |
| Steps where mean cache signal is larger | 51/51 | | |
| Peak mean cache-branch velocity RMS | 0.102444 at step 49 | | |

The full curve is `figures/action_denoising_curve.{png,pdf}`. It shows that
the cache intervention changes the action model throughout the inference
trajectory, rather than appearing only as a final rounding artifact.

### Why no ground-truth-cache oracle is reported

The frozen outputs contain realized observation latents, the installed RTC
and FBFM cache hashes, final selected actions, and the paired branch-difference
metrics. They do not contain a teacher-forced action K/V cache constructed
from the realized future observation. That cache is not interchangeable with
the saved VAE observation latent, and reconstructing it would require a new
server inference path whose initial causal VAE seed observation was not saved
as a byte-identical standalone tensor. Such a replay would no longer be a
pure offline measurement of the frozen probes. Therefore a GT-cache oracle is
not fabricated from incompatible representations. The controlled RTC/FBFM
cache switch plus same-branch repeat floor is the strongest valid second-arrow
test available from the existing cache.

## Conclusion

The smallest defensible conclusion from the existing cache is:

> In four paired task-by-trial units, FBFM reduced next-wave normalized latent
> MSE from 0.6828 to 0.6751 (1.13%) and improved latent cosine similarity from
> 0.5249 to 0.5301, with the favorable direction in all four units. In eight
> controlled cache probes clustered into the same four units, switching RTC
> versus FBFM cache conditioning changed fresh actions by normalized RMS
> 0.00890, compared with a same-branch repeat floor of 0.001205 (7.39x). The
> cache-conditioned action-model velocity difference remained above the repeat
> floor at all 51 denoising steps (AUC ratio 2.52x). These results support the
> computation-level chain `feedback -> encoded next-state estimate -> fresh
> action`, while the small sample, negative RGB sensitivity check, and equal
> 75% episode success rates preclude a broader performance or mediation claim.

## Reproduction

Run from the LingBot-VA worktree with the frozen rapid directory as
`RAPID_ROOT` and this directory as `NUMERIC_ROOT`:

```bash
python "$NUMERIC_ROOT/control/compute_state_metrics.py" \
  --rapid-root "$RAPID_ROOT" \
  --model-root /mnt/project_eai_hs/zrm/lingbot-va/checkpoints/lingbot-va-posttrain-robotwin \
  --output-root "$NUMERIC_ROOT/aggregate" \
  --device cuda:0

python "$NUMERIC_ROOT/control/analyze_numeric_mechanism.py" \
  --rapid-root "$RAPID_ROOT" \
  --numeric-root "$NUMERIC_ROOT"
```

The first command loads the VAE only to produce the RGB sensitivity check; the
strict latent metric is cross-checked against the server's frozen online
metric and hashes. The second command is offline aggregation and plotting.

Key machine-readable outputs:

| Artifact | Contents |
|---|---|
| `aggregate/paired_next_slot_latent_mse.csv` | Strict wave-0 state rows |
| `aggregate/state_pair_differences.csv` | Paired RTC-FBFM differences |
| `aggregate/one_step_latent_by_wave.csv` | Descriptive one-step wave rows |
| `aggregate/action_probe_metrics.csv` | Eight final-action probe metrics |
| `aggregate/action_denoising_curve.csv` | Unit-clustered 51-step curve |
| `aggregate/numeric_summary.json` | All headline values and source hashes |
| `artifact_manifest.json` | Size and SHA256 for every derived artifact |
