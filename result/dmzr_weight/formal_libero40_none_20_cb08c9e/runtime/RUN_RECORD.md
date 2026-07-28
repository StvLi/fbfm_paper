# DreamZero NONE LIBERO-40 formal run

- Route branch: `experiment/dreamzero-l1mass-state-weight`
- Route commit: `cb08c9e552730d26cc446885e79a3e270a270d0c`
- Mode: `NONE`
- Scope: `libero_spatial:0-9`, `libero_object:0-9`, `libero_goal:0-9`, `libero_10:0-9`
- Trials: official trial IDs `0-19`, 20 per task, 800 total episodes
- Seeds: environment seed `0`; fixed model seed `0`
- Horizon: 480 environment steps for every suite
- GPUs: physical GPU0-7, five disjoint tasks per GPU
- Ports: localhost `18900-18907`
- Checkpoint: `RLinf-DreamZero-WAN2.2-5B-LIBERO-SFT-Step26000`
- Tokenizer: `umt5-xxl`
- Recorded state weight: `56/9600 = 0.005833333333333334`; ignored in `NONE` mode
- Output: `/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_none_cb08c9e_20260726/runs/formal_libero40_none_20_cb08c9e`

This run changes only the constraint mode from the completed FBFM run. It uses
the same source snapshots, external DreamZero integration, checkpoint, task
partition, trial IDs, seed rules, solver release policy, and uniform 480-step
horizon. The source and workspace directories are reused through read-only
symbolic links; runtime files, manifests, logs, and results are isolated under
the NONE run root.

The completed matched FBFM reference is:

`/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_feedback_cb08c9e_20260726/runs/formal_libero40_fbfm_l1mass_20_cb08c9e`

Validation required before launch:

- Route CPU tests: 30/30 passed on 2026-07-26.
- Eight tables-only shard preflights must pass.
- Atomic aggregation must validate exactly 40 unique tasks and 800 expected episodes.
- All eight GPUs and TCP ports 18900-18907 must be unused.

## Version audit (2026-07-26 23:13 CST)

The route-local method and entrypoint tree is an independent nested Git checkout,
not the outer FBFM worktree. Its resolved path is:

`/mnt/project_eai_hs/zrm2/eval_isolated/dreamzero_feedback_cb08c9e_20260726/source/FBFM/wam/dreamzero-libero`

Evidence:

- route HEAD: `cb08c9e552730d26cc446885e79a3e270a270d0c`
- route tree: `b00688b0745b7a750ea07d054f6de7c0b7796bc2`
- route status and `diff-index HEAD`: clean
- commit subject: `experiment(dreamzero): default to L1-mass state guidance`
- the server imports route `src/` first, then the outer FBFM adapter package;
  its command uses this route's `scripts/model_server.py`, `--mode NONE`, and
  the isolated base workspace. Clients call this route's unchanged
  `scripts/libero_experiment.py`.

The external files are deployment snapshots and are not objects inside the
standalone cb08c9e route commit:

- outer `fbfm/model_runtime.py`: Git blob
  `97223852b4af67e127bd4109132c55165dc8163e`, SHA-256
  `a9d97e3dc34c4f388e4f0fbe73ce34c45e5ca5ca7ea00fa31786d10604d77a27`
- outer `fbfm/libero_observation.py`: Git blob
  `e2f12dd1d270f5bbc85d8168d4febd3d4b252673`, SHA-256
  `b6da37296036dce2aef829202b8218c7c59744fa0ad54209e86581ec85067ff4`
- external DreamZero base: `ab790c198fbce33503358efbbd4187ce9a89adf3`;
  its action-head file contains the route-tracked external-step patch (verified
  by `git apply --reverse --check`) plus the pre-existing offline full-checkpoint
  component-loading guard. Current file blob:
  `40f859d0717161ed40319848178f2b34809c36ba`, SHA-256
  `55adc45be5333d932c75f8b60f14b852e39e4c7eb4ae5116c7ab878f0d5f7a91`.
- RLinf base: `0f9ea98c7a6d9e3ade24e8f4846c64d3b135dbcc`.

Therefore, the route-local FBFM method is byte-for-byte cb08c9e. The external
DreamZero/model-loader adapters are the same matched deployment snapshots used
by the completed cb08c9e FBFM reference; they must not be described as files
owned by the standalone cb08c9e commit. The additional DreamZero loading guard
controls offline component loading and does not change NONE guidance math.

The NONE-only harness lives outside the route checkout and changes orchestration
only: explicit disjoint task shards, contiguous-prefix resume, process/GPU/port
launching, and atomic cross-shard aggregation. It does not edit route `src/`,
`model_server.py`, or `libero_experiment.py`. Runtime SHA-256 hashes:

- `run_shard_benchmark.py`: `58a09d13611424aceed23895a8a0ad4ce3ac20162664b79950f956cf99751801`
- `aggregate_libero40_shards.py`: `242da64f266c5bffc94d0e7d99a9844ea98bec60dc5cc43d2cb10db4de4de82a`
- `run_worker.sh`: `40812e99660e90ef98457ca5c2eb72f19c28dcf74717846155f41446e3b28c78`
- `launch_all.sh`: `e246efc44b3ec806fc9d20aa80eb9dafcf2bd8a5c1e9c7b94d9628937196f11b`
- `monitor.sh`: `76476e8769141c06bcd31cf48a090dbc85f2367f9b7c080e489df2d2b4fee50b`

## Final result and integrity audit (2026-07-27 01:45 CST)

- Status: complete; all eight workers exited normally and released GPU memory.
- Coverage: 40/40 tasks, 20 trials per task, 800/800 episodes.
- Overall: 561 successes, 239 failures, 70.125% success rate.
- Suite rates: LIBERO-Spatial 157/200 (78.500%); LIBERO-Object
  146/200 (73.000%); LIBERO-Goal 137/200 (68.500%); LIBERO-10
  121/200 (60.500%).
- Independent audit: passed. It found 800 unique `(suite, task_id, trial_id)`
  identities, zero duplicate or missing trials, no malformed/non-ok/non-NONE
  records, and no non-finite actions. All 800 trajectory files exist and are
  non-empty. The atomic summary and both aggregate CSV files agree with the
  episode ledgers.
- Ordered episode-ledger SHA-256:
  `38ac76541ed90853322cacd90e10d16084c972e01200822d5e9928f469af8cba`.
- Final report: `runs/formal_libero40_none_20_cb08c9e/FINAL_REPORT.md`.
- Audit record: `runs/formal_libero40_none_20_cb08c9e/final_audit.json`.
- Artifact hashes: `runs/formal_libero40_none_20_cb08c9e/FINAL_SHA256SUMS.txt`.
