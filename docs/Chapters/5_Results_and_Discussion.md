# Results and Discussion

## LingBot-VA on RoboTwin

We compare the frozen LingBot-VA checkpoint with no inference-time feedback
(Base) against the same checkpoint equipped with FBFM (Ours). The final summary
uses the same selected 42-task set for both methods and reports only the
aggregate success rate under RoboTwin's clean and randomized configurations.
Task-level successes and trial counts are reserved for Appendix D.

| Method | Clean SR (%) | Randomized SR (%) |
| --- | ---: | ---: |
| LingBot-VA (Base, NONE) | -- | -- |
| LingBot-VA + FBFM (Ours) | -- | -- |

<!-- TODO(results): Fill only after all 42 tasks have matched Base/FBFM records
under both configurations. Do not use the non-matched pooled snapshot rates. -->

## DreamZero on LIBERO

We similarly compare the frozen DreamZero checkpoint with and without FBFM on
the four standard LIBERO suites used in this study. LIBERO-90 is excluded. The
two rows will be filled only from matched evaluations using the same checkpoint,
task set, reset IDs, episode horizon, and delayed pseudo-asynchronous overlap
protocol. Results from DreamZero's native synchronous rollout are not used in
this comparison. Full per-task records are maintained in Appendix D.

| Method | Spatial SR (%) | Object SR (%) | Goal SR (%) | LIBERO-10 SR (%) |
| --- | ---: | ---: | ---: | ---: |
| DreamZero (Base, NONE) | -- | -- | -- | -- |
| DreamZero + FBFM (Ours) | -- | -- | -- | -- |

<!-- TODO(results): Fill both rows only after the matched delayed
pseudo-asynchronous evaluation is complete. Keep native synchronous results and
preliminary single-task diagnostics out of this table. -->

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
| 0.0316228 | 0.000184466 | 56/80 | 70 |
| **0.0486968** | **0.000284064** | **64/80** | **80** |
| 0.0749894 | 0.000437438 | 60/80 | 75 |

The middle value is the best tested point estimate and is retained as the
operational candidate. Its paired advantage over the lower value is 10
percentage points (\(p=0.0768\), exact two-sided McNemar), while its five-point
advantage over the upper value is not significant (\(p=0.5034\)). Thus the
sweep demonstrates gain sensitivity and identifies a stable working region; it
does not establish a universal optimum. Appendix E reports the preconditioner
ablation, logarithmic search trajectory, task-level outcomes, and integrity
checks.
