# Related Works

<!-- Theme 1: Generative modeling and world models. -->

Diffusion models were initially developed as iterative generative processes that
recover data by reversing a gradual corruption process [Sohl-Dickstein et al.,
2015; Ho et al., 2020]. DDIM and the score-SDE formulation subsequently
decoupled the learned denoiser or score from a single stochastic sampler and
connected diffusion to continuous-time probability dynamics [Song et al., 2021a;
Song et al., 2021b]. Latent diffusion moved this iterative process from pixels
into a learned perceptual space, making high-dimensional conditional generation
more tractable [Rombach et al., 2022]. Flow Matching provides a related continuous
generative view by learning a velocity field along a chosen probability path,
while Rectified Flow favors straighter transport trajectories that tolerate
coarser numerical integration [Lipman et al., 2023; Liu et al., 2023]. Although
these formulations use different objectives and path parameterizations, they all
generate structured samples through an iterative transport from a simple source
distribution to data.

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

Classical world models developed along a distinct but complementary line based
on latent dynamics and imagined control, rather than diffusion or Flow Matching.
World Models compressed images with a VAE and evolved the resulting latent
through a recurrent mixture-density model, while SimPLe learned a video predictor
for model-based rollouts [Ha and Schmidhuber, 2018; Kaiser et al., 2020]. PlaNet's
recurrent state-space model combined deterministic memory with stochastic latent
states for online planning, and Dreamer optimized a policy through trajectories
imagined in that latent dynamics model [Hafner et al., 2019; Hafner et al., 2020].
Subsequent work diversified what the representation should preserve: DreamerV2
used discrete stochastic states; MuZero learned dynamics that predict
planning-relevant quantities without reconstructing observations; and TD-MPC
learned a task-oriented, decoder-free latent for short-horizon trajectory
optimization [Hafner et al., 2021; Schrittwieser et al., 2020; Hansen et al.,
2022]. DreamerV3 further demonstrated that latent imagination can scale across
diverse control domains [Hafner et al., 2025]. This progression establishes the
latent state as an interface among perception, predicted dynamics, and control.
FBFM accordingly introduces real observations through the WAM's encoded state
space, rather than requiring feedback to act directly on raw pixels.

In parallel, generative video models made explicit visual futures increasingly
controllable. MCVD used conditional diffusion for video prediction and generation,
UniSim formulated an action-in-video-out diffusion simulator, and Genie learned
latent actions for interactive environment generation [Voleti et al., 2022; Yang
et al., 2024; Bruce et al., 2024]. DIAMOND further placed a diffusion model inside
an agent's learned environment, while IRASim introduced frame-level action
conditioning for fine-grained robot-object dynamics [Alonso et al., 2024; Zhu et
al., 2025]. World-Action Models arise where this explicit visual-generation line
meets latent dynamics and action prediction: GR-1 and GR-2 transfer video
pretraining into future-image and robot-action prediction, LingBot-VA formulates
autoregressive video-action modeling with closed-loop observation refresh, and
DreamZero jointly generates future video and actions from a pretrained video
diffusion backbone [Wu et al., 2023; Cheang et al., 2024; Li et al., 2026; Ye et
al., 2026]. Fast-WAM shows that video co-training can remain useful even when
explicit future generation is removed at inference time [Yuan et al., 2026].
FBFM addresses the complementary regime in which future-state generation is
retained and asks how its latent state stream can be re-grounded by observations
arriving during execution.

<!-- Theme 2: Diffusion and Flow-Matching robot policies. -->

Diffusion-based decision methods treat decisions as structured samples rather
than pointwise regressions. Diffuser denoises complete state-action trajectories and
reinterprets guidance and inpainting as planning constraints, while Decision
Diffuser casts offline decision-making as return-, constraint-, or
skill-conditioned generation [Janner et al., 2022; Ajay et al., 2023]. In
visuomotor imitation learning, ACT modeled temporally correlated action
chunks through a generative sequence model, and Diffusion Policy directly modeled
an observation-conditioned action horizon with iterative denoising and
receding-horizon execution [Zhao et al., 2023; Chi et al., 2023]. DP3 extended
this formulation with compact 3D observations, whereas RDT-1B scaled a diffusion
Transformer to multi-robot pretraining, a unified action representation, and
billion-parameter capacity [Ze et al., 2024; Liu et al., 2025]. Together, these
works established chunk-level generative modeling as a scalable interface for
multimodal continuous robot actions.

In parallel, RT-1, RT-2, Octo, and OpenVLA demonstrated that robot policies
benefit from larger and more diverse datasets, cross-embodiment training, and
pretrained vision-language representations, while adopting different action
readouts [Brohan et al., 2023a; Brohan et al., 2023b; Octo Model Team et al.,
2024; Kim et al., 2024]. RT-2 and OpenVLA, in particular, express actions through
discrete tokens so that robot trajectories can share an autoregressive interface
with language. This scaling trajectory motivates continuous generative action
heads that retain the semantic priors of a VLM without reducing high-frequency,
multimodal action chunks to a point estimate or a long sequence of discretized
outputs.

Flow Matching developed into a robot action generator across both specialized
motion policies and generalist VLA models. RFMP transported robot motions on
Riemannian state spaces, while related work applied Flow Matching to
multi-support whole-body imitation and affordance-conditioned manipulation
[Braun et al., 2024; Rouxel et al., 2024; Zhang and Gienger, 2025]. This
technical route gained much broader visibility through \(\pi_0\), which brought
Flow Matching into a large-scale generalist VLA by pairing a pretrained VLM
backbone with a smaller
robotics-specific action expert and combining cross-embodiment pretraining with
post-training. Its strong performance on high-frequency dexterous manipulation
helped establish Flow Matching as a practical and
scalable route for continuous robot action generation [Black et al., 2024].
\(\pi_{0.5}\) retained this action-generation design while adding heterogeneous
co-training and
semantic subtask prediction for open-world, long-horizon manipulation [Physical
Intelligence et al., 2025]. Beyond predictive performance, this conditional
Flow-Matching action expert exposes an iterative velocity-field interface through
which an action prefix can constrain a chunk as it is generated. The two RTC
formulations exploit this interface through training-free pseudoinverse-guided
inpainting and training-time action-prefix conditioning, respectively [Black et
al., 2025a; Black et al., 2025b]. This connection motivates the following
discussion of asynchronous execution and feedback.
