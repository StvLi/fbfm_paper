# Preliminaries and Notations

> Status: section scaffold. The technical content will be written and reviewed subsection by subsection.

## Problem Formulation: Agent-Environment Interaction

We consider an embodied agent interacting with an environment over a family of tasks
\(\mathcal{T}\). The interaction is modeled as a controlled Markov process

\[
\mathcal{M} = (\mathcal{S}, \mathcal{A}, P),
\]

where \(\mathcal{S}\) and \(\mathcal{A}\) denote the environment state space and the
action space, respectively, and \(P(s_{t+1}\mid s_t,a_t)\) is the environment
transition kernel. Each task \(T\in\mathcal{T}\) may specify an initial-state
distribution \(\rho_T\) and a task condition \(c_T\), such as a language instruction
or a goal specification. We assume that the tasks share the same state space, action
space, and physical dynamics. At environment time step \(t\), the environment is in
state \(s_t\in\mathcal{S}\), the agent applies an action \(a_t\in\mathcal{A}\), and
the next state evolves according to

\[
s_0\sim\rho_T, \qquad s_{t+1}\sim P(\cdot\mid s_t,a_t).
\]

The physical state \(s_t\) is not necessarily exposed directly to the agent. Let
\(\mathcal{O}\) denote the sensing process and \(E\) a perceptual encoder. We define
the latent state available to the world-action model (WAM) as

\[
z_t = E\!\left(\mathcal{O}(s_t)\right),
\]

where \(z_t\in\mathcal{Z}\) summarizes the sensory observation of \(s_t\). This
distinction allows the environment dynamics to remain Markovian in \(s_t\), while
the agent may act from encoded and potentially partial observations. We denote the
interaction history available at time \(t\) by

\[
\mathcal{H}_t = (c_T,z_0,a_0,z_1,a_1,\ldots,a_{t-1},z_t),
\]

and write the action-selection process generally as
\(a_t\sim\pi(\cdot\mid\mathcal{H}_t)\). This notation does not require \(z_t\) itself
to be a sufficient Markov state.

Rather than selecting only a single action, a WAM predicts future latent states and
actions over a horizon \(H\). Starting at time \(t\), we denote its predicted latent
and action chunks by

\[
\hat{\mathbf{Z}}_{t,H}
= (\hat z_{t+1},\ldots,\hat z_{t+H}),
\qquad
\hat{\mathbf{A}}_{t,H}
= (\hat a_t,\ldots,\hat a_{t+H-1}),
\]

with the generic predictive model

\[
(\hat{\mathbf{Z}}_{t,H},\hat{\mathbf{A}}_{t,H})
\sim p_\theta(\cdot\mid\mathcal{H}_t).
\]

This expression does not prescribe how the two chunks are generated: a WAM may
model them with a joint generative process or factorize generation into successive
latent-state and action stages. During execution, realized transitions and external
disturbances can cause the newly encoded latent \(z_{t+1}\) to deviate from its
prediction \(\hat z_{t+1}\). Our objective is therefore not to learn a
reward-maximizing policy, but to incorporate such newly available state feedback,
together with previously generated action constraints, into the inference process of
a pretrained WAM. Accordingly, rewards, returns, and value functions are not part of
our formulation.

## Flow Matching

We distinguish an individual variable at one environment step from a chunk spanning
multiple steps. An action
\(a_t\in\mathbb{R}^{d_a}\) is a single control command at environment time \(t\),
whereas

\[
\mathbf{A}_t
= [a_t^{\mathsf T},a_{t+1}^{\mathsf T},\ldots,
a_{t+H-1}^{\mathsf T}]^{\mathsf T}
\in\mathbb{R}^{D_A},
\qquad D_A=H d_a,
\]

is the time-stacked action vector of horizon \(H\). Similarly,
\(z_t\in\mathcal{Z}\subseteq\mathbb R^{d_z}\) denotes the single-step latent state
defined above, while

\[
\mathbf{Z}_t
= [z_{t+1}^{\mathsf T},z_{t+2}^{\mathsf T},\ldots,
z_{t+H}^{\mathsf T}]^{\mathsf T}
\in\mathbb R^{D_Z},
\qquad D_Z=H d_z,
\]

denotes the time-stacked future latent-state vector aligned with the action horizon.
Bold uppercase symbols therefore denote chunk-level vectors throughout the paper.
We use
lowercase \(x\) for a generic single-step variable and uppercase
\(\mathbf{X}\) for its chunk-level counterpart. Thus,
\((x,\mathbf{X})=(a,\mathbf{A})\) for action generation and
\((x,\mathbf{X})=(z,\mathbf{Z})\) for latent-state generation. For a WAM that
generates both modalities jointly, \(\mathbf{X}_t\) may instead denote their
concatenation,

\[
\mathbf{X}_t
=
\begin{bmatrix}
\mathbf Z_t\\
\mathbf A_t
\end{bmatrix}
\in\mathbb R^{D_X},
\qquad D_X=D_Z+D_A.
\]

For bold vectors \(\mathbf x\in\mathbb R^{d_x}\) and
\(\mathbf y\in\mathbb R^{d_y}\), all derivatives use the numerator-layout
Jacobian convention,
\(\partial\mathbf y/\partial\mathbf x\in\mathbb R^{d_y\times d_x}\).
When \(\mathbf X\) denotes a generic generation vector, \(D\) denotes its
corresponding dimension.

This generic notation does not imply a particular WAM factorization. A joint WAM
transports the concatenated \(\mathbf{X}_t\) with one flow, whereas a stage-wise WAM
applies separate flows to \(\mathbf{Z}_t\) and \(\mathbf{A}_t\). In either case, the
elements of a generated chunk remain aligned with individual environment steps; this
alignment will later allow FBFM to constrain selected \(z_{t+i}\) and
\(a_{t+i}\), rather than treating the chunk as an indivisible unit.

Flow Matching learns a time-dependent vector field that transports samples from a
simple source distribution to the conditional data distribution. Let
\(\tau\in[0,1]\) denote continuous flow time, distinct from the environment index
\(t\). Given a target chunk \(\mathbf{X}_t\) and Gaussian noise
\(\boldsymbol{\epsilon}\sim\mathcal{N}(\mathbf{0},\mathbf{I})\) of the same dimension,
we use the linear conditional probability path

\[
\mathbf{X}_t^\tau
= (1-\tau)\boldsymbol{\epsilon}+\tau\mathbf{X}_t,
\qquad
\mathbf{X}_t^0=\boldsymbol{\epsilon},
\quad
\mathbf{X}_t^1=\mathbf{X}_t.
\]

Its conditional target velocity is constant along the path:

\[
\mathbf{u}(\mathbf{X}_t^\tau\mid\mathbf{X}_t)
= \frac{\mathrm{d}\mathbf{X}_t^\tau}{\mathrm{d}\tau}
= \mathbf{X}_t-\boldsymbol{\epsilon}.
\]

Conditioned on the interaction history \(\mathcal{H}_t\), a Flow-Matching model
\(v_\theta\) takes the current noisy chunk and flow time as inputs and predicts a
velocity with the same dimension as \(\mathbf{X}_t\). It is trained using

\[
\mathcal{L}_{\mathrm{FM}}(\theta)
=
\mathbb{E}_{\substack{
(\mathcal{H}_t,\mathbf{X}_t)\sim\mathcal{D},\,
\boldsymbol{\epsilon}\sim\mathcal{N}(\mathbf{0},\mathbf{I}),\,
\tau\sim p(\tau)}}
\left[
\left\|
v_\theta(\mathbf{X}_t^\tau,\tau;\mathcal{H}_t)
-
(\mathbf{X}_t-\boldsymbol{\epsilon})
\right\|_2^2
\right],
\]

where \(p(\tau)\) is a chosen flow-time sampling distribution. Uniform sampling is
the standard choice, while non-uniform schedules may emphasize particular noise
levels.

At inference time, generation starts from
\(\mathbf{X}_t^0\sim\mathcal{N}(\mathbf{0},\mathbf{I})\) and solves the conditional
ordinary differential equation

\[
\frac{\mathrm{d}\mathbf{X}_t^\tau}{\mathrm{d}\tau}
= v_\theta(\mathbf{X}_t^\tau,\tau;\mathcal{H}_t),
\qquad
\hat{\mathbf{X}}_t
= \mathbf{X}_t^0
+ \int_0^1
v_\theta(\mathbf{X}_t^\tau,\tau;\mathcal{H}_t)\,
\mathrm{d}\tau.
\]

For example, a forward Euler solver uses

\[
\mathbf{X}_t^{\tau_{k+1}}
=
\mathbf{X}_t^{\tau_k}
+ \Delta\tau_k\,
v_\theta(\mathbf{X}_t^{\tau_k},\tau_k;\mathcal{H}_t).
\]

Some implementations parameterize the same path by the remaining noise level
\(\sigma=1-\tau\), which is integrated from \(1\) to \(0\). Defining the
corresponding field as
\(\tilde v_\theta=-v_\theta\), the clean endpoint estimate under the linear path is

\[
\hat{\mathbf{X}}_t^1
=
\mathbf{X}_t^\sigma
-\sigma\,
\tilde v_\theta(\mathbf{X}_t^\sigma,\sigma;\mathcal{H}_t).
\]

We use superscripts exclusively for flow time or noise level and subscripts for
environment time. This separation is important for FBFM, which modifies the
inference-time vector field while preserving the pretrained Flow-Matching model.

## Pseudoinverse-Guided Inpainting

Pseudoinverse guidance conditions a pretrained generative model on an inverse
problem without task-specific retraining (Song et al., 2023). Let the clean endpoint
\(\mathbf{X}_t^1\) produce a measurement

\[
\mathbf{Y}_t=h(\mathbf{X}_t^1)+\boldsymbol{\eta},
\qquad
\boldsymbol{\eta}\sim\mathcal{N}(\mathbf{0},\sigma_y^2\mathbf{I}),
\]

where \(h:\mathcal{X}\rightarrow\mathcal{Y}\) is the measurement operator. Song
et al. extend the linear Moore--Penrose pseudoinverse to a generalized inverse
\(h^\dagger:\mathcal{Y}\rightarrow\mathcal{X}\), satisfying
\(h(h^\dagger(h(\mathbf{X})))=h(\mathbf{X})\). We interpret \(h\) and
\(h^\dagger\) as a feedback encoder--decoder pair: \(h\) maps a generated
state-action object to the feedback space, while \(h^\dagger\) lifts feedback back
to the generation space. The precise consistency assumptions and their local
Moore--Penrose interpretation are provided in Appendix B.

For Flow Matching, the predicted clean endpoint at flow time \(\tau\) is

\[
\hat{\mathbf{X}}_t^1
=f_\theta^\tau(\mathbf{X}_t^\tau)
:=\mathbf{X}_t^\tau
+(1-\tau)v_\theta(\mathbf{X}_t^\tau,\tau;\mathcal{H}_t).
\]

Given mask weights \(\mathbf w_t\in[0,1]^D\), let
\(\mathbf W_t=\operatorname{Diag}(\mathbf w_t)\in\mathbb R^{D\times D}\) be the
corresponding feedback-weighting operator. Pseudoinverse inpainting forms the lifted
discrepancy and propagates it through the endpoint predictor:

\[
\mathbf{e}_t^\tau
=\mathbf{W}_t
\left[
h^\dagger(\mathbf{Y}_t)
-h^\dagger\!\left(h(\hat{\mathbf{X}}_t^1)\right)
\right],
\qquad
\mathbf{g}_t^\tau
=
\left(
\frac{\partial f_\theta^\tau(\mathbf{X}_t^\tau)}
     {\partial\mathbf{X}_t^\tau}
\right)^{\mathsf T}
\mathbf{e}_t^\tau.
\]

The VJP \(\mathbf{g}_t^\tau\) is added to the pretrained velocity field,

\[
v_{\mathrm{PG}}
=v_\theta+\lambda_\tau\mathbf{g}_t^\tau,
\]

where \(\lambda_\tau\) controls the guidance strength. This Flow-Matching
specialization follows the inference-time inpainting construction of Black et al.
(2025).

In FBFM, observed latent states and previous actions are already encoded and aligned
with the corresponding generation coordinates. We therefore use the practical
approximation
\(h^\dagger(h(\hat{\mathbf{X}}_t^1))\approx\hat{\mathbf{X}}_t^1\) on the
mask-selected feedback subspace. When \(h^\dagger(\mathbf{Y}_t)\) is likewise stored
in aligned coordinates and denoted by \(\mathbf{Y}_t\), the error reduces to

\[
\mathbf{e}_t^\tau
=\mathbf{W}_t
\left(\mathbf{Y}_t-\hat{\mathbf{X}}_t^1\right).
\]

Here, \(\mathbf w_t\in\{0,1\}^D\) gives exact masked inpainting, while
\(\mathbf w_t\in[0,1]^D\) gives a confidence-weighted relaxation. The same notation
applies when \(\mathbf{X}\) is an action chunk \(\mathbf{A}\), a latent-state chunk
\(\mathbf{Z}\), or their joint representation. The construction of
\(\mathbf{Y}_t\), the asynchronous update of \(\mathbf{W}_t\), and the joint versus
stage-wise implementations are deferred to the method section.

For quick reference, Appendix A provides a consolidated index of the notation used
throughout the paper.
