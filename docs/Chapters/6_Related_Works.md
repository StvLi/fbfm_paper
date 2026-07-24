# Related Works

<!-- Theme 1: Generative modeling and world models. -->

Diffusion and Flow Matching established iterative transport as a general interface
for structured generation. Diffusion models learn to reverse progressive data
corruption; DDIM and score-SDE formulations subsequently connected their samplers
to deterministic and continuous-time probability dynamics
[Sohl-Dickstein et al., 2015; Ho et al., 2020; Song et al., 2021a; Song et al.,
2021b]. Latent diffusion made this process practical in a learned perceptual space
[Rombach et al., 2022]. Flow Matching instead learns a velocity field along a
chosen probability path, with Rectified Flow favoring straighter trajectories for
coarser integration [Lipman et al., 2023; Liu et al., 2023]. Despite their
different objectives, these methods expose intermediate generative states at which
inference-time constraints can be introduced.

The iterative sampling interface also permits partial observations to constrain
generation at inference time. RePaint injects known pixels by modifying the
reverse diffusion schedule without mask-specific training [Lugmayr et al., 2022].
More generally, Pseudoinverse-Guided Diffusion Models (\(\Pi\)GDM) use a known
measurement map and its pseudoinverse to approximate a conditional score, then
propagate the lifted measurement residual through the denoiser with a
vector-Jacobian product [Song et al., 2023]. This construction replaces a
task-specific conditional generator with a measurement correction applied to a
frozen generative prior. Pokle et al. transfer the same principle to pretrained
continuous flows by correcting the velocity field during sampling, again without
retraining the generator [Pokle et al., 2024]. These two works provide the direct
generative mechanism that FBFM adapts from static inverse problems to
time-aligned state and action coordinates.

Classical world models developed a complementary line based on latent dynamics and
imagined control. Early systems compressed observations or learned visual rollouts,
while recurrent state-space models made stochastic latent trajectories usable for
planning and policy optimization [Ha and Schmidhuber, 2018; Kaiser et al., 2020;
Hafner et al., 2019; Hafner et al., 2020]. Later work moved from reconstructive
continuous latents toward discrete stochastic or task-oriented representations that
retain quantities needed for planning and control [Hafner et al., 2021;
Schrittwieser et al., 2020; Hansen et al., 2022; Hafner et al., 2025]. This
progression establishes the latent state as an interface among perception,
predicted dynamics, and action. FBFM accordingly introduces real observations
through the WAM's encoded state space rather than directly through raw pixels.

In parallel, diffusion video prediction, action-conditioned simulation, and
interactive environment generation made explicit visual futures increasingly
controllable [Voleti et al., 2022; Yang et al., 2024; Bruce et al., 2024; Alonso
et al., 2024; Zhu et al., 2025]. WAMs emerge where this visual-generation line
meets action prediction: GR-1 and GR-2 transfer video pretraining to future-image
and robot-action prediction, LingBot-VA formulates autoregressive video--action
modeling with observation refresh, and DreamZero jointly generates future video
and actions [Wu et al., 2023; Cheang et al., 2024; Li et al., 2026; Ye et al.,
2026]. Fast-WAM shows that video co-training can remain useful when explicit future
generation is removed at inference time [Yuan et al., 2026]. FBFM addresses the
complementary regime in which that future-state stream is retained and must be
re-grounded by observations arriving during execution.

<!-- Theme 2: Diffusion and Flow-Matching robot policies. -->

Generative decision methods model trajectories or action chunks as structured
samples rather than pointwise regressions. Diffuser and Decision Diffuser brought
diffusion, guidance, and inpainting into trajectory-level planning, while ACT and
Diffusion Policy made temporally correlated action chunks a practical visuomotor
output [Janner et al., 2022; Ajay et al., 2023; Zhao et al., 2023; Chi et al.,
2023]. Extensions to compact 3D observations and billion-parameter,
cross-embodiment diffusion Transformers further established chunk-level generation
as a scalable interface for multimodal continuous actions [Ze et al., 2024; Liu
et al., 2025].

In parallel, generalist policies scaled robot learning through larger datasets,
cross-embodiment training, and pretrained vision--language representations, often
using autoregressive or discrete action readouts [Brohan et al., 2023a; Brohan et
al., 2023b; Octo Model Team et al., 2024; Kim et al., 2024]. This scaling route
motivated continuous generative heads that preserve VLM semantics while retaining
the multimodality and temporal structure of high-frequency action chunks.

Flow Matching likewise progressed from specialized motion generation on structured
robot state spaces to generalist VLA action modeling [Braun et al., 2024; Rouxel
et al., 2024; Zhang and Gienger, 2025]. \(\pi_0\) made this route broadly visible
by coupling a pretrained VLM with a Flow-Matching action expert and demonstrating
scalable, high-frequency continuous control; \(\pi_{0.5}\) retained the same action
interface while extending co-training and long-horizon generalization [Black et
al., 2024; Physical Intelligence et al., 2025]. Crucially for the present work,
the resulting iterative velocity field permits an action prefix to constrain a
chunk during generation. The two RTC formulations exploit this interface through
training-free pseudoinverse-guided inpainting and training-time prefix
conditioning, respectively [Black et al., 2025a; Black et al., 2025b], motivating
the following discussion of asynchronous feedback.

<!-- Theme 3: Inference-time guidance, asynchronous execution, and feedback. -->

Action chunking creates two coupled deployment problems: computation must overlap
with execution, while independently generated chunks must remain temporally
coherent. Bidirectional Decoding addresses this trade-off by sampling multiple
candidate chunks and selecting among them using backward coherence with previous
decisions and forward contrast between policy checkpoints [Liu et al., 2025].
Inference-time RTC instead acts inside a single Flow-Matching trajectory: it
represents actions already committed by the executing chunk as a frozen prefix,
uses a soft mask over later overlap, and applies pseudoinverse-guided inpainting to
a frozen policy [Black et al., 2025a]. Its training-time counterpart learns
prefix-conditioned postfix generation under simulated inference delays, removing
the sampling-time vector--Jacobian products at the cost of modifying training
[Black et al., 2025b]. Later approaches place the same continuity prior elsewhere,
including policy-native continuation learned by Legato and initial-noise selection
in PAINT [Liu et al., 2026; Ho et al., 2026]. These methods establish a rich design
space for cross-chunk action consistency; their constrained variables nevertheless
remain actions inherited from an earlier plan.

Other work targets responsiveness to information that becomes available during
execution. RA-DP interleaves one denoising update with dequeueing an executable
action and appending a noisy action, while admitting differentiable guidance from
dynamic signals [Ye et al., 2025]. Although new guidance objectives can be added
without retraining, its heterogeneous-noise action queue is itself learned with a
specialized training schedule. VLASH rolls the robot state forward under committed
actions and fine-tunes the policy with temporal offsets so that actions are
conditioned on an estimated execution-time proprioceptive state [Tang et al.,
2025]. A2C2 and DCDP instead use the latest observations to correct stale actions
through separately trained residual or dynamics-aware modules while keeping the
large base policy frozen [Sendai et al., 2025; Wu et al., 2026]. AsyncVLA refines
low-confidence action tokens before execution through a jointly trained
synchronous/asynchronous Flow-Matching model, whereas TIDAL combines stale semantic
intent with current proprioception in a trained micro-controller that interleaves
single-step flow integration and short action execution [Jiang et al., 2026; Sun et
al., 2026]. These approaches provide complementary choices among online
computation, specialized training, and action-space reactivity.

Dynamics-based guidance extends this discussion beyond action continuity.
DynaGuide backpropagates desired- or undesired-outcome objectives through a
separately trained latent dynamics model to steer the denoising of an off-the-shelf
diffusion policy [Du and Song, 2025]. More closely related to our motivation,
Feedback World Model independently closes the prediction--observation loop at
inference time: it maintains an auxiliary latent belief, uses the residual to the
observed state to correct one-step predictions, and converts those predictions
into action-aware guidance for a separate diffusion policy [An et al., 2026]. Its
analysis bounds the latent observer error; it does not analyze pseudoinverse
guidance of a multi-step WAM flow. AHA-WAM learns a different WAM-specific solution,
routing each current observation into reusable context from a low-frequency video
planner for a high-frequency action DiT [Cai et al., 2026]. WA-LQR preserves WAM
weights but steers robustness-related hidden activations toward setpoints identified
from contrastive rollouts and locally linearized block dynamics [Hong et al., 2026].
These studies demonstrate several useful forms of world or dynamics feedback, but
they differ in whether the reference is a task objective, an observer residual, a
routed context, or a learned activation feature.

Taken together, action-centric asynchronous methods primarily address cross-chunk
continuity or action-space responsiveness, whereas recent world- and
dynamics-feedback methods operate through one-step observers, learned context
routing, or activation-space control. FBFM studies the intersection of these
directions by imposing training-free, time-aligned state and action constraints
during the active generation of a frozen WAM.
