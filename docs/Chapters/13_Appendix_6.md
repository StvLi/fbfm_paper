# Appendix F: Auxiliary Video-Codec Diagnostic

To isolate how temporal feedback coverage interacts with the video codec, we
additionally apply state-only FBFM to the auxiliary ball-meets-ball sequence.
This diagnostic is separate from the primary robot evaluation and exposes an
unresolved behavior of pseudoinverse guidance in temporally compressed video
latent spaces.

![State-feedback coverage on the auxiliary ball-collision sequence. Rows show
0, 0.25, 0.5, 1, 2, 3, 4, and 5 s; columns show the reference, Wan2.2 Base,
and FBFM with 10, 20, and 30 measured latent slots.](../../material/wan2.2/ball_meet_ball_fiveway_vertical.jpg)

Extending feedback from 10 to 30 time-aligned slots progressively covers the
measured motion. With all 30 slots, FBFM reduces table-region MAE from 21.77 to
6.34 and reduces the mean orange-ball center error from 173.84 to 3.05 pixels,
confirming that the state constraints affect the generated trajectory. The
same outputs nevertheless contain colored high-frequency artifacts,
particularly after a constrained horizon ends.

We attribute this behavior primarily to an imperfect transfer of image-space
pseudoinverse guidance to Wan2.2's temporally compressed video latent. Its VAE
and video post-training do not ensure that independently encoded slot
measurements remain on the clean-video manifold expected by the denoiser and
decoder. Separate image- and latent-space MSE diagnostics further examine this
model-specific interpretation.
