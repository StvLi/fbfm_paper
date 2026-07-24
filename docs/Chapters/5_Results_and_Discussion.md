# Results and Discussion

**DreamZero baseline on LIBERO.** We first characterize the frozen DreamZero
checkpoint before adding FBFM. The suite-level summary below covers all 800
base-model episodes.
The checkpoint succeeds in 618 episodes, corresponding to an aggregate success
rate of 77.25% and a 95% Wilson interval of \([74.22,80.02]\%\).

| Suite | Success / Trials | Success Rate | 95% Wilson CI |
| --- | ---: | ---: | ---: |
| LIBERO-Spatial | 181 / 200 | 90.50% | [85.64, 93.83]% |
| LIBERO-Object | 181 / 200 | 90.50% | [85.64, 93.83]% |
| LIBERO-Goal | 114 / 200 | 57.00% | [50.07, 63.67]% |
| LIBERO-10 | 142 / 200 | 71.00% | [64.36, 76.85]% |
| **Aggregate** | **618 / 800** | **77.25%** | **[74.22, 80.02]%** |

The aggregate masks substantial task heterogeneity. Spatial and object
generalization both reach 90.5%, whereas LIBERO-Goal falls to 57.0%; five of its
ten tasks have success rates at or below 30%. LIBERO-10 reaches 71.0%, including
one task at 10%. The base checkpoint therefore provides both ceiling-limited
tasks and tasks with considerable room for correction. Subsequent FBFM
comparisons must use the same checkpoint and reset IDs and report paired
per-task and per-suite changes; this baseline alone is not evidence for an FBFM
improvement.

<!-- TODO(results): Expand this table with the matched RTC and FBFM results.
Retain per-task paired outcomes in the appendix and report absolute
percentage-point changes with uncertainty. -->
