# DreamZero FBFM LIBERO-40 a051933 run

- Route branch: `experiment/dreamzero-l1mass-state-weight`
- Route commit: `a051933e2b058d74bb268e94080464569d99ce39`
- Outer integration runner: `8d4184f0ada01911d874853bdb3abacd6b536e04`
- Mode: `FBFM`, causal rolling feedback, uniform one-grant-per-action release
- State weight: `56/9600 = 0.005833333333333334`
- State feedback gain `kp`: `0.0486968`
- Effective state weight: `0.0002840646666666667`
- Scope: `libero_spatial:0-9`, `libero_object:0-9`, `libero_goal:0-9`, `libero_10:0-9`
- Trials: official trial IDs `0-19`, 20 per task, 800 total episodes
- Seeds: environment seed `0`; fixed model seed `0`
- Horizon: 480 environment steps for every suite
- GPUs: physical GPU0-7, five disjoint tasks per GPU
- Formal ports: localhost `19000-19007`
- Checkpoint: `RLinf-DreamZero-WAN2.2-5B-LIBERO-SFT-Step26000`
- Bundle SHA-256: `f493268785986bc88927ab8a840b167ae2cd528eb540c7f5be77231bfae9e4d3`
- Output: `/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_feedback_a051933_kp00486968_20260727/runs/formal_libero40_fbfm_kp00486968_20_a051933`
- Formal launch: `2026-07-27T16:59:32+08:00`

The route is deployed from a complete Git bundle and detached at the exact
requested commit. The outer runner and external DreamZero deployment remain
isolated from other evaluations.

## Pre-launch verification

- Route CPU suite: `38/38` passed.
- Checkpoint: 1,828 tensors across six safetensor shards; tokenizer present.
- Eight tables-only shard preflights passed, covering 40 unique tasks and 800
  expected episodes without overlap.
- GPU smoke: `libero_spatial:1`, trial 0, `1/1` success in 167 executed steps;
  20 complete asynchronous chunks and 160 solver steps audited with zero
  server errors and finite actions.
- Every manifest and smoke runtime record contains mode `FBFM`, `kp=0.0486968`,
  commit `a051933e2b058d74bb268e94080464569d99ce39`, and effective state weight
  `0.0002840646666666667`.

## Formal initial status

- Eight model servers became ready on ports `19000-19007`; all eight
  `ready.json` files exactly matched the requested mode, state weight, `kp`,
  and effective state weight.
- Eight benchmark clients started, one per physical GPU. Each shard completed
  at least one episode with `actions_finite=true` before the run was handed
  to the atomic monitor.
- At `2026-07-27T17:15:53+08:00`, the aggregate was still growing at `25/800`
  episodes with 22 successes; all eight servers and clients were alive.
- Gain-aware live audit: 8/8 workers passed across 636 complete asynchronous
  chunks and 5,088 solver steps. No server errors, failed markers, traceback,
  OOM, non-finite action, or protocol mismatch was found.

## Runtime SHA-256

- `launch_all.sh`: `9969f529cdf15cdd3a362e300f656649c5ec852c8a5714621db42ab2e39e0a9e`
- `run_worker.sh`: `f84fee95dcae57c58b47b97a03759cbfda86e3c5871a1c6b2acaaa73045aa527`
- `monitor.sh`: `afc18f262a85323d812a5b4be3242e0785d4360b9ffc3b87b09c176241ddeda8`
- `aggregate_libero40_shards.py`: `6c9be1a957b43e5ec170d8cd8205bdee2fb4ed2fbcbeb8a7e5eaeab26fdacef3`
- `validate_live_audit_a051.py`: `419f12cded1b8911976c0a5d2bbe35224f03120b74faa00c0c536608143aced0`

## Recovery on 2026-07-27

- The original processes stopped at approximately `2026-07-27T17:18:20+08:00`
  when the development-machine container was stopped. The host itself did not
  reboot, and no application failure, traceback, or kernel OOM record was found.
- Raw shard records contained 37 unique, finite episodes. The aggregate had
  only reported 36 because the monitor stopped before its next refresh.
- Resume-prefix validation passed on all shards. Their first task resumed at
  trial IDs `5,5,7,3,3,2,5,7` for GPU0-7 respectively, with no duplicate trial.
- A PID-1-managed runit service resumed the evaluation at
  `2026-07-27T21:14:28+08:00`. All eight servers became ready with the exact
  requested parameters, and all eight benchmark clients resumed.
- At `2026-07-27T21:32:18+08:00`, the aggregate had grown to `47/800` episodes
  with 44 successes. Eight servers, eight clients, the monitor, and the runit
  supervisor were alive; failed markers and log error hits were zero.
- The post-recovery live audit passed on 8/8 workers across 1,170 complete
  asynchronous chunks and 9,360 solver steps.
- `persistent_supervisor.sh` SHA-256:
  `39092c0e505da5a3feacdb9d9a0b3ec56b7483ab1e97f64ff646893787db153e`.

The runit registration lives in the current container's tmpfs. Completed
episodes and the supervisor script live on shared storage, but another full
container recreation would require re-registering the runit service before
automatic resume.
