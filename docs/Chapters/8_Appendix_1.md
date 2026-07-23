# Appendix 1: Pseudoinverse Interpretation and Approximation Details

> Status: initial technical appendix. The assumptions and approximation analysis
> should be revisited after the final FBFM implementation is frozen.

## Generalized-Inverse Consistency

Consider a noiseless linear measurement

\[
\mathbf{Y}_t=\mathbf{H}\mathbf{X}_t^1,
\]

where \(\mathbf{H}\) has linearly independent rows. Its Moore--Penrose
pseudoinverse is

\[
\mathbf{H}^\dagger
=
\mathbf{H}^{\mathsf T}
(\mathbf{H}\mathbf{H}^{\mathsf T})^{-1}.
\]

For a predicted clean endpoint \(\hat{\mathbf{X}}_t^1\), lifting the measurement
residual back to the generation space gives

\[
\mathbf{H}^\dagger
\left(
\mathbf{Y}_t-\mathbf{H}\hat{\mathbf{X}}_t^1
\right)
=
\mathbf{H}^\dagger\mathbf{Y}_t
-
\mathbf{H}^\dagger\mathbf{H}\hat{\mathbf{X}}_t^1.
\]

The matrix \(\mathbf{P}_{\mathbf H}=\mathbf{H}^\dagger\mathbf{H}\) is the
orthogonal projector onto the row space of \(\mathbf H\). Consequently,
pseudoinverse guidance compares only components that are recoverable from the
measurement.

For a nonlinear measurement operator \(h\), Song et al. (2023) require a generalized
inverse satisfying

\[
h\circ h^\dagger\circ h=h.
\]

We additionally use the reflexive consistency relation

\[
h^\dagger\circ h\circ h^\dagger=h^\dagger.
\]

These identities motivate the term *Moore--Penrose-consistent feedback
encoder--decoder pair*. They do not assert that arbitrary nonlinear maps possess a
global Moore--Penrose inverse. Rather, on the relevant data manifold, the encoder
and decoder preserve measurable content; under local linearization, the lifting is
modeled by the Moore--Penrose pseudoinverse of the measurement Jacobian.

## Masked Inpainting as a Projection

Let \(\mathbf M_t\) select the observed coordinates of a chunk:

\[
\mathbf Y_t=\mathbf M_t\mathbf X_t^1.
\]

When the rows of \(\mathbf M_t\) are selected canonical basis vectors, they are
orthonormal and

\[
\mathbf M_t^\dagger=\mathbf M_t^{\mathsf T}.
\]

Define the full-space binary mask weights \(\mathbf w_t\in\{0,1\}^D\) and their
diagonal operator \(\mathbf W_t\) by

\[
\mathbf W_t
=
\operatorname{Diag}(\mathbf w_t)
=
\mathbf M_t^{\mathsf T}\mathbf M_t
\]

and the zero-filled observation by
\(\bar{\mathbf Y}_t=\mathbf M_t^{\mathsf T}\mathbf Y_t\). Then

\[
\begin{aligned}
\mathbf M_t^\dagger
\left(
\mathbf Y_t-\mathbf M_t\hat{\mathbf X}_t^1
\right)
&=
\mathbf M_t^{\mathsf T}\mathbf Y_t
-
\mathbf M_t^{\mathsf T}\mathbf M_t\hat{\mathbf X}_t^1\\
&=
\mathbf W_t
\left(
\bar{\mathbf Y}_t-\hat{\mathbf X}_t^1
\right).
\end{aligned}
\]

Hence, binary coordinate inpainting is exactly a Moore--Penrose projection.
Replacing \(\mathbf w_t\in\{0,1\}^D\) with
\(\mathbf w_t\in[0,1]^D\), while retaining
\(\mathbf W_t=\operatorname{Diag}(\mathbf w_t)\), yields a confidence-weighted
relaxation; the resulting operator is generally no longer an orthogonal projector.

## Aligned-Coordinate Approximation

The exact lifted discrepancy used by pseudoinverse guidance is

\[
\mathbf e_{\mathrm{exact}}
=
\mathbf W_t
\left[
h^\dagger(\mathbf Y_t)
-
h^\dagger\!\left(h(\hat{\mathbf X}_t^1)\right)
\right].
\]

FBFM uses the aligned-coordinate approximation

\[
\mathbf e_{\mathrm{approx}}
=
\mathbf W_t
\left[
h^\dagger(\mathbf Y_t)
-
\hat{\mathbf X}_t^1
\right].
\]

Define the masked encoder--decoder reconstruction error

\[
\boldsymbol\delta_t
=
\mathbf W_t
\left[
h^\dagger\!\left(h(\hat{\mathbf X}_t^1)\right)
-
\hat{\mathbf X}_t^1
\right].
\]

The two discrepancies satisfy

\[
\mathbf e_{\mathrm{exact}}
=
\mathbf e_{\mathrm{approx}}-\boldsymbol\delta_t,
\qquad
\left\|
\mathbf e_{\mathrm{exact}}-\mathbf e_{\mathrm{approx}}
\right\|_2
=
\|\boldsymbol\delta_t\|_2.
\]

The approximation is therefore exact whenever \(h^\dagger\circ h\) is the identity
on the mask-selected coordinates, and its discrepancy is controlled directly by the
masked reconstruction error otherwise. This condition is plausible when feedback
values and model predictions have already been encoded into the same latent/action
coordinates, but it is not guaranteed for an arbitrary nonlinear encoder--decoder
pair.

## Few-Step Flow-Matching Guidance

With

\[
\hat{\mathbf X}_t^1
=
f_\theta^\tau(\mathbf X_t^\tau)
=
\mathbf X_t^\tau
+(1-\tau)v_\theta(\mathbf X_t^\tau,\tau;\mathcal H_t),
\]

the correction is computed as the VJP

\[
\mathbf g_t^\tau
=
\left(
\frac{\partial f_\theta^\tau(\mathbf X_t^\tau)}
     {\partial\mathbf X_t^\tau}
\right)^{\mathsf T}
\mathbf e_t^\tau.
\]

A practical weight schedule for few-step Flow-Matching solvers is

\[
\lambda_\tau
=
\min\!\left(
\beta,\frac{1-\tau}{\tau r_\tau^2}
\right),
\qquad
r_\tau^2
=
\frac{(1-\tau)^2}{\tau^2+(1-\tau)^2},
\]

where \(\beta\) clips the weight for numerical stability (Black et al., 2025).
Reverse-mode automatic differentiation evaluates the VJP through
\(f_\theta^\tau\); differentiability of \(h\) and \(h^\dagger\) is not required.
