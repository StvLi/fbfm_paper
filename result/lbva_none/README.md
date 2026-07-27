# LingBot-VA NONE CPU-Render Results

## Result Snapshot

This directory records the completed portion of the LingBot-VA no-feedback
RoboTwin CPU-render evaluation as synchronized on
`2026-07-26T22:44:09+08:00`. A result cell is the tuple `(config, task)` and
requires exactly 10 episodes.

| Config | Complete cells | Successes / episodes | Micro success rate |
| --- | ---: | ---: | ---: |
| `demo_clean` | 29 | 205 / 290 | 70.69% |
| `demo_randomized` | 8 | 58 / 80 | 72.50% |
| **All complete cells** | **37** | **263 / 370** | **71.08%** |

The aggregate Wilson 95% confidence interval is 66.26%-75.47%. At snapshot
time, the 66 planned cells comprised 37 complete, 2 partially running, 1
running without a recorded episode, and 26 pending cells. Only the 37 complete
cells contribute to the table above.

## Protocol and Provenance

- Model: LingBot-VA post-trained RoboTwin checkpoint, weights frozen
- Method: native inference without feedback (`constraint_mode=None`)
- Simulator/configs: RoboTwin `demo_clean` and `demo_randomized`, CPU rendering
- Episodes required per result cell: 10
- Evaluation revision: `a116e48d9c8956c7ee66360ae68007bc146abcc3`
- Checkpoint: `/mnt/project_eai_hs/zrm/lingbot-va/checkpoints/lingbot-va-posttrain-robotwin`
- Source root: `/mnt/project_eai_hs/zrm2/FBFM/wam/lingbot-va/robotwin_outputs/base_none_remaining33_clean_random_10_a116e48`

The exact synchronized source table is retained without normalization in
`source_snapshot.tsv`. Absolute `res.json` paths are provenance references and
are not expected to resolve outside the evaluation host.

## Files

| File | Contents |
| --- | --- |
| `task_summary.csv` | complete cells, counts, rates, Wilson intervals, and source path |
| `cell_ledger.csv` | normalized ledger for all 66 planned cells, including incomplete states |
| `source_snapshot.tsv` | byte-preserved synchronized source table |
| `aggregate.json` | machine-readable protocol, coverage, grouped totals, and limitations |
| `SHA256SUMS` | integrity hashes for the packaged artifacts |

This snapshot contains task-level counts rather than per-episode outcome
records. It supports the reported aggregate and per-task rates, but it does not
support seed-level pairing or episode-identity audits.
