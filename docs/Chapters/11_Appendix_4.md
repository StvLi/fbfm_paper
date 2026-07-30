# Appendix D: Detailed Evaluation Records

This appendix is the source-of-record layout for the main success-rate tables.
Each entry is reported as `successes/trials (SR)`. The RoboTwin summary treats
CPU and GPU rendering as equivalent benchmark backends while retaining the
source counts. Because cells contain either 10 or 20 episodes and are not
seed-paired across methods, the main comparison macro-averages task-cell rates
rather than pooling their episodes.

## LingBot-VA on RoboTwin

The selected RoboTwin evaluation contains 42 tasks under both `demo_clean` and
`demo_randomized`. Longer tasks outside this set are excluded from the main
evaluation. The consolidated ledger supplies all 168 cells: 42 tasks, two
configurations, and two methods. Integer successes and trials are treated as
the source of truth, and the displayed rates are recomputed from these counts.
The final CPU package provides 124 cells; an audited GPU package provides 12
FBFM Clean cells; and the remaining 32 Base cells retain task-level counts from
the shared experiment ledger. The latter support task-level rates but not
episode-identity or seed-paired analyses.

| Task | Clean Base | Clean FBFM | Randomized Base | Randomized FBFM |
| --- | ---: | ---: | ---: | ---: |
| `handover_block` | 0/10 (0%) | 1/10 (10%) | 1/10 (10%) | 0/10 (0%) |
| `place_cans_plasticbox` | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| `stack_blocks_two` | 7/10 (70%) | 10/10 (100%) | 7/10 (70%) | 8/10 (80%) |
| `open_laptop` | 9/10 (90%) | 9/10 (90%) | 9/10 (90%) | 9/10 (90%) |
| `place_bread_basket` | 9/10 (90%) | 5/10 (50%) | 8/10 (80%) | 9/10 (90%) |
| `place_can_basket` | 7/10 (70%) | 10/10 (100%) | 7/10 (70%) | 9/10 (90%) |
| `place_object_basket` | 9/10 (90%) | 8/10 (80%) | 7/10 (70%) | 7/10 (70%) |
| `put_object_cabinet` | 7/10 (70%) | 6/10 (60%) | 8/10 (80%) | 7/10 (70%) |
| `shake_bottle` | 20/20 (100%) | 10/10 (100%) | 20/20 (100%) | 10/10 (100%) |
| `shake_bottle_horizontally` | 20/20 (100%) | 10/10 (100%) | 20/20 (100%) | 10/10 (100%) |
| `dump_bin_bigbin` | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| `handover_mic` | 7/10 (70%) | 10/10 (100%) | 8/10 (80%) | 8/10 (80%) |
| `place_dual_shoes` | 0/10 (0%) | 1/10 (10%) | 1/10 (10%) | 1/10 (10%) |
| `place_bread_skillet` | 8/10 (80%) | 7/10 (70%) | 6/10 (60%) | 7/10 (70%) |
| `place_burger_fries` | 10/10 (100%) | 18/20 (90%) | 9/10 (90%) | 10/10 (100%) |
| `place_empty_cup` | 20/20 (100%) | 20/20 (100%) | 20/20 (100%) | 10/10 (100%) |
| `place_shoe` | 5/10 (50%) | 11/20 (55%) | 6/10 (60%) | 5/10 (50%) |
| `scan_object` | 9/10 (90%) | 13/20 (65%) | 8/10 (80%) | 8/10 (80%) |
| `adjust_bottle` | 18/20 (90%) | 20/20 (100%) | 20/20 (100%) | 10/10 (100%) |
| `beat_block_hammer` | 7/10 (70%) | 15/20 (75%) | 9/10 (90%) | 9/10 (90%) |
| `click_alarmclock` | 16/20 (80%) | 20/20 (100%) | 18/20 (90%) | 10/10 (100%) |
| `click_bell` | 20/20 (100%) | 20/20 (100%) | 20/20 (100%) | 10/10 (100%) |
| `grab_roller` | 19/20 (95%) | 20/20 (100%) | 17/20 (85%) | 10/10 (100%) |
| `lift_pot` | 20/20 (100%) | 20/20 (100%) | 17/20 (85%) | 10/10 (100%) |
| `move_can_pot` | 18/20 (90%) | 19/20 (95%) | 14/20 (70%) | 9/10 (90%) |
| `move_pillbottle_pad` | 18/20 (90%) | 20/20 (100%) | 19/20 (95%) | 9/10 (90%) |
| `move_playingcard_away` | 17/20 (85%) | 10/10 (100%) | 17/20 (85%) | 10/10 (100%) |
| `move_stapler_pad` | 2/10 (20%) | 4/10 (40%) | 6/10 (60%) | 6/10 (60%) |
| `pick_diverse_bottles` | 10/10 (100%) | 10/10 (100%) | 9/10 (90%) | 8/10 (80%) |
| `pick_dual_bottles` | 18/20 (90%) | 10/10 (100%) | 14/20 (70%) | 8/10 (80%) |
| `place_a2b_left` | 9/10 (90%) | 9/10 (90%) | 10/10 (100%) | 10/10 (100%) |
| `place_a2b_right` | 9/10 (90%) | 8/10 (80%) | 9/10 (90%) | 10/10 (100%) |
| `place_container_plate` | 20/20 (100%) | 10/10 (100%) | 17/20 (85%) | 10/10 (100%) |
| `place_fan` | 8/10 (80%) | 9/10 (90%) | 9/10 (90%) | 9/10 (90%) |
| `place_mouse_pad` | 5/10 (50%) | 5/10 (50%) | 5/10 (50%) | 5/10 (50%) |
| `place_object_scale` | 9/10 (90%) | 10/10 (100%) | 8/10 (80%) | 7/10 (70%) |
| `place_object_stand` | 12/20 (60%) | 7/10 (70%) | 14/20 (70%) | 9/10 (90%) |
| `place_phone_stand` | 9/10 (90%) | 8/10 (80%) | 8/10 (80%) | 8/10 (80%) |
| `press_stapler` | 20/20 (100%) | 9/10 (90%) | 18/20 (90%) | 10/10 (100%) |
| `rotate_qrcode` | 9/10 (90%) | 9/10 (90%) | 9/10 (90%) | 9/10 (90%) |
| `stamp_seal` | 10/10 (100%) | 10/10 (100%) | 9/10 (90%) | 9/10 (90%) |
| `turn_switch` | 12/20 (60%) | 7/10 (70%) | 13/20 (65%) | 5/10 (50%) |
| **Completed task cells** | **42/42** | **42/42** | **42/42** | **42/42** |
| **Macro SR** | **80.5%** | **83.3%** | **79.8%** | **82.9%** |

## DreamZero on LIBERO

The detailed LIBERO record covers all ten tasks in each of LIBERO-Spatial,
LIBERO-Object, LIBERO-Goal, and LIBERO-10. Each cell reports
successes/20 episodes and the corresponding success rate. LIBERO-90 is not
included.

| Suite | Task ID | Base | FBFM |
| --- | ---: | ---: | ---: |
| LIBERO-Spatial | 0 | 19/20 (95%) | 17/20 (85%) |
| LIBERO-Spatial | 1 | 19/20 (95%) | 18/20 (90%) |
| LIBERO-Spatial | 2 | 19/20 (95%) | 19/20 (95%) |
| LIBERO-Spatial | 3 | 19/20 (95%) | 19/20 (95%) |
| LIBERO-Spatial | 4 | 10/20 (50%) | 8/20 (40%) |
| LIBERO-Spatial | 5 | 3/20 (15%) | 2/20 (10%) |
| LIBERO-Spatial | 6 | 20/20 (100%) | 20/20 (100%) |
| LIBERO-Spatial | 7 | 19/20 (95%) | 19/20 (95%) |
| LIBERO-Spatial | 8 | 14/20 (70%) | 17/20 (85%) |
| LIBERO-Spatial | 9 | 15/20 (75%) | 15/20 (75%) |
| **LIBERO-Spatial** | **Subtotal** | **157/200 (78.5%)** | **154/200 (77%)** |
| LIBERO-Object | 0 | 14/20 (70%) | 17/20 (85%) |
| LIBERO-Object | 1 | 18/20 (90%) | 17/20 (85%) |
| LIBERO-Object | 2 | 15/20 (75%) | 12/20 (60%) |
| LIBERO-Object | 3 | 16/20 (80%) | 18/20 (90%) |
| LIBERO-Object | 4 | 12/20 (60%) | 9/20 (45%) |
| LIBERO-Object | 5 | 20/20 (100%) | 20/20 (100%) |
| LIBERO-Object | 6 | 7/20 (35%) | 9/20 (45%) |
| LIBERO-Object | 7 | 9/20 (45%) | 7/20 (35%) |
| LIBERO-Object | 8 | 17/20 (85%) | 16/20 (80%) |
| LIBERO-Object | 9 | 18/20 (90%) | 19/20 (95%) |
| **LIBERO-Object** | **Subtotal** | **146/200 (73%)** | **144/200 (72%)** |
| LIBERO-Goal | 0 | 18/20 (90%) | 17/20 (85%) |
| LIBERO-Goal | 1 | 20/20 (100%) | 20/20 (100%) |
| LIBERO-Goal | 2 | 8/20 (40%) | 18/20 (90%) |
| LIBERO-Goal | 3 | 9/20 (45%) | 9/20 (45%) |
| LIBERO-Goal | 4 | 14/20 (70%) | 9/20 (45%) |
| LIBERO-Goal | 5 | 13/20 (65%) | 15/20 (75%) |
| LIBERO-Goal | 6 | 14/20 (70%) | 14/20 (70%) |
| LIBERO-Goal | 7 | 20/20 (100%) | 20/20 (100%) |
| LIBERO-Goal | 8 | 20/20 (100%) | 20/20 (100%) |
| LIBERO-Goal | 9 | 1/20 (5%) | 0/20 (0%) |
| **LIBERO-Goal** | **Subtotal** | **137/200 (68.5%)** | **142/200 (71%)** |
| LIBERO-10 | 0 | 13/20 (65%) | 10/20 (50%) |
| LIBERO-10 | 1 | 9/20 (45%) | 12/20 (60%) |
| LIBERO-10 | 2 | 13/20 (65%) | 14/20 (70%) |
| LIBERO-10 | 3 | 14/20 (70%) | 12/20 (60%) |
| LIBERO-10 | 4 | 16/20 (80%) | 18/20 (90%) |
| LIBERO-10 | 5 | 17/20 (85%) | 19/20 (95%) |
| LIBERO-10 | 6 | 14/20 (70%) | 14/20 (70%) |
| LIBERO-10 | 7 | 8/20 (40%) | 13/20 (65%) |
| LIBERO-10 | 8 | 10/20 (50%) | 5/20 (25%) |
| LIBERO-10 | 9 | 7/20 (35%) | 9/20 (45%) |
| **LIBERO-10** | **Subtotal** | **121/200 (60.5%)** | **126/200 (63%)** |
| **All suites** | **Total** | **561/800 (70.125%)** | **566/800 (70.75%)** |
| **Coverage** | **All tasks** | **40/40 task cells** | **40/40 task cells** |
