# Appendix D: Detailed Evaluation Records

This appendix is the source-of-record layout for the main success-rate tables.
Each available entry is reported as `successes/trials (SR)`. Dashes denote
pending records rather than zero success. Final comparisons will use only Base
and FBFM evaluations satisfying the same checkpoint, task configuration,
initialization protocol, and episode horizon.

## LingBot-VA on RoboTwin

The selected RoboTwin evaluation contains 42 tasks under both `demo_clean` and
`demo_randomized`. Longer tasks outside this set are excluded from the main
evaluation. Snapshot commit `50a3cc4` supplies 33 completed Base cells and 45
completed FBFM cells within this selection; 15 cells currently have both
records.

| Task | Clean Base | Clean FBFM | Randomized Base | Randomized FBFM |
| --- | ---: | ---: | ---: | ---: |
| `handover_block` | 0/10 (0%) | -- | 1/10 (10%) | -- |
| `place_cans_plasticbox` | 10/10 (100%) | -- | -- | -- |
| `stack_blocks_two` | 7/10 (70%) | -- | -- | -- |
| `open_laptop` | 9/10 (90%) | -- | 9/10 (90%) | -- |
| `place_bread_basket` | 9/10 (90%) | -- | -- | -- |
| `place_can_basket` | 7/10 (70%) | -- | -- | -- |
| `place_object_basket` | 9/10 (90%) | -- | -- | -- |
| `put_object_cabinet` | 7/10 (70%) | -- | -- | -- |
| `shake_bottle` | -- | -- | -- | -- |
| `shake_bottle_horizontally` | -- | -- | -- | -- |
| `dump_bin_bigbin` | 10/10 (100%) | -- | 10/10 (100%) | -- |
| `handover_mic` | 7/10 (70%) | 10/10 (100%) | -- | -- |
| `place_dual_shoes` | 0/10 (0%) | -- | -- | -- |
| `place_bread_skillet` | 8/10 (80%) | -- | -- | -- |
| `place_burger_fries` | 10/10 (100%) | -- | -- | 10/10 (100%) |
| `place_empty_cup` | -- | -- | -- | 10/10 (100%) |
| `place_shoe` | 5/10 (50%) | -- | -- | 5/10 (50%) |
| `scan_object` | 9/10 (90%) | -- | -- | 8/10 (80%) |
| `adjust_bottle` | -- | -- | -- | 10/10 (100%) |
| `beat_block_hammer` | 7/10 (70%) | -- | 9/10 (90%) | 9/10 (90%) |
| `click_alarmclock` | -- | -- | -- | 10/10 (100%) |
| `click_bell` | -- | -- | -- | 10/10 (100%) |
| `grab_roller` | -- | -- | -- | 10/10 (100%) |
| `lift_pot` | -- | -- | -- | 10/10 (100%) |
| `move_can_pot` | -- | -- | -- | 9/10 (90%) |
| `move_pillbottle_pad` | -- | -- | -- | 9/10 (90%) |
| `move_playingcard_away` | -- | 10/10 (100%) | -- | 10/10 (100%) |
| `move_stapler_pad` | 2/10 (20%) | 4/10 (40%) | 6/10 (60%) | 6/10 (60%) |
| `pick_diverse_bottles` | 10/10 (100%) | 10/10 (100%) | 9/10 (90%) | 8/10 (80%) |
| `pick_dual_bottles` | -- | 10/10 (100%) | -- | 8/10 (80%) |
| `place_a2b_left` | 9/10 (90%) | 9/10 (90%) | -- | 10/10 (100%) |
| `place_a2b_right` | 9/10 (90%) | 8/10 (80%) | 9/10 (90%) | 10/10 (100%) |
| `place_container_plate` | -- | 10/10 (100%) | -- | 10/10 (100%) |
| `place_fan` | 8/10 (80%) | 9/10 (90%) | -- | 9/10 (90%) |
| `place_mouse_pad` | 5/10 (50%) | 5/10 (50%) | -- | 5/10 (50%) |
| `place_object_scale` | 9/10 (90%) | 10/10 (100%) | -- | 7/10 (70%) |
| `place_object_stand` | -- | 7/10 (70%) | -- | 9/10 (90%) |
| `place_phone_stand` | 9/10 (90%) | 8/10 (80%) | -- | 8/10 (80%) |
| `press_stapler` | -- | 9/10 (90%) | -- | 10/10 (100%) |
| `rotate_qrcode` | 9/10 (90%) | 9/10 (90%) | -- | 9/10 (90%) |
| `stamp_seal` | 10/10 (100%) | 10/10 (100%) | -- | 9/10 (90%) |
| `turn_switch` | -- | 7/10 (70%) | -- | 5/10 (50%) |

## DreamZero on LIBERO

The detailed LIBERO record covers all ten tasks in each of LIBERO-Spatial,
LIBERO-Object, LIBERO-Goal, and LIBERO-10. LIBERO-90 is not included.

| Suite | Task ID | Base | FBFM |
| --- | ---: | ---: | ---: |
| LIBERO-Spatial | 0 | -- | -- |
| LIBERO-Spatial | 1 | -- | -- |
| LIBERO-Spatial | 2 | -- | -- |
| LIBERO-Spatial | 3 | -- | -- |
| LIBERO-Spatial | 4 | -- | -- |
| LIBERO-Spatial | 5 | -- | -- |
| LIBERO-Spatial | 6 | -- | -- |
| LIBERO-Spatial | 7 | -- | -- |
| LIBERO-Spatial | 8 | -- | -- |
| LIBERO-Spatial | 9 | -- | -- |
| LIBERO-Object | 0 | -- | -- |
| LIBERO-Object | 1 | -- | -- |
| LIBERO-Object | 2 | -- | -- |
| LIBERO-Object | 3 | -- | -- |
| LIBERO-Object | 4 | -- | -- |
| LIBERO-Object | 5 | -- | -- |
| LIBERO-Object | 6 | -- | -- |
| LIBERO-Object | 7 | -- | -- |
| LIBERO-Object | 8 | -- | -- |
| LIBERO-Object | 9 | -- | -- |
| LIBERO-Goal | 0 | -- | -- |
| LIBERO-Goal | 1 | -- | -- |
| LIBERO-Goal | 2 | -- | -- |
| LIBERO-Goal | 3 | -- | -- |
| LIBERO-Goal | 4 | -- | -- |
| LIBERO-Goal | 5 | -- | -- |
| LIBERO-Goal | 6 | -- | -- |
| LIBERO-Goal | 7 | -- | -- |
| LIBERO-Goal | 8 | -- | -- |
| LIBERO-Goal | 9 | -- | -- |
| LIBERO-10 | 0 | -- | -- |
| LIBERO-10 | 1 | -- | -- |
| LIBERO-10 | 2 | -- | -- |
| LIBERO-10 | 3 | -- | -- |
| LIBERO-10 | 4 | -- | -- |
| LIBERO-10 | 5 | -- | -- |
| LIBERO-10 | 6 | -- | -- |
| LIBERO-10 | 7 | -- | -- |
| LIBERO-10 | 8 | -- | -- |
| LIBERO-10 | 9 | -- | -- |
