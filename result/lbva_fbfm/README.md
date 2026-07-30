# LingBot-VA FBFM CPU-Render Results

## Final Snapshot

This directory records the final completed portion of the LingBot-VA with FBFM feedback
RoboTwin CPU-render evaluation. The last canonical result was written at
`2026-07-30T03:41:38+08:00`. A result cell is `(config, task)` and requires exactly 10
seed-unique episodes.

| Config | Complete cells | Successes / episodes | Micro success rate |
| --- | ---: | ---: | ---: |
| `demo_clean` | 30 | 242 / 300 | 80.67% |
| `demo_randomized` | 42 | 348 / 420 | 82.86% |
| **All complete cells** | **72** | **590 / 720** | **81.94%** |

The aggregate Wilson 95% confidence interval is
78.97%-84.58%.
Coverage is 72/80 planned cells. Under the
predeclared `max_steps < 900` scope, coverage is 72/72
with 590/720 successes
(81.94%). All remaining incomplete cells have
`max_steps >= 900` and were stopped by design.

## Protocol and Provenance

- Model: LingBot-VA post-trained RoboTwin checkpoint, weights frozen
- Method: FBFM feedback evaluation
- Simulator/configs: RoboTwin `demo_clean` and `demo_randomized`, CPU rendering
- Episodes required per result cell: 10
- Evaluation revision: `a116e48d9c8956c7ee66360ae68007bc146abcc3`
- Checkpoint: `/mnt/project_eai_hs/zrm/lingbot-va/checkpoints/lingbot-va-posttrain-robotwin`
- Source root: `/mnt/project_eai_hs/zrm2/FBFM/wam/lingbot-va/robotwin_outputs/feedback_multinode_80cells_clean30_random50_10_a116e48`
- Canonical `res.json` archive SHA-256: `49bfec081cbc8f57af5a82ad728542c5870db21a0808374f9df4888187ac34d2`

`source_snapshot.tsv` was regenerated directly from canonical `res.json` files
and the original planned-cell metadata. Absolute source paths are provenance
references and are not expected to resolve outside the evaluation hosts.

## Files

| File | Contents |
| --- | --- |
| `task_summary.csv` | complete cells, counts, rates, Wilson intervals, and provenance |
| `cell_ledger.csv` | normalized ledger for every planned cell, including stopped long-horizon cells |
| `source_snapshot.tsv` | planned-cell snapshot regenerated from canonical results |
| `aggregate.json` | protocol, coverage, grouped totals, under-900 totals, and limitations |
| `SHA256SUMS` | integrity hashes for the packaged artifacts |

The seed-audited final under-900 package is in `under900_20260729_a116e48/`.
