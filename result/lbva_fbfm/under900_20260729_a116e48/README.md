# LingBot-VA FBFM CPU-Render Under-900 Snapshot

> **Dataset identity:** this is a LingBot-VA + FBFM **RoboTwin** CPU-render
> snapshot, not a LIBERO evaluation. It contains two partial `handover_block`
> cells and therefore must not be treated as a fully completed benchmark or
> pooled without the complete-cell rule below.

Read-only snapshot captured at `2026-07-29T18:18:52.331311+08:00` from evaluation commit `a116e48d9c8956c7ee66360ae68007bc146abcc3`.
Only cells with `max_steps < 900` are reported; tasks at 900 steps or above are excluded.

- Imported from branch: `exp/lbva_fbfm_cpurender_result`
- Source paper-record commit: `44855bbd415e97001853e219ccb035fa27778942`

## Progress

| View | Complete cells | Successes / effective episodes | Notes |
| --- | ---: | ---: | --- |
| Official progress script | 13/15 | 107/134 | canonical/main selection |
| Including unpromoted unique shards | 13/15 | 108/140 | seed-deduplicated |

The effective view adds 6 unique episodes and 1 success. Five promoted shard cells are counted from canonical only.

## Requested FBFM Results

| Task | Clean | Randomized |
| --- | ---: | ---: |
| `handover_block` | 1/6 (16.67%, partial) | 0/4 (0.00%, partial) |
| `place_cans_plasticbox` | 10/10 (100.00%, complete) | 10/10 (100.00%, complete) |
| `stack_blocks_two` | 10/10 (100.00%, complete) | 8/10 (80.00%, complete) |
| `open_laptop` | 9/10 (90.00%, complete) | 9/10 (90.00%, complete) |
| `place_bread_basket` | 5/10 (50.00%, complete) | 9/10 (90.00%, complete) |
| `place_can_basket` | 10/10 (100.00%, complete) | 9/10 (90.00%, complete) |
| `place_object_basket` | 8/10 (80.00%, complete) | 7/10 (70.00%, complete) |
| `put_object_cabinet` | 6/10 (60.00%, complete) | 7/10 (70.00%, complete) |
| `shake_bottle` | 10/10 (100.00%, complete) | 10/10 (100.00%, complete) |
| `shake_bottle_horizontally` | 10/10 (100.00%, complete) | 10/10 (100.00%, complete) |
| `dump_bin_bigbin` | 10/10 (100.00%, complete) | 10/10 (100.00%, complete) |
| `handover_mic` | 10/10 (100.00%, complete) | 8/10 (80.00%, complete) |
| `place_dual_shoes` | 1/10 (10.00%, complete) | 1/10 (10.00%, complete) |
| `place_bread_skillet` | 7/10 (70.00%, complete) | 7/10 (70.00%, complete) |

Additional randomized cells:

| Task | Randomized |
| --- | ---: |
| `place_burger_fries` | 10/10 (100.00%, complete) |
| `place_empty_cup` | 10/10 (100.00%, complete) |
| `place_shoe` | 5/10 (50.00%, complete) |
| `scan_object` | 8/10 (80.00%, complete) |

## Incomplete Cells and Workers

- `demo_clean/handover_block`: 1/6, missing 4 trials.
- `demo_randomized/handover_block`: 0/4, missing 6 trials.
- Seven matching client workers were alive across the main and shard runs; no `.failed` marker was present.

## Deduplication and Provenance

The audit follows the production merger: episodes are keyed by true `seed` within each `(mode, config, task)` cell; duplicate seeds must agree on `instruction` and `success`; the first ten unique seeds in ascending order are selected. Once a shard cell appears in `promotions.tsv`, canonical is authoritative and shard records are not counted again.

`raw/` retains all 72 canonical, 14 main, and 14 shard `res.json` objects as JSONL, including source paths. `effective_trials.csv` records every selected requested trial and its source. Videos, checkpoints, simulator caches, and verbose logs remain on the evaluation hosts.

## Import Integrity Note

The source checksum manifest was calculated from CRLF text files, while Git
stored nine of them with normalized LF endings. Their checksums were regenerated
against the committed representation during import; experiment values and
derived counts were not changed.

See `aggregate.json`, `requested_task_results.csv`, `under900_progress.csv`, `res_file_inventory.csv`, `effective_trials.csv`, `worker_snapshot.tsv`, and `SHA256SUMS` for machine-readable details.
