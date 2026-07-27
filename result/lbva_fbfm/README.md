# LingBot-VA FBFM CPU-Render Results

## Result Snapshot

This directory records the completed portion of the LingBot-VA FBFM RoboTwin
CPU-render evaluation as synchronized on `2026-07-26T22:44:09+08:00`. A result
cell is the tuple `(config, task)` and requires exactly 10 episodes.

| Config | Complete cells | Successes / episodes | Micro success rate |
| --- | ---: | ---: | ---: |
| `demo_clean` | 17 | 145 / 170 | 85.29% |
| `demo_randomized` | 28 | 243 / 280 | 86.79% |
| **All complete cells** | **45** | **388 / 450** | **86.22%** |

The aggregate Wilson 95% confidence interval is 82.73%-89.10%. At snapshot
time, the 80 planned cells comprised 45 complete, 6 partially running, and 29
pending cells. Only the 45 complete cells contribute to the table above.

## Protocol and Provenance

- Model: LingBot-VA post-trained RoboTwin checkpoint, weights frozen
- Method: FBFM feedback evaluation
- Simulator/configs: RoboTwin `demo_clean` and `demo_randomized`, CPU rendering
- Episodes required per result cell: 10
- Evaluation revision: `a116e48d9c8956c7ee66360ae68007bc146abcc3`
- Checkpoint: `/mnt/project_eai_hs/zrm/lingbot-va/checkpoints/lingbot-va-posttrain-robotwin`
- Source root: `/mnt/project_eai_hs/zrm2/FBFM/wam/lingbot-va/robotwin_outputs/feedback_multinode_80cells_clean30_random50_10_a116e48`

The exact synchronized source table is retained without normalization in
`source_snapshot.tsv`. Absolute `res.json` paths are provenance references and
are not expected to resolve outside the evaluation host.

## Files

| File | Contents |
| --- | --- |
| `task_summary.csv` | complete cells, counts, rates, Wilson intervals, worker assignment, and source path |
| `cell_ledger.csv` | normalized ledger for all 80 planned cells, including incomplete states |
| `source_snapshot.tsv` | byte-preserved synchronized source table |
| `aggregate.json` | machine-readable protocol, coverage, grouped totals, and limitations |
| `SHA256SUMS` | integrity hashes for the packaged artifacts |

This snapshot contains task-level counts rather than per-episode outcome
records. It supports the reported aggregate and per-task rates, but it does not
support seed-level pairing or episode-identity audits.
