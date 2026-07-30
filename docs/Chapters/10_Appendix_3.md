# Implementation Details for Stage-Wise and Joint WAMs

## Audited Boundary and Common Controls

The corrected DreamZero integration is on branch
`experiment/dreamzero-l1mass-state-weight`. Its numerical implementation is
frozen at commit `cb08c9e552730d26cc446885e79a3e270a270d0c`, with the associated
audit and implementation record at commit
`0f2cc4f133532af16841b3698e7cc7a036cecdee`. These revisions supersede the
earlier A6000 snapshot `a7dcd4a4bbf69709c038fb433bbc1cf42b029f63` for all DreamZero
implementation claims. The default `main` branch does not contain this
corrected path and must not be used to reproduce the track.

The LingBot-VA/RoboTwin implementation was audited from the current experiment
worktree based on commit `e482dccb6841f3a2bea73128e05b0954371ee9be`. Its
run-specific launcher and task-manifest changes are still under validation and
have not yet been frozen into a published commit; the final result artifacts
must record that eventual revision. Both routes use BF16 inference and retain
their pretrained transformer, VAE, text encoder, classifier-free guidance,
scheduler, and cache behavior.
FBFM adds no learned module. Gradients are enabled only for the current noisy
sample while computing an endpoint VJP, and every corrected velocity and solver
sample is detached before the next step.

Each route exposes one solver path with three mask settings. The `NONE` mode
zeros the state and action masks, `RTC` retains only the previous-action mask,
and `FBFM` uses the same action mask together with the dynamic state mask.
Targets may be maintained in all modes, but a zero mask makes them numerically
inactive. This keeps the model, normalization, random initialization, solver
budget, and pseudo-asynchronous schedule fixed within each architecture.

The principal runtime settings are summarized below; subsequent sections
define their tensor alignment and scheduling semantics in detail.

| Setting | LingBot-VA | DreamZero |
|---|---:|---:|
| Generation factorization | Stage-wise | Joint |
| \((H,d,s)\) | \((32,16,16)\) | \((16,8,8)\) |
| Predicted state slots | 2 | 2 |
| Guided updates / Jacobian refreshes | 25 state / 50 action | 16 UniPC / 8 DiT--\(J\) |
| Pseudo-clock release | 26 video calls / 16 actions | 8 DiT blocks / 8 actions |
| State-target refresh | 4 sampled observations / latent | Every 3 actions (training stride) |
| State preconditioner | \(1\) | \(P_Z=56/9600\) |
| Proportional state gain | n/a | \(k_p=0.0486968\) |
| Guidance clip \(\beta\) | 10 | 10 |
| Precision | BF16 | BF16 |

*The LingBot-VA pseudo-clock count includes its final cache-only video call.*

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

Let UniPC index \(j\) be served by the most recent native DiT evaluation \(k\),
which supplies the unguided joint velocity \(\mathbf v_k\) and clean-endpoint
Jacobian \(\mathbf J_k\). In DreamZero's decreasing-noise convention, the
runtime computes

\[
\hat{\mathbf X}_j^1
=\mathbf X_j^{\sigma_j}-\sigma_j\mathbf v_k,
\qquad
\mathbf e_j
=\mathbf P\mathbf W_j(\mathbf Y_j-\hat{\mathbf X}_j^1),
\]

\[
\mathbf g_j=\mathbf J_k^{\mathsf T}\mathbf e_j,
\qquad
\tilde{\mathbf v}_j
=\mathbf v_k-\lambda(\sigma_j)\mathbf g_j.
\]

Here \(\mathbf X=[\mathbf Z,\mathbf A]\),
\(\mathbf J_k=\partial\hat{\mathbf X}_k^1/
\partial\mathbf X_k^{\sigma_k}\), \(\mathbf W_j\) is the binary state--action
support mask, and \(\mathbf P\) is a separate block-diagonal modality
preconditioner. The residual and VJP are formed jointly with respect to the
state and action samples. This retains the cross-modal Jacobian blocks:
even with an action residual of zero, a state residual may produce a nonzero
correction in action coordinates.

At each native DiT evaluation, \(\mathbf v_k\) and \(\mathbf J_k\) are
refreshed. At skipped DiT indices, only these two native quantities are reused;
the endpoint, residual, VJP, guidance coefficient, and guided field are
recomputed from the current sample and \(\sigma_j\). The solver cache therefore
never stores or recursively propagates \(\tilde{\mathbf v}_j\). We use
\(\tau=1-\sigma\), \(r^2=\sigma^2/(\tau^2+\sigma^2)\), and
\(\lambda(\sigma)=\min\{\sigma/(\tau r^2),\beta\}\) with \(\beta=10\).

The action block uses \(P_A=1\). For concision, the effective state block of
\(\mathbf P\) in the equations above is \(k_p P_Z\): \(P_Z\) balances modality
scale, while the separate proportional gain \(k_p\) tunes state-feedback loop
gain. The evaluated configuration uses \(P_Z=56/9600\) and
\(k_p=0.0486968\). Although the implementation applies their product by scaling
the stored state-mask tensor, \(\mathbf W_j\), \(P_Z\), and \(k_p\) remain
conceptually distinct. Schedule scalars are evaluated in at least FP32, outputs
are checked for finite values, and guided fields are detached after the current
update. Appendix E provides the stability motivation and complete parameter
search.

### Rolling Causal State Target

DreamZero's causal VAE uses an anchor plus four temporally sampled images to
encode one future latent. The LIBERO checkpoint was trained with a three-action
video stride. The runtime retains every newly observed image in causal order,
but refreshes the hard latent target only at offsets aligned with this stride.
Missing left history is padded with the measured launch anchor; an observed
image is never copied forward into an unobserved future position. The first two
windows available during an eight-action overlap are therefore
\([0,0,0,0,3]\) after action 3 and \([0,0,0,3,6]\) after action 6. Only these
two offsets refresh the first latent slot in the evaluated wave; the second
slot remains unmasked because the overlap provides no aligned measurement for
it.

Rolling feedback history is deliberately separate from the model's causal
inference history. The latter uses a one-frame warm-up and then the most recent
four chunk-level inference anchors, padding early history with the oldest
available frame. Per-action observations enter only the rolling feedback
history; a stride-aligned window updates the active FBFM target, and neither
operation advances the solver-start causal/KV history.

### Native Solver Schedule and Chunk Handoff

We use \(d=s=8\). DreamZero retains its 16-step UniPC scheduler and released
DiT cache mask, which evaluates the DiT and refreshes the endpoint Jacobian
eight times. A scheduler callback applies guidance to every UniPC update
without replacing the native velocities stored in `prev_predictions`. At a
skipped DiT index, the callback reuses the latest native velocity and Jacobian
but recomputes the endpoint residual and VJP for the current update.

After each committed action is executed, the client submits its observation
and releases one native DiT block. One block may cover multiple UniPC indices;
eight action releases expose all eight DiT/Jacobian refreshes and all 16 guided
UniPC updates. The observation is retained immediately, while the hard state
target changes only when its offset reaches the three-action encoder stride.
After the eight releases, the generated suffix at positions 8--15 becomes the
execution chunk for the next wave.

The native synchronous DreamZero control is kept distinct from the matched
pseudo-asynchronous modes: it replans from the latest observation, executes the
first eight actions, and does not invoke the overlap, feedback, or pseudo-clock
interfaces. In contrast, matched `NONE`, `RTC`, and `FBFM` runs all use the
same eight-action overlap protocol and differ only through their masks.

## Diagnostics and Numerical Safeguards

Both routes record the chunk and solver-step identifiers, constraint version,
active mask sizes, feedback offsets, endpoint errors, state/action correction
norms, guidance weight, and GPU memory. DreamZero additionally records the
UniPC index and whether its endpoint Jacobian was refreshed or reused. Solver
outputs are rejected if they contain non-finite values. These records are used
to verify stride-aligned target activation, the native-only velocity-cache
invariant, and that a state-active joint VJP can generate a nonzero
action-coordinate correction. Because a reused Jacobian is only a local
linearization, trust-region, norm-clipping, or native-update fallback safeguards
remain to be evaluated before the final benchmark.
