# FBFM Paper TODO

This file tracks paper-level revisions and consistency checks. Check an item only after the corresponding figure, text, and implementation claim have been verified together.

## Main Method Figures

### Shared notation

- [ ] Use `t` for environment/chunk time, `i` for a position within a chunk, and `\tau` for Flow-Matching time throughout all figures.
- [ ] Replace repeated `0` subscripts with indexed variables such as `\hat{Z}_{t,i}^{\tau}` and `\hat{A}_{t,i}^{\tau}`.
- [ ] Use `d\tau`, rather than `dt`, when integrating along Flow-Matching time.
- [ ] Typeset the pseudoinverse as `h^{\dagger}`; remove ambiguous `h+` notation.
- [ ] Make state, action, observed, predicted, constrained, and unconstrained slots visually distinguishable with one shared legend.
- [ ] Check that capitalization and hyphenation are consistent: `Flow Matching`, `World-Action Model`, and `Pseudoinverse-Guided`.

### Joint-generation figure (`material/parallel.jpg`)

- [ ] Rename the displayed paradigm to `Joint Generation` or `Joint Flow Matching`; avoid `parallel` in the paper text.
- [ ] Explicitly identify the joint flow variable as `X_t^\tau = [Z_t^\tau, A_t^\tau]`.
- [ ] Show that state and action observations share one mask and one joint Jacobian/VJP path.
- [ ] Clarify that a state residual may update both state and action components through the joint Jacobian.
- [ ] Replace or explain the database/cylinder icon so that its role is unambiguous.

### Stage-wise figure (`material/serial.png`)

- [ ] Rename the displayed paradigm to `Stage-wise Generation`, `Factorized Generation`, or `Sequential Denoising`; avoid using `serial` as the formal term.
- [ ] Label the two vector fields separately, e.g. `v_\theta^Z` and `v_\theta^A`.
- [ ] Show the conditioning path from the corrected frame prediction to the action-generation stage explicitly.
- [ ] Distinguish direct action feedback from the indirect effect of state feedback on actions.
- [ ] Replace `Hidden Markov Model` with a more precise label such as `Feedback Observation Model` or `Asynchronous Feedback Buffer`, unless an HMM is formally defined in the text.
- [ ] Keep the caption at the complete method level; disclose the current Lingbot-VA action-feedback status in Experiment and Result rather than adding implementation caveats to the Method figure.

## Mask and Guidance Figures

- [ ] Add a legend for mask values: `1` means observed/constrained and `0` means unavailable/unconstrained.
- [ ] Label the diagonal matrix as `W_t` and state its dimensions or block structure.
- [ ] Label the derivative block as the Jacobian/VJP of the predicted clean endpoint with respect to the current flow state.
- [ ] Explain why activating one observation row can affect multiple generated variables in the joint model.
- [ ] In the stage-wise version, keep the frame mask/Jacobian and action mask/Jacobian visibly separate.
- [ ] Show newly arriving observations updating the ongoing solver, as required by the complete Method; track the current implementation gap in `docs/handover.md` and report the realized schedule in Experiment and Result.
- [ ] Align colors, slot ordering, line styles, and tensor orientation with the two main method figures.
- [ ] Add final captions after the method notation is frozen.

## Writing Decisions

- [ ] Decide whether `Pseudoinverse-Guided Inpainting` belongs in Preliminaries or Method. Keep only background and established results in Preliminaries; place FBFM-specific adaptation and derivation in Method.
- [ ] Use `joint generation` and `stage-wise generation` as the two WAM architecture categories throughout the paper.
- [ ] Keep three concepts separate: generation architecture, feedback target, and asynchronous execution schedule.
- [x] Define the feedback-window boundary at each solver evaluation before making claims about online or asynchronous mask updates.
- [x] In Method, keep the solver-start interaction history \(\mathcal H_t\) separate from chunk-internal feedback that arrives during Flow Matching; represent the latter as a dynamic feedback set and time-varying mask containing newly encoded \(z_{t+i}\).
- [x] For a stage-wise WAM, specify that state feedback arriving after the state flow ends refreshes the state context consumed by the ongoing action flow, without binding Method to a model-specific cache implementation.
- [x] Define the previous-action target over the full aligned chunk overlap, including both executed and not-yet-executed committed actions; do not shrink it with the execution pointer.
- [x] For a joint-generation WAM, formulate one joint state-action flow and explicitly derive the direct action-coordinate correction \(\mathbf J_{ZA}^{\mathsf T}\mathbf e^Z\) induced by state feedback through the clean-endpoint VJP.
- [ ] Keep Method implementation-agnostic: use Lingbot-VA and DreamZero only to understand and instantiate the FBFM design; defer model-specific engineering details, configurations, and implementation behavior to Experiment and Result.
- [ ] Before finalizing Method, remove code-path-specific claims unless they define the general FBFM algorithm.

## Notation Audit

- [ ] Before freezing Preliminaries, verify that every mathematical symbol used in Sections 1.1--1.3 appears in Section 1.4 with a consistent definition, and remove entries that are not used.
- [ ] After Method is finalized, extend Section 1.4 with all method-specific symbols and repeat the whole-paper notation consistency audit.

## Paper-Implementation Consistency

- [ ] Verify the DreamZero implementation and experiments support joint state-action guidance claims.
- [ ] Enable and validate previous-action feedback in the Lingbot-VA server path before describing it as an implemented result.
- [ ] Replace the temporary Lingbot-VA "None" adapter mode with a formal path in which state feedback and previous-action constraints are both enabled.
- [ ] Make newly encoded state feedback visible to the currently active Flow-Matching solver, rather than only to a pre-inference snapshot or the next inference call.
- [ ] Do not use wall-clock concurrency in RoboTwin as a necessary validation condition for the general asynchronous Method; evaluate the intended feedback behavior under its controlled pseudo-asynchronous schedule.
- [ ] Track and close every P0 item in docs/handover.md before freezing the main Lingbot-VA experiments.
- [ ] In Experiment and Result, describe RoboTwin explicitly as pseudo-asynchronous: simulation progression and Flow-Matching denoising are coordinated through a controlled ratio of simulation steps to solver steps. Report that ratio and do not present this simulator-specific schedule as a restriction of the general Method.
- [ ] State the mapping between one latent-state feedback slot, raw observations, and low-level actions.
- [ ] Present the third, generalized previous-action-constraint formulation with \(\mathbf W_t^A\) in Method; in Experiment and Result, explicitly state that the current implementation evaluates only the first formulation, i.e., hard action-prefix masking.
- [ ] Audit the abstract, method, figures, and experiment section together after both implementation tracks stabilize.

## Theory and Limitations

- [ ] State in Conclusion and Limitations that the implementation approximates \(h^\dagger(h(\hat{\mathbf{X}}))\) by \(\hat{\mathbf{X}}\) on the mask-selected feedback subspace; this is not guaranteed for arbitrary nonlinear encoder--decoder pairs.
- [x] Move the detailed pseudoinverse, mask-projection, and approximation-error derivations into docs/Chapters/Appendix_1.
- [ ] Validate and finalize the Appendix 1 analysis of the masked reconstruction error \(\|\mathbf{W}\odot[h^\dagger(h(\hat{\mathbf{X}}))-\hat{\mathbf{X}}]\|\) after the implementation is frozen.
- [ ] Consider an ablation comparing the explicit encoder--decoder residual with the aligned-coordinate approximation if the full \(h/h^\dagger\) path is implemented.
