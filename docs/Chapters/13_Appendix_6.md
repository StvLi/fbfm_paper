# Appendix F: Auxiliary Video-Codec Diagnostic

To isolate how temporal feedback coverage interacts with the video codec, we
additionally apply state-only FBFM to the auxiliary ball-meets-ball sequence.
This diagnostic is separate from the primary robot evaluation and exposes an
unresolved behavior that appears when feedback measurements cover only a
finite prefix of a temporally compressed video latent.

![State-feedback coverage on the auxiliary ball-collision sequence. Rows show
0, 0.25, 0.5, 1, 2, 3, 4, and 5 s; columns show the reference, Wan2.2 Base,
and FBFM with 10, 20, and 30 measured latent slots.](../../material/wan2.2/ball_meet_ball_fiveway_vertical.jpg)

Extending feedback from 10 to 30 time-aligned slots progressively covers the
measured motion. With all 30 slots, FBFM reduces table-region MAE from 21.77 to
6.34 and reduces the mean orange-ball center error from 173.84 to 3.05 pixels,
confirming that the state constraints affect the generated trajectory. The
principal failure mode is instead the large-area corruption that develops after
the finite feedback horizon in the 10- and 20-slot settings. Its onset moves
later as the measured prefix is extended, while full 30-slot coverage largely
preserves the scene structure over the evaluated horizon.

We attribute this behavior primarily to a Wan2.2-specific mismatch between the
codec and the generative backbone. Pseudoinverse guidance assumes that a
measurement lifted through the encoder is compatible with the model's clean
latent-state distribution. Wan2.2's joint video training and subsequent
post-training may distort the effective VAE-latent distribution used by the
generator, such that independently encoded observations do not necessarily
remain semantically meaningful clean-video states under the guided dynamics.
Once the finite constraint ends, this off-manifold mismatch can amplify and
decode into large regions without a coherent visual interpretation. Separate
image- and latent-space MSE diagnostics further examine this model-specific
hypothesis.
