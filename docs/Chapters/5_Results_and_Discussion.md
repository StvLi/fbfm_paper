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
percentage points, respectively. Because the checkpoint, task predicates,
solver budget, and execution protocol are held fixed, this comparison isolates
the effect of inference-time feedback under the evaluated protocol.

## LingBot-VA Mechanism Analysis

The following figure evaluates the two internal links isolated by the auxiliary
diagnostic. Across four paired task--trial units, FBFM lowers the wave-0
next-state latent MSE from 0.6828 to 0.6751 (1.13%). Switching only the
installed RTC versus FBFM cache changes the normalized fresh action by RMS
0.00890, 7.39x the same-cache repeat floor. The corresponding velocity
difference remains above that floor throughout all 51 action-solver steps and
has a 2.52x AUC ratio. Together, these observations trace the intended path
from state feedback to latent prediction, flow velocity, and final action.
Because the diagnostic contains four independent units, it is mechanism
evidence rather than a task-success claim.

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
is reused across multiple solver updates. FBFM recomputes its residual from the
current \(\mathbf Z\) and \(\mathbf A\), but reuses the latest native velocity
and endpoint Jacobian between DiT evaluations; this amortization can damp or
delay new corrections. Joint feedback is also sensitive to the relative scale
of its state and action residuals. We therefore use modality preconditioning
and a separately calibrated proportional gain. Appendix E contains the
closed-loop motivation, configuration search, and task-level sensitivity
analysis; the selected value is an operational setting rather than a universal
optimum.

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
