# Related Works

<!-- Theme 1: Generative modeling and world models. -->

Diffusion and Flow Matching established iterative transport as a general
interface for structured generation [Sohl-Dickstein et al., 2015; Ho et al.,
2020; Song et al., 2021a; Song et al., 2021b; Rombach et al., 2022; Lipman et
al., 2023; Liu et al., 2023]. Their intermediate sampling states also admit
inference-time constraints. RePaint conditions diffusion on known pixels, while
\(\Pi\)GDM and its continuous-flow extensions propagate measurement residuals
through a frozen generator by vector--Jacobian products [Lugmayr et al., 2022;
Song et al., 2023; Pokle et al., 2024]. This pseudoinverse-guided interface is
the generative foundation of FBFM.

World models developed in parallel from learned visual rollouts and recurrent
latent dynamics toward task-oriented representations for imagined control [Ha
and Schmidhuber, 2018; Kaiser et al., 2020; Hafner et al., 2019; Hafner et al.,
2020; Hafner et al., 2021; Schrittwieser et al., 2020; Hansen et al., 2022;
Hafner et al., 2025]. Video diffusion, action-conditioned simulation, and
interactive generation then made explicit visual futures increasingly
controllable [Voleti et al., 2022; Yang et al., 2024; Bruce et al., 2024;
Alonso et al., 2024; Zhu et al., 2025]. At their intersection, GR-1/GR-2
predict future images and actions, LingBot-VA models video and action with
observation refresh, and DreamZero jointly generates both modalities [Wu et
al., 2023; Cheang et al., 2024; Li et al., 2026; Ye et al., 2026]. Fast-WAM
instead removes explicit future imagination at inference [Yuan et al., 2026];
FBFM addresses WAMs that retain this latent future and must re-ground it during
execution.

<!-- Theme 2: Diffusion and Flow-Matching robot policies. -->

Generative decision models brought diffusion and inpainting from trajectory
planning to temporally correlated action chunks [Janner et al., 2022; Ajay et
al., 2023; Zhao et al., 2023; Chi et al., 2023; Ze et al., 2024; Liu et al.,
2025]. In parallel, RT-1/RT-2, Octo, and OpenVLA scaled generalist robot
policies through larger data and pretrained vision--language representations
[Brohan et al., 2023a; Brohan et al., 2023b; Octo Model Team et al., 2024; Kim
et al., 2024]. Flow-Matching policies progressed from structured robot motion
to generalist VLA control [Braun et al., 2024; Rouxel et al., 2024; Zhang and
Gienger, 2025]. The broad empirical adoption of the Flow-Matching action expert
in \(\pi_0\) and \(\pi_{0.5}\) [Black et al., 2024; Physical Intelligence et
al., 2025] is especially relevant: their iterative velocity field enables RTC
to impose a committed action prefix through training-free inpainting or
learned prefix conditioning [Black et al., 2025a; Black et al., 2025b].

<!-- Theme 3: Inference-time guidance, asynchronous execution, and feedback. -->

Asynchronous action-chunk execution must overlap inference with control while
maintaining cross-chunk continuity. Bidirectional Decoding selects coherent
candidate chunks; inference-time RTC directly constrains the active
Flow-Matching trajectory; its training-time counterpart, Legato, and PAINT
instead learn continuation or modify initialization [Liu et al., 2025; Black
et al., 2025a; Black et al., 2025b; Liu et al., 2026; Ho et al., 2026]. These
methods mainly constrain actions inherited from an earlier plan.

Other approaches react to information arriving during execution. RA-DP
interleaves denoising and action dequeueing, VLASH compensates inference delay
with predicted execution-time state, and A2C2/DCDP correct stale actions using
additional learned modules [Ye et al., 2025; Tang et al., 2025; Sendai et al.,
2025; Wu et al., 2026]. AsyncVLA and TIDAL likewise trade specialized training
or a lightweight controller for online action refinement [Jiang et al., 2026;
Sun et al., 2026]. These methods complement FBFM but operate primarily in
action space.

Dynamics- and world-feedback methods provide the closest second line of work.
DynaGuide steers a diffusion policy through a separately trained latent
dynamics model [Du and Song, 2025]. Feedback World Model independently closes
a prediction--observation loop with a latent observer and action-aware
guidance, and provides an observer-error analysis [An et al., 2026]. AHA-WAM
routes current observations into reusable WAM context, while WA-LQR controls
internal WAM activations [Cai et al., 2026; Hong et al., 2026]. FBFM instead
uses the frozen WAM's own differentiable flow to impose time-aligned
latent-state measurements and committed actions within the actively generated
multi-step chunk.
