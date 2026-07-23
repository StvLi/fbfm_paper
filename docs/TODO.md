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

- [ ] Before freezing Preliminaries, verify that every mathematical symbol used there appears in Appendix A with a consistent definition, and remove entries that are not used.
- [ ] After Method is finalized, extend the Appendix A notation index with all method-specific symbols and repeat the whole-paper notation consistency audit.

## Introduction and Related Works Audit

### Introduction scope and claims

- [ ] Keep the Introduction-level FBFM description consistent with Method: feedback arriving during generation must update the target and mask before subsequent evaluations of the active solver, rather than being described as a fixed pre-inference snapshot for the next call.
- [ ] Present latent-state feedback and previous-action consistency as the two symmetric components of complete FBFM, while making the increment over RTC precise: RTC constrains overlapping action coordinates, whereas FBFM additionally treats newly observed latent states as time-aligned measurements of the generated WAM future.
- [ ] Describe both stage-wise-generation and joint-generation instantiations at the architecture level. Keep model-specific buffers, VAE streams, cache handling, and runtime plumbing out of Introduction; place general mechanisms in Method and realized configurations in Experiments.
- [ ] Keep the Introduction focused on the WAM-specific temporal-granularity gap. Move detailed comparisons, implementation differences, and judgments about prior methods to Related Works.
- [ ] Remove or qualify broad architectural claims such as `dominant`, `exclusive conditioning`, or universal KV-cache replacement unless the cited models directly support them.

### Literature-specific checks

- [ ] Build the final Related Works bibliography from `docs/Related_Works_Literature_Map.md`: verify author order, title, venue/year, arXiv version, and a stable BibTeX key for every retained citation; do not promote metadata-only notes into strong claims without checking the paper text.
- [ ] Organize Related Works as three internal thematic blocks without necessarily exposing subsection headings: generative modeling/world models; diffusion and Flow-Matching robot policies; inference-time guidance/asynchronous feedback. Ensure each citation supports a sentence in this argument rather than appearing as an isolated literature list.
- [ ] In the world-model background, keep two historically distinct lines explicit: latent dynamics and imagined control; diffusion/flow-based visual generation. Explain their convergence in WAMs, and relate the evolution of latent state representations to FBFM's choice to apply state feedback after encoding.
- [ ] Use grouped citations only after stating a shared field objective or method family. Give direct predecessors such as PiGDM, flow-based inverse guidance, RTC, and concurrent WAM-feedback methods independent multi-sentence comparisons covering their problem, mechanism, scope, and difference from FBFM.
- [ ] Apply a contribution-first comparison style to close prior work: state what the method enables before delimiting its feedback target, temporal granularity, training requirement, or architectural scope; audit unsupported absolute terms including `first`, `only`, `all`, `dominant`, `hard constraint`, and `guarantee`.
- [ ] **RTC / Real-Time Chunking (Black et al., 2025):** verify the hard-prefix and soft-overlap masks, inference-delay assumptions, pseudoinverse-guided VJP, and training-free scope; use it as the action-overlap baseline without attributing latent-state feedback to RTC.
- [ ] **BID / Bidirectional Decoding:** read the latest arXiv revision in addition to the version cited by RTC; verify the guided test-time sampling/rejection mechanism and avoid relying on the older subtitle alone.
- [ ] **Fast-WAM:** locate and verify the exact paper, its training-time video-co-training result, and whether the inference-time-imagination comparison is necessary in Introduction or belongs only in Related Works.
- [ ] **Feedback World Model (FWM):** verify the auxiliary feedback-state definition, prediction--observation residual, update timing, frozen-model claim, and one-step/task-specific scope before contrasting it with slot-aligned WAM future feedback.
- [ ] **RA-DP:** verify its environment-interleaved denoising schedule, action-space feedback/cost mechanism, heterogeneous-noise training requirement, and applicability boundary before using it as a contrast.
- [ ] **DynaGuide, AsyncVLA, TIDAL, and DCDP:** audit their external-model requirements, asynchronous schedules, dynamic-correction interfaces, and exact training-free boundaries before comparing them with inference-time FBFM.
- [ ] **WA-LQR / Steering Robustness into WAMs (Hong et al., 2026):** read the full paper and assess its activation-steering and reduced-order optimal-control formulation, its reported LingBot-VA steerability result, and its novelty overlap with training-free WAM feedback.
- [ ] **Lingbot-VA and DreamZero:** verify the exact generation factorization, conditioning interfaces, and history/cache update behavior of each cited implementation; use them as examples of stage-wise generation and joint generation without generalizing model-specific behavior to all WAMs.
- [ ] When citing LingBot-VA, keep its paper claim and released-code behavior separate: Related Works may describe the paper's unified autoregressive video-action formulation, while Experiments must report the audited frame-first/action-second inference path in upstream commit `7c6ffa9bfc4b83582cafc860fab4c82cc7deeeeb`.
- [ ] **Pseudoinverse-Guided Diffusion and Flow-Matching inpainting:** keep Song et al. as the source of pseudoinverse guidance, distinguish established inverse-problem background from the FBFM adaptation, and ensure the RTC lineage is cited accurately.

## Experiment and Result: Engineering Checklist

### Reproducibility boundary

- [ ] Report the exact experimental code commits, upstream model versions, checkpoints, dependency environment, accelerator hardware, and random seeds for the Lingbot-VA and DreamZero tracks; retain `3604b457a24485cddf326a997e48955b7ca6b548` as the current theory-audit baseline, not automatically as the final experiment commit.
- [ ] Separate base-model preparation from the training-free claim: report each WAM checkpoint's pretraining/post-training or task-fine-tuning data and steps, then verify that adding FBFM keeps that checkpoint frozen and introduces no additional training.
- [ ] Record the model-specific inference configuration needed to reproduce each result: chunk/state/action horizons and shapes, solver and scheduler type, state/action/joint Flow-Matching step counts, CFG scales if used, precision, and batch settings.

### Architecture-specific integration

- [ ] For Lingbot-VA, document the state-first/action-second inference order, the corrected-state-context handoff to the action stage, and how late state feedback refreshes that context without presenting cache mechanics as part of the general Method.
- [ ] Enable and validate previous-action feedback in the Lingbot-VA server path; replace the temporary `None` adapter mode so the reported full method contains both state feedback and previous-action constraints.
- [ ] Make newly encoded state feedback visible to the currently active Lingbot-VA Flow-Matching solver rather than only to a pre-inference snapshot or the next inference call.
- [ ] For DreamZero, verify and document the joint \(\mathbf X=[\mathbf Z,\mathbf A]\) ordering, joint target/mask construction, and the direct state-to-action correction through the cross-modal endpoint Jacobian.
- [ ] Keep all model/checkpoint-specific engineering details in Experiment and Result; Method should retain only the general stage-wise and joint-generation interfaces.

### Temporal and data alignment

- [ ] Report action/control frequency, sensor frequency, observation-window construction, encoder/latent temporal downsampling, actions per latent-state slot, and the exact mapping among raw observations, \(z_{t+i}\), feedback slots, and low-level actions.
- [ ] Report chunk horizon, overlap length, inference-delay assumption, global-time alignment between consecutive chunks, chunk handoff rule, and which preceding-chunk actions form the committed target for the new chunk.
- [ ] State explicitly that the committed action-overlap target includes both executed and not-yet-executed actions and remains fixed during generation; the execution pointer does not shrink the action mask.
- [ ] Describe RoboTwin explicitly as pseudo-asynchronous: report the controlled ratio of simulation steps to solver steps, inference trigger, feedback-delivery point, and result-handoff schedule. Do not require wall-clock concurrency as validation of the general Method.
- [ ] Document the realized runtime topology at a high level (simulator/environment loop, policy server/client, feedback buffer or queue, and synchronization boundary), including any communication assumptions that affect feedback timing.
- [ ] If physical-robot results remain in the paper, separately report the real execution/inference concurrency mechanism, sensor-to-action timing, feedback latency, control rate, safety policy, and deployment hardware.
- [ ] Specify the synchronization or versioning rule by which feedback arriving before solver evaluation \(k\) becomes visible at that evaluation, including how late feedback updates stage-wise action context.

### Feedback and guidance implementation

- [ ] Document the observation/sensor and encoder path used to construct latent state feedback, including the implemented interpretation of \(h\) and \(h^\dagger\) and the aligned-coordinate approximation \(h^\dagger(h(\hat{\mathbf X}))\approx\hat{\mathbf X}\).
- [ ] Report how \(\mathbf Y_{t,k}^Z\) and the dynamic state mask \(\mathbf W_{t,k}^Z\) are initialized, aligned, refreshed, and retained at every solver evaluation.
- [ ] Report how \(\mathbf Y_t^A\) and \(\mathbf W_t^A\) are constructed from the preceding chunk. State explicitly that the experiments evaluate hard action-prefix masking only, while Method gives the third, generalized weighting formulation.
- [ ] Report all guidance and numerical settings: \(\lambda_\tau\) schedule, maximum guidance weight/clipping, state/action modality weights, solver-step placement of the VJP, and any stability safeguards.
- [ ] Log enough internal evidence to verify the claimed mechanism: inference/chunk id, solver-step id, feedback version, activated state/action slots, masks, and state/action correction norms. For the joint model, verify a state-only residual can produce a nonzero action-coordinate correction.

### Evaluation and reporting

- [ ] Define all evaluated LIBERO and RoboTwin tasks, benchmark suites and versions, number of trials and seeds, initial-state sampling, success/failure criteria, aggregation, uncertainty reporting, and any excluded or retried runs.
- [ ] Keep baseline comparisons fair by using matched checkpoints, observations, action horizons, solver budgets, and execution schedules. Define the intended Original WAM, RTC/action-overlap-only, and full FBFM variants precisely, and record the RTC implementation provenance and any adaptation from the LeRobot reference.
- [ ] Include at least state-only, action-only, and state+action ablations; consider overlap length, pseudo-asynchronous step ratio/feedback timing, and guidance strength ablations where they support the main claims.
- [ ] If the latent-state diagnostic is retained, define the prediction target, encoder/checkpoint, compared post-training levels, latent-state MSE computation, test trajectories, and aggregation; distinguish improved prediction accuracy from faster Flow-Matching convergence.
- [ ] If the chunk-internal robustness study is retained, define a reproducible disturbance/intervention protocol, its timing within the chunk, the Original WAM/RTC/FBFM comparison, and response or recovery metrics for simulation and/or physical deployment.
- [ ] Report task success together with the efficiency cost of FBFM, including inference time or throughput, VJP overhead, peak memory, and effective control/update rate.
- [ ] Validate the locked OpenReview Abstract claim that FBFM improves success rates by more than 5% on the selected LIBERO and RoboTwin tasks; report the per-task values and the exact baseline used for each improvement.
- [ ] If physical-robot tracking remains an Abstract claim, define the platform, tasks, trial count, baseline, tracking metric, and quantitative result; otherwise remove or weaken that claim before submission.
- [ ] Track and close both confirmed issues in `docs/handover.md` before freezing the main Lingbot-VA experiments, and keep any newly confirmed code--theory mismatch equally concise there.
- [ ] Audit Abstract, Introduction, Method, figures, Experiment and Result, Conclusion, and implementation evidence together after both model tracks stabilize; do not let planned or unverified capabilities appear as completed results.

## Theory and Limitations

- [ ] State in Conclusion and Limitations that the implementation approximates \(h^\dagger(h(\hat{\mathbf{X}}))\) by \(\hat{\mathbf{X}}\) on the mask-selected feedback subspace; this is not guaranteed for arbitrary nonlinear encoder--decoder pairs.
- [x] Move the detailed pseudoinverse, mask-projection, and approximation-error derivations into `docs/Chapters/9_Appendix_2` (Appendix B).
- [ ] Validate and finalize the Appendix B analysis of the masked reconstruction error \(\|\mathbf{W}[h^\dagger(h(\hat{\mathbf{X}}))-\hat{\mathbf{X}}]\|\) after the implementation is frozen.
- [ ] Consider an ablation comparing the explicit encoder--decoder residual with the aligned-coordinate approximation if the full \(h/h^\dagger\) path is implemented.

## Final Whole-Paper Consistency Pass

- [ ] As the final editing pass, audit the exact wording, capitalization, hyphenation, and abbreviation of every professional concept across all editable sections, figures, captions, tables, appendix, and references. Treat the OpenReview-aligned title and Abstract as locked text; elsewhere, use `stage-wise generation` and `joint generation` consistently and eliminate competing labels such as `serial`, `parallel`, `cascaded dual-stream`, and `unified joint-prediction` unless they are explicitly introduced as informal explanations.
