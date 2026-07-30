# LingBot-VA RoboTwin Data-Coverage Matrix

This review table aligns all 42 selected RoboTwin tasks with `max_steps < 900`
across method and environment configuration. CPU and GPU rendering are treated
as equivalent benchmark backends for the manuscript summary, while the source
of every cell remains explicit. The primary source is the final CPU-render
package at paper-record commit
`70b0a94388379ee5b7f572881e39ab30c30ec519` (evaluation revision `a116e48`).
When that package does not contain a cell, the table displays an existing
secondary record so that numerical availability and protocol completeness are
not conflated.

## Source legend

- **C**: final canonical CPU-render record at `70b0a94`; ten seed-unique
  episodes and auditable canonical `res.json` provenance.
- **G**: audited GPU-render FBFM clean record in `result/lbva_fbfm_gpu/`;
  twenty accepted episodes with episode-level validation.
- **L**: count copied from the legacy shared experiment sheet
  `result/FBFM实验分锅记录 - LingbotVAxRoboTwin.csv`. These cells have numerical
  counts in the repository but are absent from the final canonical CPU package.
- The final column lists cells that are not backed by **C**. These are included
  in the renderer-agnostic summary, but the tag preserves provenance. `BC`,
  `FC`, `BR`, and `FR` denote Base Clean, FBFM Clean, Base Randomized, and FBFM
  Randomized.

## Integrated table

| Task | Max steps | Base Clean | FBFM Clean | Base Randomized | FBFM Randomized | Outside final CPU package |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `handover_block` | 800 | 0/10 (0%) [C] | 1/10 (10%) [C] | 1/10 (10%) [C] | 0/10 (0%) [C] | -- |
| `place_cans_plasticbox` | 800 | 10/10 (100%) [C] | 10/10 (100%) [C] | 10/10 (100%) [C] | 10/10 (100%) [C] | -- |
| `stack_blocks_two` | 800 | 7/10 (70%) [C] | 10/10 (100%) [C] | 7/10 (70%) [C] | 8/10 (80%) [C] | -- |
| `open_laptop` | 700 | 9/10 (90%) [C] | 9/10 (90%) [C] | 9/10 (90%) [C] | 9/10 (90%) [C] | -- |
| `place_bread_basket` | 700 | 9/10 (90%) [C] | 5/10 (50%) [C] | 8/10 (80%) [C] | 9/10 (90%) [C] | -- |
| `place_can_basket` | 700 | 7/10 (70%) [C] | 10/10 (100%) [C] | 7/10 (70%) [C] | 9/10 (90%) [C] | -- |
| `place_object_basket` | 700 | 9/10 (90%) [C] | 8/10 (80%) [C] | 7/10 (70%) [C] | 7/10 (70%) [C] | -- |
| `put_object_cabinet` | 700 | 7/10 (70%) [C] | 6/10 (60%) [C] | 8/10 (80%) [C] | 7/10 (70%) [C] | -- |
| `shake_bottle` | 700 | 20/20 (100%) [L] | 10/10 (100%) [C] | 20/20 (100%) [L] | 10/10 (100%) [C] | BC, BR |
| `shake_bottle_horizontally` | 700 | 20/20 (100%) [L] | 10/10 (100%) [C] | 20/20 (100%) [L] | 10/10 (100%) [C] | BC, BR |
| `dump_bin_bigbin` | 600 | 10/10 (100%) [C] | 10/10 (100%) [C] | 10/10 (100%) [C] | 10/10 (100%) [C] | -- |
| `handover_mic` | 600 | 7/10 (70%) [C] | 10/10 (100%) [C] | 8/10 (80%) [C] | 8/10 (80%) [C] | -- |
| `place_dual_shoes` | 600 | 0/10 (0%) [C] | 1/10 (10%) [C] | 1/10 (10%) [C] | 1/10 (10%) [C] | -- |
| `place_bread_skillet` | 500 | 8/10 (80%) [C] | 7/10 (70%) [C] | 6/10 (60%) [C] | 7/10 (70%) [C] | -- |
| `place_burger_fries` | 500 | 10/10 (100%) [C] | 18/20 (90%) [G] | 9/10 (90%) [C] | 10/10 (100%) [C] | FC |
| `place_empty_cup` | 500 | 20/20 (100%) [L] | 20/20 (100%) [G] | 20/20 (100%) [L] | 10/10 (100%) [C] | BC, FC, BR |
| `place_shoe` | 500 | 5/10 (50%) [C] | 11/20 (55%) [G] | 6/10 (60%) [C] | 5/10 (50%) [C] | FC |
| `scan_object` | 500 | 9/10 (90%) [C] | 13/20 (65%) [G] | 8/10 (80%) [C] | 8/10 (80%) [C] | FC |
| `adjust_bottle` | 400 | 18/20 (90%) [L] | 20/20 (100%) [G] | 20/20 (100%) [L] | 10/10 (100%) [C] | BC, FC, BR |
| `beat_block_hammer` | 400 | 7/10 (70%) [C] | 15/20 (75%) [G] | 9/10 (90%) [C] | 9/10 (90%) [C] | FC |
| `click_alarmclock` | 400 | 16/20 (80%) [L] | 20/20 (100%) [G] | 18/20 (90%) [L] | 10/10 (100%) [C] | BC, FC, BR |
| `click_bell` | 400 | 20/20 (100%) [L] | 20/20 (100%) [G] | 20/20 (100%) [L] | 10/10 (100%) [C] | BC, FC, BR |
| `grab_roller` | 400 | 19/20 (95%) [L] | 20/20 (100%) [G] | 17/20 (85%) [L] | 10/10 (100%) [C] | BC, FC, BR |
| `lift_pot` | 400 | 20/20 (100%) [L] | 20/20 (100%) [G] | 17/20 (85%) [L] | 10/10 (100%) [C] | BC, FC, BR |
| `move_can_pot` | 400 | 18/20 (90%) [L] | 19/20 (95%) [G] | 14/20 (70%) [L] | 9/10 (90%) [C] | BC, FC, BR |
| `move_pillbottle_pad` | 400 | 18/20 (90%) [L] | 20/20 (100%) [G] | 19/20 (95%) [L] | 9/10 (90%) [C] | BC, FC, BR |
| `move_playingcard_away` | 400 | 17/20 (85%) [L] | 10/10 (100%) [C] | 17/20 (85%) [L] | 10/10 (100%) [C] | BC, BR |
| `move_stapler_pad` | 400 | 2/10 (20%) [C] | 4/10 (40%) [C] | 6/10 (60%) [C] | 6/10 (60%) [C] | -- |
| `pick_diverse_bottles` | 400 | 10/10 (100%) [C] | 10/10 (100%) [C] | 9/10 (90%) [C] | 8/10 (80%) [C] | -- |
| `pick_dual_bottles` | 400 | 18/20 (90%) [L] | 10/10 (100%) [C] | 14/20 (70%) [L] | 8/10 (80%) [C] | BC, BR |
| `place_a2b_left` | 400 | 9/10 (90%) [C] | 9/10 (90%) [C] | 10/10 (100%) [C] | 10/10 (100%) [C] | -- |
| `place_a2b_right` | 400 | 9/10 (90%) [C] | 8/10 (80%) [C] | 9/10 (90%) [C] | 10/10 (100%) [C] | -- |
| `place_container_plate` | 400 | 20/20 (100%) [L] | 10/10 (100%) [C] | 17/20 (85%) [L] | 10/10 (100%) [C] | BC, BR |
| `place_fan` | 400 | 8/10 (80%) [C] | 9/10 (90%) [C] | 9/10 (90%) [C] | 9/10 (90%) [C] | -- |
| `place_mouse_pad` | 400 | 5/10 (50%) [C] | 5/10 (50%) [C] | 5/10 (50%) [C] | 5/10 (50%) [C] | -- |
| `place_object_scale` | 400 | 9/10 (90%) [C] | 10/10 (100%) [C] | 8/10 (80%) [C] | 7/10 (70%) [C] | -- |
| `place_object_stand` | 400 | 12/20 (60%) [L] | 7/10 (70%) [C] | 14/20 (70%) [L] | 9/10 (90%) [C] | BC, BR |
| `place_phone_stand` | 400 | 9/10 (90%) [C] | 8/10 (80%) [C] | 8/10 (80%) [C] | 8/10 (80%) [C] | -- |
| `press_stapler` | 400 | 20/20 (100%) [L] | 9/10 (90%) [C] | 18/20 (90%) [L] | 10/10 (100%) [C] | BC, BR |
| `rotate_qrcode` | 400 | 9/10 (90%) [C] | 9/10 (90%) [C] | 9/10 (90%) [C] | 9/10 (90%) [C] | -- |
| `stamp_seal` | 400 | 10/10 (100%) [C] | 10/10 (100%) [C] | 9/10 (90%) [C] | 9/10 (90%) [C] | -- |
| `turn_switch` | 400 | 12/20 (60%) [L] | 7/10 (70%) [C] | 13/20 (65%) [L] | 5/10 (50%) [C] | BC, BR |

## Coverage summary

- The table contains a numerical entry for all `42 tasks x 2 configs x 2
  methods = 168` cells; no task-level experiment cell is missing under the
  renderer-agnostic evaluation scope.
- The final canonical CPU package covers `124/168` cells: all 72 FBFM cells
  that were planned below 900 steps and 52 Base cells.
- Twenty-two tasks have all four canonical CPU cells. The strict CPU-only
  overlap remains useful as a conservative provenance check: across 48
  config--task cells, FBFM is `367/480 = 76.46%` versus Base
  `359/480 = 74.79%`, a descriptive `+1.67` percentage-point difference.
- The 44 cells outside that package comprise 16 Base Clean, 16 Base Randomized,
  and 12 FBFM Clean cells. The FBFM cells have audited episode-level GPU
  records [G]. The Base cells retain task-level shared-ledger counts [L], which
  support success-rate reporting but not seed-paired analysis.
- Equal-weight macro averaging over all 42 tasks gives Base/FBFM rates of
  `80.48%/83.33%` for Clean and `79.76%/82.86%` for Randomized. The overall
  task-configuration macro rates are `80.12%/83.10%`, a `+2.98` point gain.

## Interpretation

No additional rollout is required to complete the agreed 42-task Appendix-D
matrix. Recovering episode-level records for the 32 legacy Base cells would
strengthen provenance and enable seed-level audits, but is not a missing-data
requirement. The eight tasks with `max_steps >= 900` remain intentionally
outside this matrix and should not be counted as missing under the agreed
short-task scope.
