# LingBot-VA and RoboTwin Integration Details

## Audited Implementation Boundary

The implementation described here was audited at FBFM commit
`3ecac79bb1730b426f5338afa32a9e77b4bf74cb` against the released LingBot-VA
commit `7c6ffa9bfc4b83582cafc860fab4c82cc7deeeeb`. The integration retains the
pretrained transformer, VAE, text encoder, video-first/action-second execution
order, and LingBot-VA cache-update semantics. Both the checkpoint and all model
parameters remain frozen. Gradients are enabled only locally to obtain the
clean-endpoint VJP with respect to the current solver sample, and every guided
solver output is detached before the next step.

LingBot-VA appends a final zero-time transformer evaluation to each flow for
prediction-cache construction. This call is retained as cache-only: its output
is not integrated as an additional solver step. Consequently, the evaluated
configuration contains 25 numerical video-flow steps followed by one cache-only
evaluation, and 50 numerical action-flow steps followed by one cache-only
evaluation.

## Constraint Alignment

The RoboTwin configuration predicts two latent video slots, each paired with 16
low-level actions, yielding an action horizon of \(H=32\). The fixed execution
horizon is \(s=16\), and the hard-overlap boundary is \(d=16\). The final 16
actions of the preceding chunk are therefore aligned with the first 16 action
coordinates of the new chunk. The public robot commands are first mapped back
through LingBot-VA's action normalization and padded to its 30-channel internal
representation; the native action-channel mask keeps unused channels zero. In
this default setting \(d=H-s\), so the evaluated action constraint is a hard
prefix and the generalized soft-overlap region is empty.

State feedback uses the same three camera views and frozen VAE weights as the
base model, but an independent streaming encoder cache prevents feedback
windows from advancing the real-history encoder. The client samples one
observation package every four low-level actions. Four causal packages produce
one normalized video-latent slot, whose full channel and spatial block is
assigned to the corresponding future slot. A versioned chunk context stores
the latent target and slot mask; feedback outside the active window, duplicate
slots, and slots outside the predicted chunk are rejected.

The implementation directly compares this normalized latent target with the
predicted clean endpoint in aligned coordinates. It therefore realizes the
\(h^\dagger(h(\hat{\mathbf X}))\approx\hat{\mathbf X}\) approximation discussed
in Appendix B, without decoding and re-encoding the predicted endpoint at each
solver evaluation.

## Deterministic Pseudo-Asynchronous Schedule

RoboTwin is used as a controlled pseudo-asynchronous environment. The policy
client starts generation of a new chunk, executes the 16-action suffix of the
preceding chunk, and grants a fixed fraction of the video-flow budget after each
simulator transition. Across those 16 transitions, exactly 26 video
evaluations are released. Feedback is transmitted through a separate control
connection, queued without running model code in the communication thread, and
consumed at the next video-solver boundary. In multi-GPU inference, rank 0
broadcasts the same queued batch so that all ranks update an identical
constraint version.

Under the current temporal compression, the first complete feedback latent is
formed at the sixteenth executed action step. The first 15 simulator steps have
released 24 video evaluations; the final transition releases the remaining two.
Thus, the new state measurement affects the last numerical video update, after
which the cache-only evaluation writes the corrected prediction context for the
action flow. The action flow then completes before the deterministic chunk
handoff. This schedule is fixed across baseline and FBFM runs and is independent
of measured server latency.

Real observations produced during this interval are not immediately inserted
into the solver-start history. They first act as dynamic feedback for the active
chunk, are staged once, and are written together with their aligned executed
actions into the real KV cache before the following chunk is launched. This
one-chunk promotion rule separates dynamic feedback from history and prevents
duplicate cache updates.
