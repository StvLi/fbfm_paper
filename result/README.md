# Experiment Results

This directory stores compact, reviewable LingBot-VA CPU-render evaluation
artifacts. Large videos, checkpoints, simulator caches, and server logs remain in
the experiment workspace and are not committed to the paper repository.

| Directory | Experiment | Included result state |
| --- | --- | --- |
| `lbva_fbfm/` | LingBot-VA with FBFM on RoboTwin | original 45-cell snapshot plus a seed-audited under-900 follow-up |
| `lbva_none/` | LingBot-VA without feedback on RoboTwin | 37 complete 10-episode cells |

Each experiment directory contains a human-readable record, a complete-cell
summary, the full snapshot ledger, a structured aggregate, and SHA-256 hashes.
Rates use only cells satisfying `status == complete && trials == 10`. Partial,
running, and pending cells remain visible in the ledgers but are excluded from
reported rates.

The two snapshots contain different task/config coverage. Their pooled rates are
therefore descriptive and must not be treated as a matched FBFM-versus-NONE
treatment comparison.
