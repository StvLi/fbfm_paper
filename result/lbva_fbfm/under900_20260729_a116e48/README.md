# LingBot-VA FBFM CPU-Render Under-900 Final Snapshot

Final canonical snapshot at `2026-07-30T03:41:38+08:00` from evaluation commit
`a116e48d9c8956c7ee66360ae68007bc146abcc3`. Only cells with
`max_steps < 900` are included; tasks at 900 steps or above were stopped by
design.

## Complete Coverage

| Method | Complete cells | Successes / episodes | Micro success rate |
| --- | ---: | ---: | ---: |
| FBFM | 72/72 | 590/720 | 81.94% |
| NONE | 52/52 | 390/520 | 75.00% |

Across the 48 identical `config x task` cells completed by both methods, FBFM
is 367/480 (76.46%) and NONE is 359/480 (74.79%), a descriptive difference of
+1.67 percentage points. This CPU-only subset is retained as a conservative
provenance audit; it is not the renderer-agnostic 42-task summary reported in
the manuscript.

## Requested FBFM Results

| Task | Clean | Randomized |
| --- | ---: | ---: |
| `handover_block` | 1/10 (10.00%) | 0/10 (0.00%) |
| `place_cans_plasticbox` | 10/10 (100.00%) | 10/10 (100.00%) |
| `stack_blocks_two` | 10/10 (100.00%) | 8/10 (80.00%) |
| `open_laptop` | 9/10 (90.00%) | 9/10 (90.00%) |
| `place_bread_basket` | 5/10 (50.00%) | 9/10 (90.00%) |
| `place_can_basket` | 10/10 (100.00%) | 9/10 (90.00%) |
| `place_object_basket` | 8/10 (80.00%) | 7/10 (70.00%) |
| `put_object_cabinet` | 6/10 (60.00%) | 7/10 (70.00%) |
| `shake_bottle` | 10/10 (100.00%) | 10/10 (100.00%) |
| `shake_bottle_horizontally` | 10/10 (100.00%) | 10/10 (100.00%) |
| `dump_bin_bigbin` | 10/10 (100.00%) | 10/10 (100.00%) |
| `handover_mic` | 10/10 (100.00%) | 8/10 (80.00%) |
| `place_dual_shoes` | 1/10 (10.00%) | 1/10 (10.00%) |
| `place_bread_skillet` | 7/10 (70.00%) | 7/10 (70.00%) |

Additional randomized cells:

| Task | Randomized |
| --- | ---: |
| `place_burger_fries` | 10/10 (100.00%) |
| `place_empty_cup` | 10/10 (100.00%) |
| `place_shoe` | 5/10 (50.00%) |
| `scan_object` | 8/10 (80.00%) |

All 32 requested cells are complete. The requested subset totals 245/320
(76.56%).

## Audit and Provenance

Canonical results are authoritative. Every included cell contains exactly ten
episodes with unique seeds; `succ_num`, `total_num`, and the episode records
agree. `raw/canonical_res.jsonl` contains all 72 official FBFM under-900
records. Historical main and shard JSONL files are retained to show how earlier
partial cells were recovered, but they are not counted again.

`effective_trials.csv` contains all 720 official FBFM under-900 episodes.
`audit_report.json` records the seed checks and the strict matched comparison.
`res_file_inventory.csv` inventories canonical and historical records.
`worker_snapshot.tsv` and `worker_processes.txt` are explicitly historical
precompletion provenance; evaluation processes were later stopped and GPU
resources released.

The source checksum manifest was calculated before Git normalized several text
files from CRLF to LF. The committed manifest is regenerated against the
repository representation; experiment values and derived counts are unchanged.
