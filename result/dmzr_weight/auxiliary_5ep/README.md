# DreamZero FBFM Three-Weight Auxiliary Sweep

Status: running on the NVIDIA RTX A6000 workstation.

This experiment tests whether DreamZero FBFM's state-modality preconditioner
explains the performance and numerical-stability differences observed on the
single-task diagnosis. It covers all ten `libero_spatial` tasks and all ten
`libero_object` tasks.

## Compared Weights

| Label | State preconditioner | Intended interpretation |
| --- | ---: | --- |
| Binary | `1.0` | No modality attenuation; every active state support has unit scale |
| RMS | `sqrt(56/9600) = 0.07637626158259733` | Equalize expected Euclidean energy under equal-variance coordinates |
| L1 mass | `56/9600 = 0.005833333333333334` | Equalize the sum of coordinate weights across modalities |

The hard-overlap support matrix `W` remains binary in every run. The fractional
value is a separate state-modality preconditioner and does not turn `W` into a
soft mask.

## Controlled Protocol

```text
suites: libero_spatial tasks 0-9; libero_object tasks 0-9
official init IDs: 0-4
episodes: 5 per task and weight; 100 per weight; 300 total
checkpoint: RLinf-DreamZero-WAN2.2-5B-LIBERO-SFT-Step26000
environment seed: 0
model seed: fixed 0
horizon: 480 environment steps
mode: FBFM pseudo_async_overlap
solver release: uniform
weight order: binary -> RMS -> L1 mass
hardware: NVIDIA RTX A6000 48 GB
```

All three weights run serially on the same GPU and exact code revision. This
avoids cross-device, precision, checkpoint-residency, and concurrent-load
confounds. The task order and official initial-state IDs are identical.

Five episodes per cell are an auxiliary screening experiment. Per-task rates
have 20-percentage-point resolution and wide uncertainty, so the analysis must
emphasize paired patterns, suite aggregates, numerical tails, and follow-up
candidates rather than treating each cell as a final benchmark estimate.

## Recording

The `data/` directory is synchronized from the A6000 every 30 minutes. It keeps
manifests, task tables, episode ledgers, and monitor history. Large trajectory
arrays, server logs, and solver audits remain on the workstation; their source
paths and checksums will be recorded after completion.

The final analysis will report:

- per-task successes out of five for every weight;
- suite and overall micro rates, plus task-macro rates;
- paired task and episode differences between weights;
- episode time and completion-time estimates;
- action/correction tail and server-error checks;
- a method-level interpretation of binary, RMS, and L1-mass scaling.

## Source Revision

```text
repository: StvLi/FBFM DreamZero-LIBERO integration
branch: fix/dreamzero-relinearized-unipc-guidance
run revision: a37fcf5fc05147d7b9cf6a18beb70c8f991fd52f
numerical-method revision: 13de791f74139b165cff70ff8165b1cc4538ea64
```

