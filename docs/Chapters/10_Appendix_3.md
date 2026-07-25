# Implementation Details for Stage-Wise and Joint WAMs

## Audited Boundary and Common Controls

The implementation described here was audited in the LingBot-VA/RoboTwin
repository at commit `e482dccb6841f3a2bea73128e05b0954371ee9be` and in the
DreamZero/LIBERO repository at commit
`a7dcd4a4bbf69709c038fb433bbc1cf42b029f63`. The exact revisions used to
produce the reported tables must match these audited snapshots. Both routes
use BF16 inference and retain their pretrained transformer, VAE, text encoder,
classifier-free guidance, scheduler, and cache behavior.
FBFM adds no learned module. Gradients are enabled only for the current noisy
sample while computing an endpoint VJP, and every corrected velocity and solver
sample is detached before the next step.

Each route exposes one solver path with three mask settings. The `NONE` mode
zeros the state and action masks, `RTC` retains only the previous-action mask,
and `FBFM` uses the same action mask together with the dynamic state mask.
Targets may be maintained in all modes, but a zero mask makes them numerically
inactive. This keeps the model, normalization, random initialization, solver
budget, and pseudo-asynchronous schedule fixed within each architecture.

## LingBot-VA on RoboTwin

### Tensor and Constraint Alignment

The RoboTwin configuration predicts two video-latent slots. Each slot is paired
with 16 low-level actions, giving \(H=32\). For the three-camera input, the
overhead image is resized to \(256\times320\), the two wrist images to
\(128\times160\), and their encoded features are spatially concatenated in the
same layout as the released model. The resulting video sample has shape
\([1,48,2,24,20]\); its state mask has shape \([1,1,2,1,1]\) and is broadcast
over each complete channel--spatial latent block.

The action solver uses a tensor of shape \([1,30,2,16,1]\). RoboTwin's 16
active command channels are restored to LingBot-VA's 30-channel internal
layout, normalized with the checkpoint's 1st and 99th action quantiles, and
masked so that unused internal channels remain zero. We use \(d=s=16\). The
last 16 actions of the preceding chunk are placed at the first 16 temporal
coordinates of the new chunk and remain fixed throughout its generation. Since
\(d=H-s\), the generalized soft-overlap interval is empty in this experiment;
the realized constraint is a hard action prefix.

State feedback is encoded with the frozen streaming VAE and compared directly
with the predicted clean endpoint in normalized latent coordinates. Hence the
implementation uses the aligned-coordinate approximation
\(h^\dagger(h(\hat{\mathbf X}))\approx\hat{\mathbf X}\) discussed in Appendix B,
without decoding and re-encoding the predicted endpoint at every solver step.
The feedback encoder has an independent streaming cache, so encoding a dynamic
measurement does not advance the real-history encoder.

### Solver and Feedback Schedule

LingBot-VA performs stage-wise generation. The released 25-step video flow and
50-step action flow are retained. Each stage also appends a zero-time
transformer call to update its prediction cache; this call is executed under
`no_grad` and its numerical output is not integrated. The realized schedule is
therefore 25 numerical video updates plus one cache-only evaluation, followed
by 50 numerical action updates plus one cache-only evaluation. The guidance
coefficient follows the schedule in Section 3 and is clipped at
\(\beta=10\).

RoboTwin execution is coupled to the video stage by a deterministic clock. The
client launches the new chunk, executes the 16-action suffix of the preceding
chunk, and releases exactly 26 video evaluations over these 16 simulator
transitions. An observation package is sampled after every four actions. The
stream is first primed with the solver-start observation; four subsequent
packages yield one normalized latent slot. Thus, under the evaluated temporal
compression, the first complete dynamic state target is formed after action
16. The first 15 transitions have released 24 evaluations, and the final
transition releases the remaining two. Feedback is consumed before the first
of these evaluations, so it affects the last numerical video update; the final
cache-only call then records the corrected state context. The action stage
starts only after this video schedule completes.

Inference and feedback use separate communication lanes. The communication
thread only queues CPU observations; queued items are encoded and installed at
video-solver boundaries. A versioned chunk context rejects duplicate or
out-of-range state slots and supplies an atomic target--mask snapshot to every
evaluation. When distributed inference is enabled, rank zero broadcasts the
queued feedback batch before all ranks update the same context version.

### Real-History Promotion

The model's real KV history contains only observation--action pairs available
when the active solver was launched. Observations collected while that solver
runs first enter the dynamic FBFM feedback set. At chunk handoff, those
observations and the aligned executed action frame are staged once and written
to the real KV cache before the following launch. This one-chunk promotion rule
prevents a transition from appearing simultaneously as solver-start history
and newly arrived state feedback. The implementation also checks that the
observation and action frame counts agree before every real-history update.

## DreamZero on LIBERO

### Joint Endpoint Guidance

DreamZero predicts two video-latent slots and \(H=16\) actions in one joint
solver. At a native DiT evaluation, the video sample has shape
\([1,48,2,10,20]\), while the action sample and target have shape
\([1,16,32]\). Physical LIBERO commands have seven dimensions; the preceding
eight actions are quantile-normalized, padded to 32 model coordinates, and
placed in the first eight temporal positions. The active action mask therefore
contains \(8\times7=56\) scalar coordinates. During the eight-action overlap,
real observations support the first of the two future latent slots, containing
\(48\times10\times20=9600\) coordinates.

The hook reconstructs the conditional clean endpoints in DreamZero's
decreasing-noise convention,

\[
\hat{\mathbf Z}^{1}=\mathbf Z^{\sigma}-\sigma\mathbf v_Z,
\qquad
\hat{\mathbf A}^{1}=\mathbf A^{\sigma}-\sigma\mathbf v_A.
\]

It forms the state and action residuals together and requests one VJP with
respect to both \(\mathbf Z^{\sigma}\) and \(\mathbf A^{\sigma}\). This single
joint differentiation retains the cross-modal Jacobian blocks: even with an
action residual of zero, the state residual may produce a nonzero correction
in action coordinates. The corrected fields are

\[
(\tilde{\mathbf v}_Z,\tilde{\mathbf v}_A)
=
(\mathbf v_Z,\mathbf v_A)-\lambda_\sigma(\mathbf g_Z,\mathbf g_A),
\]

where \(\tau=1-\sigma\),
\(r^2=\sigma^2/(\tau^2+\sigma^2)\), and
\(\lambda_\sigma=\min\{\sigma/(\tau r^2),\beta\}\) with \(\beta=10\).
We multiply every active state-mask coordinate by \(56/9600\), so one observed
state block and the action block each contribute an aggregate mask weight of
56 before their data-dependent residuals and Jacobians are applied. Schedule
scalars are evaluated in at least FP32, corrected fields are checked for finite
values, and outputs are detached immediately.

### Rolling Causal State Target

DreamZero's causal VAE uses an anchor plus four future image samples to encode
one future latent. One latent corresponds to eight actions, so complete samples
occur at action offsets \(2,4,6,8\). Nevertheless, the state target is refreshed
after every executed action. Until all four samples are observed, the latest
real image is held forward in the missing positions. For example, the source
offsets begin as \([0,1,1,1,1]\) and end as the fully observed
\([0,2,4,6,8]\). The provisional target is causal at every release and equals
the native complete-window encoding at offset 8. Each refresh increments the
constraint version and overwrites the first latent slot; the second slot
remains unmasked because the evaluated overlap provides no real measurements
for it.

Rolling feedback history is deliberately separate from the model's causal
inference history. The latter uses a one-frame warm-up and then the most recent
four chunk-level inference anchors, padding early history with the oldest
available frame. Per-action observations update only the active FBFM target and
do not advance the solver-start causal/KV history.

### Native Solver Schedule and Chunk Handoff

We use \(d=s=8\). DreamZero retains its 16-step UniPC scheduler and released
DiT cache mask, which evaluates the DiT eight times. The integration hooks only
these eight native evaluations; cache updates and skipped scheduler positions
follow the released path unchanged. After each committed action is executed,
the client submits its new observation and releases one DiT evaluation. The
solver drains feedback, snapshots the new version, applies joint guidance, and
signals completion before the next environment transition. After eight
releases, the generated suffix at positions 8--15 becomes the execution chunk
for the next wave.

The native synchronous DreamZero control is kept distinct from the matched
pseudo-asynchronous modes: it replans from the latest observation, executes the
first eight actions, and does not invoke the overlap, feedback, or pseudo-clock
interfaces. In contrast, matched `NONE`, `RTC`, and `FBFM` runs all use the
same eight-action overlap protocol and differ only through their masks.

## Diagnostics and Numerical Safeguards

Both routes record the chunk and solver-step identifiers, constraint version,
active mask sizes, feedback offsets, endpoint errors, state/action correction
norms, guidance weight, and GPU memory. Solver outputs are rejected if they
contain non-finite values. These records are used to verify that feedback is
visible at the claimed evaluation boundary and, for DreamZero, that a
state-active joint VJP can generate a nonzero action-coordinate correction.
