# LingBot-VA NONE CPU-Render Results

## Final Snapshot

This directory records the final completed portion of the LingBot-VA without feedback
RoboTwin CPU-render evaluation. The last canonical result was written at
`2026-07-30T03:41:38+08:00`. A result cell is `(config, task)` and requires exactly 10
seed-unique episodes.

| Config | Complete cells | Successes / episodes | Micro success rate |
| --- | ---: | ---: | ---: |
| `demo_clean` | 29 | 205 / 290 | 70.69% |
| `demo_randomized` | 28 | 206 / 280 | 73.57% |
| **All complete cells** | **57** | **411 / 570** | **72.11%** |

The aggregate Wilson 95% confidence interval is
68.28%-75.63%.
Coverage is 57/66 planned cells. Under the
predeclared `max_steps < 900` scope, coverage is 52/52
with 390/520 successes
(75.00%). All remaining incomplete cells have
`max_steps >= 900` and were stopped by design.

## Protocol and Provenance

- Model: LingBot-VA post-trained RoboTwin checkpoint, weights frozen
- Method: native inference without feedback (`constraint_mode=None`)
- Simulator/configs: RoboTwin `demo_clean` and `demo_randomized`, CPU rendering
- Episodes required per result cell: 10
- Evaluation revision: `a116e48d9c8956c7ee66360ae68007bc146abcc3`
- Checkpoint: `/mnt/project_eai_hs/zrm/lingbot-va/checkpoints/lingbot-va-posttrain-robotwin`
- Source root: `/mnt/project_eai_hs/zrm2/FBFM/wam/lingbot-va/robotwin_outputs/base_none_remaining33_clean_random_10_a116e48`
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
