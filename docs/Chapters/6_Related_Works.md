# Related Works

<!-- Theme 1: Generative modeling and world models. -->

Diffusion models were initially developed as iterative generative processes that
recover data by reversing a gradual corruption process [Sohl-Dickstein et al.,
2015; Ho et al., 2020]. Subsequent formulations decoupled the learned denoiser
from a particular stochastic sampler through non-Markovian diffusion and
continuous-time score dynamics [Song et al., 2021a; Song et al., 2021b]. Flow
Matching provides a closely related continuous generative view: instead of
learning the reverse of a prescribed noising process, it trains a velocity field
that transports a simple source distribution to the data distribution along a
chosen probability path [Lipman et al., 2023]. Rectified Flow further favors
increasingly straight transport trajectories that can be integrated accurately
with fewer solver evaluations [Liu et al., 2023]. Thus, diffusion and Flow
Matching use different training and path parameterizations, but both generate
structured samples through iterative transport from noise to data.

Their iterative sampling procedures also permit observations to be introduced at
inference time. RePaint conditions an unconditional diffusion prior on known
pixels by modifying only the reverse sampling schedule, without mask-specific
training [Lugmayr et al., 2022]. More generally, Pseudoinverse-Guided Diffusion
Models (\(\Pi\)GDM) use a known measurement model and its pseudoinverse to
approximate a conditional score, with a vector-Jacobian product propagating
measurement residuals back to the current sample [Song et al., 2023]. Pokle et
al. transfer this correction to pretrained flow models, adding measurement
guidance directly to the velocity field while retaining a training-free linear
inverse solver [Pokle et al., 2024]. This progression establishes the technical
basis for using partial measurements to steer a frozen continuous generator
during sampling.

World models shift the generated object from a static sample to the future of an
acting agent. Early neural world models learned compact visual dynamics and used
imagined rollouts for controller training or latent-space planning [Ha and
Schmidhuber, 2018; Hafner et al., 2019]. Dreamer and its successors further
optimized policies through trajectories imagined in learned latent dynamics and
scaled this principle across increasingly diverse control domains [Hafner et al.,
2020; Hafner et al., 2021; Hafner et al., 2025]. With the emergence of large
video generators, UniSim and Genie reframed video prediction as an interactive,
action-conditioned simulation problem, while IRASim introduced frame-level
action conditioning for fine-grained robot-object dynamics [Yang et al., 2024;
Bruce et al., 2024; Zhu et al., 2025]. Recent video-action policies and
World-Action Models (WAMs) move one step further by coupling future visual
generation with robot action prediction: GR-2 transfers Internet-video dynamics
into joint video-action fine-tuning, LingBot-VA formulates autoregressive
video-action modeling with closed-loop observation refresh and asynchronous
execution, and DreamZero jointly generates future video and actions from a
pretrained video diffusion backbone [Cheang et al., 2024; Li et al., 2026; Ye et
al., 2026]. Fast-WAM shows that video co-training can remain beneficial even when
explicit future generation is removed at inference time [Yuan et al., 2026].
FBFM addresses the complementary setting in which such future-state generation
is retained, and asks how the generated state stream can be re-grounded with
observations arriving during execution.
