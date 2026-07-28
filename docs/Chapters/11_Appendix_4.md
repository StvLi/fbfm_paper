# Appendix D: Detailed Evaluation Records

This appendix is the source-of-record layout for the main success-rate tables.
Each entry will be filled as `successes/trials (SR)` only after the corresponding
Base and FBFM evaluations satisfy the same checkpoint, task configuration,
initialization protocol, and episode horizon. Dashes denote pending matched
records rather than zero success.

## LingBot-VA on RoboTwin

The selected RoboTwin evaluation contains 42 tasks under both `demo_clean` and
`demo_randomized`. Longer tasks outside this set are excluded from the main
evaluation.

| Task | Clean Base | Clean FBFM | Randomized Base | Randomized FBFM |
| --- | ---: | ---: | ---: | ---: |
| `handover_block` | -- | -- | -- | -- |
| `place_cans_plasticbox` | -- | -- | -- | -- |
| `stack_blocks_two` | -- | -- | -- | -- |
| `open_laptop` | -- | -- | -- | -- |
| `place_bread_basket` | -- | -- | -- | -- |
| `place_can_basket` | -- | -- | -- | -- |
| `place_object_basket` | -- | -- | -- | -- |
| `put_object_cabinet` | -- | -- | -- | -- |
| `shake_bottle` | -- | -- | -- | -- |
| `shake_bottle_horizontally` | -- | -- | -- | -- |
| `dump_bin_bigbin` | -- | -- | -- | -- |
| `handover_mic` | -- | -- | -- | -- |
| `place_dual_shoes` | -- | -- | -- | -- |
| `place_bread_skillet` | -- | -- | -- | -- |
| `place_burger_fries` | -- | -- | -- | -- |
| `place_empty_cup` | -- | -- | -- | -- |
| `place_shoe` | -- | -- | -- | -- |
| `scan_object` | -- | -- | -- | -- |
| `adjust_bottle` | -- | -- | -- | -- |
| `beat_block_hammer` | -- | -- | -- | -- |
| `click_alarmclock` | -- | -- | -- | -- |
| `click_bell` | -- | -- | -- | -- |
| `grab_roller` | -- | -- | -- | -- |
| `lift_pot` | -- | -- | -- | -- |
| `move_can_pot` | -- | -- | -- | -- |
| `move_pillbottle_pad` | -- | -- | -- | -- |
| `move_playingcard_away` | -- | -- | -- | -- |
| `move_stapler_pad` | -- | -- | -- | -- |
| `pick_diverse_bottles` | -- | -- | -- | -- |
| `pick_dual_bottles` | -- | -- | -- | -- |
| `place_a2b_left` | -- | -- | -- | -- |
| `place_a2b_right` | -- | -- | -- | -- |
| `place_container_plate` | -- | -- | -- | -- |
| `place_fan` | -- | -- | -- | -- |
| `place_mouse_pad` | -- | -- | -- | -- |
| `place_object_scale` | -- | -- | -- | -- |
| `place_object_stand` | -- | -- | -- | -- |
| `place_phone_stand` | -- | -- | -- | -- |
| `press_stapler` | -- | -- | -- | -- |
| `rotate_qrcode` | -- | -- | -- | -- |
| `stamp_seal` | -- | -- | -- | -- |
| `turn_switch` | -- | -- | -- | -- |

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
