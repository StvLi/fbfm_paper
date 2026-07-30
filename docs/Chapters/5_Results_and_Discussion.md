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
| Base | 83.1 | 83.0 |
| FBFM | **85.4 ↑** | **84.6 ↑** |

*The Randomized aggregate excludes `handover_block` from both methods.*

FBFM improves the pooled Clean and Randomized success rates by 2.3 and 1.7
percentage points, respectively. Since the checkpoint, task predicates, solver
budget, and execution protocol are held fixed, the improvement is attributable
to the inference-time feedback mechanism itself rather than additional
training or a stronger base policy.

## LingBot-VA Mechanism Analysis

The following figure evaluates the two internal links isolated by the
auxiliary diagnostic. Across all four paired task--trial units, FBFM reduces
the wave-0 next-state latent MSE, lowering the mean from 0.6828 to 0.6751
(1.13%). This verifies that masked feedback changes the latent state prediction
in the intended direction. Switching only the installed RTC versus FBFM cache
then changes the normalized fresh action by RMS 0.00890, compared with a
same-cache repeat floor of 0.001205, a 7.39x ratio, showing that the refreshed
latent state context propagates to the final action prediction. The
cache-switch velocity also remains above the mean repeat floor at all 51
action-solver steps, with a 2.52x AUC ratio; the action difference is therefore
introduced through the flow-matching velocity field rather than appearing only
as a terminal decoding artifact. These results support the computation-level
path from encoded state feedback through the refreshed cache to action
generation; with only four independent units, they are mechanism evidence
rather than a task-success claim.

![LingBot-VA mechanism diagnostic. Panel (a) reports paired wave-0 next-state
latent MSE; panel (b) compares fresh-action RMS under a same-cache repeat and an
RTC--FBFM cache switch; panel (c) follows both velocity signals across 51 action
solver steps.](../../material/lbva_aux_mechanism_main.jpg)

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
| Base | 78.5 | 73.0 | 68.5 | 60.5 | 70.1 |
| FBFM | 77.0 | 72.0 | **71.0 ↑** | **63.0 ↑** | **70.8 ↑** |

*Up-arrows mark improvements over the corresponding Base result.*

FBFM improves both LIBERO-Goal and LIBERO-10 by 2.5 percentage points, while
LIBERO-Spatial and LIBERO-Object decrease by 1.5 and 1.0 points, respectively.
Across all 800 episodes, the pooled success rate increases by 0.625 points. We
therefore interpret the current result as a modest aggregate gain with
heterogeneous suite-level effects rather than a uniform improvement. A likely
reason is DreamZero's accelerated inference design: one native model evaluation
is reused across multiple Euler-style solver updates. Our implementation keeps
this schedule and recomputes FBFM residuals from the newest \(\mathbf Z\) and
\(\mathbf A\), but it must reuse the latest native velocity and endpoint
Jacobian between refreshed DiT evaluations. This amortization preserves
DreamZero's fast execution but can damp or delay the corrective effect of newly
arrived feedback.

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
the opposite Jacobian block; an over-large state correction can therefore make
the physical feedback loop unstable even when the local Jacobian terms look
scale-balanced. We therefore balance the state residual before its VJP using a
modality preconditioner \(P_Z\), and tune a separate proportional gain \(k_p\):

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

We retain the middle value, which attained the highest tested success rate
(80%). Its 10-point gain over the lower value was marginal (\(p=0.0768\), exact
two-sided McNemar), and its five-point gain over the upper value was not
significant (\(p=0.5034\)). Thus this sweep shows gain sensitivity, not a
universal optimum; Appendix E gives the full search and task-level results.

## Real-World Robot Observation Prediction

The following figure reports the recorded physical robot-arm ball-stopping
experiment described above. Both methods start from the same image at the end
of a two-second context and predict the same five-second, 121-frame horizon.
The Base receives no later image, whereas FBFM causally incorporates all 120
measured future RealSense frames as 30 latent feedback slots. Base preserves a
coherent robot and tabletop but departs from the recorded ball evolution. FBFM
moves the full-frame prediction closer to the reference (MAE 9.63 to 9.27 and
PSNR 20.06 to 23.10 dB) and better preserves task-relevant physical information
such as the ball position over time, even though visual artifacts remain. This
shows that FBFM can use observations recorded from a physical robot task to
constrain the active frame chunk beyond pure open-loop prediction. Appendix F
separately analyzes the behavior observed when state feedback covers only a
limited prefix of the generated video and treats the resulting large-area
artifacts as a Wan2.2-specific codec/backbone mismatch hypothesis.

![Real-world robot-arm ball-stopping observation prediction. The RGB sequence
was recorded from a physical robot task with a RealSense D435i. Columns show 0,
0.25, 0.5, 1, 2, 3, 4, and 5 s; rows show the recorded reference, Wan2.2 Base
without feedback, and FBFM using all 30 measured latent slots.](../../material/wan2.2/robot_arm_ball_stop_keyframes.jpg)
