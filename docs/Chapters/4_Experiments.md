# Experiments

We evaluate FBFM in two complementary tracks that cover the two WAM generation
factorizations considered in Section 3. Comparisons are made within each track
using the same frozen base model; absolute scores are not compared across
architectures or benchmarks.

## Models, Benchmarks, and Tasks

**Models.** We instantiate FBFM on LingBot-VA and DreamZero. The LingBot-VA
track uses the official checkpoint post-trained on RoboTwin. Its released
inference implementation provides the stage-wise WAM instance, in which the
state trajectory is generated before the action trajectory. The DreamZero
track uses a LIBERO-post-trained checkpoint obtained at SFT step 26,000 with
the [RLinf DreamZero SFT
recipe](https://rlinf.readthedocs.io/zh-cn/latest/rst_source/examples/embodied/sft_dreamzero.html).
DreamZero jointly generates future states and actions and therefore provides
the joint-generation WAM instance. Together, the two tracks test whether the
same training-free feedback principle transfers across distinct WAM
factorizations rather than comparing the two base models directly.

**Benchmarks and tasks.** We evaluate the LingBot-VA track on RoboTwin and the
DreamZero track on LIBERO. The current DreamZero baseline covers all four
standard suites---LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-10---with
10 tasks per suite. Each task is evaluated once at each reset ID from 0 to 19,
giving 20 episodes per task and 800 episodes in total. Both benchmarks provide
environment-side, task-specific completion predicates. We use these native
predicates without manual relabeling: an episode is assigned \(u_{q,n}=1\) if
the benchmark reports successful completion of task \(q\), and \(u_{q,n}=0\)
otherwise. For \(N_q\) evaluation episodes, the per-task success rate is

\[
\operatorname{SR}_q=\frac{1}{N_q}\sum_{n=1}^{N_q}u_{q,n}.
\]

<!-- TODO(experiments): Complete the RoboTwin task/protocol record and add the
exact artifact identifier for the DreamZero step-26,000 checkpoint. -->

## FBFM Instantiations

For both tracks, FBFM is inserted only at inference time. We retain the
checkpoint, native solver and cache schedule, classifier-free guidance, and
chunk dimensions of each WAM, with all pretrained parameters frozen. A
deterministic pseudo-asynchronous clock couples environment transitions to
solver evaluations, controlling feedback timing independently of wall-clock
latency.

**Stage-wise generation: LingBot-VA.** We preserve the released video-first,
action-second inference order. While the preceding action suffix is executed,
frozen-VAE observations update time-aligned constraints in the active video
flow. The corrected video context then conditions action generation, while the
same preceding suffix provides a fixed action-prefix constraint.

**Joint generation: DreamZero.** We retain DreamZero's joint state--action
solver. Guidance is recomputed at all 16 UniPC updates, whereas the native DiT
velocity and endpoint Jacobian are refreshed at eight DiT evaluations. Skipped
DiT indices reuse only the latest native velocity and Jacobian; their endpoint,
residual, VJP, and guided field are evaluated from the current solver sample.
Joint differentiation preserves the cross-modal Jacobian blocks through which
state feedback can directly correct action coordinates. Every execution
observation is retained in causal order, but the hard state target is refreshed
only at the checkpoint's three-action video stride. The preceding actions
remain a fixed prefix target throughout the active chunk.

| Setting | LingBot-VA | DreamZero |
|---|---:|---:|
| Generation factorization | Stage-wise | Joint |
| \((H,d,s)\) | \((32,16,16)\) | \((16,8,8)\) |
| Predicted state slots | 2 | 2 |
| Guided updates / Jacobian refreshes | 25 state / 50 action | 16 UniPC / 8 DiT--\(J\) |
| Pseudo-clock release | 26 video calls / 16 actions | 8 DiT blocks / 8 actions |
| State-target refresh | 4 sampled observations / latent | Every 3 actions (training stride) |
| State preconditioner | \(1\) | \(P_Z=56/9600\) |
| Guidance clip \(\beta\) | 10 | 10 |
| Precision | BF16 | BF16 |

*The LingBot-VA pseudo-clock count includes its final cache-only video call.*

The implementation exposes a common mask-controlled path for later controlled
comparisons. Within each architecture, the unguided, action-only, and full FBFM
modes share the checkpoint, noise, solver budget, and pseudo-clock, differing
only in their active masks. DreamZero's native synchronous rollout is recorded
separately. Appendix C provides tensor alignment, cache separation, rolling
encoding, and exact solver schedules.

## Baselines and Ablations

<!-- TODO(experiments): Leave this subsection blank until the baseline and
ablation design has been agreed with the experiment team. -->
