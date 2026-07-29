# Results and Discussion

## LingBot-VA on RoboTwin

We compare the frozen LingBot-VA checkpoint with no inference-time feedback
(Base) against the same checkpoint equipped with FBFM (Ours). We micro-average
the recorded episode outcomes: Clean uses all 42 selected tasks, whereas
Randomized uses the 41 tasks with completed records for both methods and
excludes the unfinished `handover_block` FBFM cell. Task-level counts are
reserved for Appendix D.

| Method | Clean SR (%) | Randomized SR (%) |
| --- | ---: | ---: |
| LingBot-VA (Base, NONE) | 83.1 | 83.0 |
| LingBot-VA + FBFM (Ours) | **85.4 ↑** | **84.6 ↑** |

*The Randomized aggregate excludes `handover_block` from both methods.*

FBFM improves the pooled Clean and Randomized success rates by 2.3 and 1.7
percentage points, respectively.

## DreamZero on LIBERO

We compare the frozen DreamZero checkpoint with and without FBFM on
LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-10; LIBERO-90 is
excluded. Both evaluations use the same tasks, 20 official initial states per
task, 480-step horizon, and delayed pseudo-asynchronous overlap protocol.
DreamZero's native synchronous rollout is not used as the Base. For concision,
the main table reports all four evaluated suites and their pooled total.
Appendix D reports every task.

| Method | Spatial SR (%) | Object SR (%) | Goal SR (%) | LIBERO-10 SR (%) | Total SR (%) |
| --- | ---: | ---: | ---: | ---: | ---: |
| DreamZero (Base, NONE) | 78.5 | 73.0 | 68.5 | 60.5 | 70.125 |
| DreamZero + FBFM (Ours) | 77.0 | 72.0 | **71.0 ↑** | **63.0 ↑** | **70.750 ↑** |

*Up-arrows mark improvements over the corresponding Base result.*

FBFM improves both LIBERO-Goal and LIBERO-10 by 2.5 percentage points, while
LIBERO-Spatial and LIBERO-Object decrease by 1.5 and 1.0 points, respectively.
Across all 800 episodes, the pooled success rate increases by 0.625 points. We
therefore interpret the current result as a modest aggregate gain with
heterogeneous suite-level effects rather than a uniform improvement.

## State-Feedback Gain and Closed-Loop Stability

For a joint WAM, the two off-diagonal endpoint-Jacobian blocks couple state and
action coordinates in opposite directions. Within one local linearization, the
dimension-induced gains of these two paths may partially offset. This algebraic
possibility does not imply stable closed-loop execution, because an action also
changes the next state through the physical Markov transition rather than only
through the WAM Jacobian:

\[
\mathbf e_t^Z
\xrightarrow{\mathbf J_{ZA}^{\mathsf T}}
\Delta\mathbf A_t
\longrightarrow a_t
\xrightarrow{P(\cdot\mid s_t,a_t)}
s_{t+1}
\xrightarrow{\mathcal O,E}
z_{t+1}
\longrightarrow \mathbf e_{t+1}^Z.
\]

The environment branch is delayed, nonlinear, and generally not the inverse of
the opposite Jacobian block. We therefore balance the state residual before its
VJP using a modality preconditioner \(P_Z\), and tune a separate proportional
gain \(k_p\):

\[
\mathbf e_t^Z
=k_p P_Z\mathbf W_t^Z
(\mathbf Y_t^Z-\hat{\mathbf Z}_t^1),
\qquad P_Z=56/9600.
\]

With \(P_Z\) fixed, the final three candidates were evaluated on the same eight
LIBERO tasks and ten initial states per task. LIBERO-90 is excluded because the
checkpoint was not trained on that suite.

| \(k_p\) | Effective state weight \(k_p P_Z\) | Success | SR (%) |
| ---: | ---: | ---: | ---: |
| 0.0316 | \(1.84\times10^{-4}\) | 56/80 | 70 |
| **0.0487** | **\(2.84\times10^{-4}\)** | **64/80** | **80** |
| 0.0750 | \(4.37\times10^{-4}\) | 60/80 | 75 |

The middle value is the best tested point estimate and is retained as the
operational candidate. Its paired advantage over the lower value is 10
percentage points (\(p=0.0768\), exact two-sided McNemar), while its five-point
advantage over the upper value is not significant (\(p=0.5034\)). Thus the
sweep demonstrates gain sensitivity and identifies a stable working region; it
does not establish a universal optimum. Appendix E reports the preconditioner
ablation, logarithmic search trajectory, task-level outcomes, and integrity
checks.
