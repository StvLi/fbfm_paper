# Appendix A: Notation Index

For quick reference, the first table indexes the core notation introduced in
Preliminaries, and the second lists the extensions used by the stage-wise and
joint-generation FBFM formulations.

| Symbol | Definition |
|---|---|
| \(T,\mathcal{T},c_T,\rho_T\) | A task, the task family, the condition associated with task \(T\), and its initial-state distribution. |
| \(\mathcal{M},\mathcal{S},\mathcal{A},P\) | The controlled Markov process, environment state space, action space, and transition kernel. |
| \(t,i,s_t\) | Environment time, an offset within a chunk, and the physical environment state. |
| \(\mathcal{O},E,\mathcal{H}_t,\pi\) | Sensor mapping, perceptual encoder, interaction history at time \(t\), and the action-selection process. |
| \(H,d_a,d_z,D_A,D_Z,D_X,D\) | Prediction horizon; dimensions of one action and one latent state; time-stacked action, state, and joint chunk dimensions, where \(D_A=Hd_a\), \(D_Z=Hd_z\), and \(D_X=D_Z+D_A\); and a generic generation-space dimension. |
| \(a_t,\mathbf{A}_t\) | A single-step action and its time-stacked action chunk vector. |
| \(z_t,\mathbf{Z}_t,\mathcal{Z}\) | An encoded single-step latent state, its time-stacked future latent-state chunk vector, and the latent space. |
| \(x,\mathbf{X}_t\) | A generic single-step variable and its chunk-level representation; instantiated as \(a/\mathbf A\), \(z/\mathbf Z\), or a joint state-action chunk. |
| \(\hat{\cdot},p_\theta,\theta\) | A predicted or estimated quantity, the conditional WAM distribution, and its model parameters. |
| \(\tau,k,\tau_k,\Delta\tau_k,\sigma\) | Continuous flow time, solver-step index, the corresponding flow-time point and integration step, and the remaining noise level \(\sigma=1-\tau\). |
| \(\boldsymbol{\epsilon},\mathbf{0},\mathbf{I},\mathbf{X}_t^\tau\) | Gaussian source noise, zero vector, identity matrix, and the intermediate chunk vector on the probability path. |
| \(\mathbf{u},v_\theta,\tilde v_\theta\) | Conditional target velocity, learned Flow-Matching vector field, and its noise-level parameterization \(\tilde v_\theta=-v_\theta\). |
| \(\mathcal{D},p(\tau),\mathcal{L}_{\mathrm{FM}}\) | Training distribution, flow-time sampling distribution, and Flow-Matching objective. |
| \(\hat{\mathbf{X}}_t,\hat{\mathbf{X}}_t^1,f_\theta^\tau\) | Generated chunk, predicted clean endpoint, and the endpoint predictor evaluated at flow time \(\tau\). |
| \(\mathbf{Y}_t,\mathcal{X},\mathcal{Y},h,h^\dagger\) | Feedback measurement, generation and measurement spaces, feedback encoder, and generalized lifting decoder. |
| \(\boldsymbol{\eta},\sigma_y\) | Measurement noise and its standard deviation. |
| \(\mathbf w_t,\mathbf W_t\) | Element-wise feedback mask or confidence weights and the corresponding diagonal weighting operator \(\mathbf W_t=\operatorname{Diag}(\mathbf w_t)\). |
| \(\mathbf{e}_t^\tau,\mathbf{g}_t^\tau\) | Masked lifted discrepancy and its vector--Jacobian product with respect to the current flow variable. |
| \(v_{\mathrm{PG}},\lambda_\tau\) | Pseudoinverse-guided velocity field and its time-dependent guidance strength. |

Method-specific extensions:

| Symbol | Definition |
|---|---|
| \(\mathcal I_t^A,a_{t+i}^{\mathrm{prev}}\) | The action-slot overlap between the preceding and new chunks, and the preceding chunk's action aligned to an overlap slot. |
| \(\mathcal F_{t,k}\) | Dynamic set of encoded real-state feedback available before solver evaluation \(k\), kept separate from the solver-start history \(\mathcal H_t\). |
| \(\theta_Z,\theta_A,v_{\theta_Z}^Z,v_{\theta_A}^A\) | Frozen parameters and separate state/action vector fields of a stage-wise WAM. |
| \(\tau_k^Z,\tau_k^A,f_{\theta_Z}^{Z,\tau_k^Z},f_{\theta_A}^{A,\tau_k^A}\) | State/action flow times and their clean-endpoint predictors at solver evaluation \(k\). |
| \(\mathbf Y_{t,k}^Z,\mathbf W_{t,k}^Z,w_{t,i}^{Z,k}\) | Aligned dynamic state-feedback target, its block mask/weighting operator, and the weight for state slot \(i\). |
| \(\mathbf Y_t^A,\mathbf W_t^A\) | Aligned committed-action target and the general previous-action weighting operator over the cross-chunk overlap. |
| \(\hat{\mathbf Z}_t,\check{\mathbf Z}_{t,k},\Phi_Z,\mathcal C_{t,k}^Z\) | Generated state endpoint, its latest feedback-refreshed representation, the native state-context constructor, and the context supplied to the action flow. |
| \(\mathbf e_{t,k}^Z,\mathbf e_{t,k}^A,\mathbf g_{t,k}^Z,\mathbf g_{t,k}^A\) | State/action discrepancies and their corresponding VJPs. |
| \(v_{\mathrm{FBFM}}^Z,v_{\mathrm{FBFM}}^A,\lambda_{\tau_k^Z}^Z,\lambda_{\tau_k^A}^A\) | State/action FBFM-guided vector fields and their guidance strengths. |
| \(\tau_k^X,v_\theta^X,f_\theta^{X,\tau_k^X}\) | Joint flow time, vector field, and clean-endpoint predictor at solver evaluation \(k\). |
| \(\mathbf Y_{t,k}^X,\mathbf W_{t,k}^X,\mathbf e_{t,k}^X,\mathbf g_{t,k}^X\) | Joint feedback target, block weighting operator, discrepancy, and VJP correction. |
| \(v_{\mathrm{FBFM}}^X,\lambda_{\tau_k^X}^X\) | FBFM-guided joint vector field and its guidance strength. |
| \(\mathbf J_{t,k}^X,\mathbf J_{QR}\) | Joint clean-endpoint Jacobian and its output-modality/input-modality block, where \(Q,R\in\{Z,A\}\). |
| \(\otimes,\mathbb 1[\cdot]\) | Kronecker product and indicator function. |
