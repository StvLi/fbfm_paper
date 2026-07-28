# DreamZero FBFM LIBERO-40 formal run

- Route branch: `experiment/dreamzero-l1mass-state-weight`
- Route commit: `cb08c9e552730d26cc446885e79a3e270a270d0c`
- Observed remote branch head at launch: `0f2cc4f133532af16841b3698e7cc7a036cecdee`
- Outer integration runner: `8d4184f0ada01911d874853bdb3abacd6b536e04`
- External DreamZero base: `ab790c198fbce33503358efbbd4187ce9a89adf3`
- Mode: `FBFM`, rolling causal feedback, uniform one-grant-per-action release
- State weight: `56/9600 = 0.005833333333333334` (L1-mass default)
- Scope: `libero_spatial:0-9`, `libero_object:0-9`, `libero_goal:0-9`, `libero_10:0-9`
- Trials: official trial IDs `0-19`, 20 per task, 800 total episodes
- Seeds: environment seed `0`; fixed model seed `0`
- Horizon: 480 environment steps for every suite
- GPUs: physical GPU0-7, five disjoint tasks per GPU
- Ports: localhost `18900-18907`
- Checkpoint: `RLinf-DreamZero-WAN2.2-5B-LIBERO-SFT-Step26000`
- Output: `/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_feedback_cb08c9e_20260726/runs/formal_libero40_fbfm_l1mass_20_cb08c9e`

The route was fetched and pulled on `dreamzero-fbfm` through the user-provided
localhost proxy because `fbfm-lingbot-va` cannot reach GitHub directly. The
worktree was then detached at the requested commit. The external DreamZero
source is an isolated worktree containing the checked-in scheduler callback
patch plus the existing `skip_component_loading` deployment fix; the shared
DreamZero worktree was not modified.

Validation before launch:

- 30 route CPU tests passed.
- Eight tables-only shard preflights passed.
- Atomic aggregation validated exactly 40 unique tasks and 800 expected episodes.
- The checked-in legacy audit validator still assumes one state-target refresh per
  action. `runtime/validate_live_audit_cb08.py` instead validates the cb08c9e
  stride-3 contract documented by this branch: refreshes at offsets 3 and 6,
  context versions `0,0,1,1,1,2,2,2`, action mask 56, state slot 0, finite
  corrections, and no server error records.
