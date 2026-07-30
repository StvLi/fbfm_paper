# Experiment Results

This directory stores compact, reviewable LingBot-VA CPU-render evaluation
artifacts. Large videos, checkpoints, simulator caches, and server logs remain
in the experiment workspace and are not committed to the paper repository.

| Directory | Experiment | Final included state |
| --- | --- | --- |
| `lbva_fbfm/` | LingBot-VA with FBFM | 72/80 complete cells, 590/720 (81.94%); under-900 72/72 |
| `lbva_none/` | LingBot-VA without feedback | 57/66 complete cells, 411/570 (72.11%); under-900 52/52 |

Each experiment directory contains a human-readable record, a complete-cell
summary, the full planned-cell ledger, a structured aggregate, and SHA-256
hashes. Rates use only cells satisfying `status == complete && trials == 10`.
Tasks with `max_steps >= 900` were stopped by design; any already-completed
long-horizon cells remain visible in the all-complete totals.

The pooled method totals have different task/config coverage. Use the strict
48-cell matched under-900 comparison in
`lbva_fbfm/under900_20260729_a116e48/` when comparing methods descriptively.
