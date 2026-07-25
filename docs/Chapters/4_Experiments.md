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
chunk dimensions of each WAM; all pretrained parameters remain frozen. The
environment and model server are coupled by a deterministic pseudo-asynchronous
clock: executing one part of the preceding chunk releases a prescribed number
of solver evaluations for the active chunk. This controls the relative timing
of feedback across compared modes without conflating the method with
machine-dependent wall-clock latency.

**Stage-wise generation: LingBot-VA.** We preserve the released video-first,
action-second inference order. Each chunk contains two predicted video-latent
slots and 32 low-level actions, with inference-delay and execution horizons
\(d=s=16\). While the 16-action suffix of the preceding chunk is executed in
RoboTwin, observations from the three cameras are encoded by the frozen
streaming VAE and inserted into time-aligned slots of the active video flow.
The state target and mask are versioned, and each video-solver evaluation uses
the latest available version. We use 25 numerical video-flow updates and 50
numerical action-flow updates, retaining LingBot-VA's final cache-only call in
each stage.

The corrected video trajectory is then supplied through LingBot-VA's native
prediction context to the action stage. Independently, the preceding action
suffix is mapped back to the checkpoint's normalized coordinates and imposed
as a fixed prefix target on the new action flow. State feedback therefore
reaches the action prediction through the corrected intermediate state
context, whereas action continuity is constrained directly in action
coordinates. No backbone, encoder, or decoder weights are updated.

**Joint generation: DreamZero.** We retain DreamZero's joint state--action
solver and apply one endpoint VJP to the concatenated flow variables at each
native DiT evaluation. The state and action discrepancies are differentiated
together with respect to both noisy inputs. Consequently, the cross-modal
blocks of the clean-endpoint Jacobian are preserved, allowing an observed
state residual to correct action coordinates directly rather than only through
a subsequent generation stage.

DreamZero predicts \(H=16\) actions and two future latent slots. We set
\(d=s=8\), preserve its 16-step UniPC schedule and eight native DiT
evaluations, and release one DiT evaluation after each executed action. Each
new observation refreshes a causal target for the first future latent slot;
incomplete four-frame encoder windows are completed by holding the latest
observation forward until the full window becomes available. The fixed action
constraint covers the first \(8\times7=56\) valid action coordinates. We set
the state-mask weight to \(56/9600\), balancing its aggregate coordinate weight
with the active action block, and clip the guidance coefficient at
\(\beta=10\). Appendix C gives the tensor alignment, rolling encoder, cache
separation, and exact schedules for both instantiations.

The implementation exposes a common mask-controlled path for later controlled
comparisons: the unguided mode zeros both masks, the action-only mode retains
only the preceding-action mask, and full FBFM activates both the action and
dynamic state masks. Within each architecture, these modes share the same
checkpoint, noise initialization, solver budget, and pseudo-clock. DreamZero's
native synchronous rollout is recorded separately from this matched
pseudo-asynchronous unguided control.

## Baselines and Ablations

<!-- TODO(experiments): Leave this subsection blank until the baseline and
ablation design has been agreed with the experiment team. -->
