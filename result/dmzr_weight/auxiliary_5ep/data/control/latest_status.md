# DreamZero FBFM three-weight sweep

Updated: `2026-07-26T22:12:59+08:00`

State: `running:l1mass_005833` | active: `l1mass_005833` (`0.005833333333333334`)

Overall: 57/60 task-weight cells, 286/300 episodes, 124 successes (43.4%).

Observed mean episode: `106.58s`; estimated finish: `2026-07-26T22:37+08:00`.

## Weight progress

| Weight | Complete tasks | Episodes | Success | Micro rate | Mean seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| `1.0` | 20/20 | 100/100 | 0 | 0.0% | 148.14 |
| `sqrt(56/9600) = 0.07637626158259733` | 20/20 | 100/100 | 59 | 59.0% | 93.56 |
| `56/9600 = 0.005833333333333334` | 17/20 | 86/100 | 65 | 75.6% | 73.39 |

## Health

GPU (`name, MiB used/total, utilization %, power W`): `NVIDIA RTX A6000, 31714, 49140, 94, 285.95`

Server: pid `1244654`, alive `True`; client: pid `1245030`, alive `True`.

Active audit: server errors `0`, tail records `4614`, max action correction `5.935782432556152`, max video correction `29.845266342163086`.

## Active weight task results

| Suite | Task | Status | Success | Rate | Mean steps | Mean seconds |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| `libero_spatial` | 0 | complete | 4/5 | 80.0% | 166.2 | 53.04764873723034 |
| `libero_spatial` | 1 | complete | 5/5 | 100.0% | 181.6 | 58.0330587371951 |
| `libero_spatial` | 2 | complete | 5/5 | 100.0% | 107.2 | 34.92796740459744 |
| `libero_spatial` | 3 | complete | 5/5 | 100.0% | 159.2 | 50.97992883280385 |
| `libero_spatial` | 4 | complete | 1/5 | 20.0% | 416.0 | 130.03059669642244 |
| `libero_spatial` | 5 | complete | 2/5 | 40.0% | 385.4 | 120.32851298698225 |
| `libero_spatial` | 6 | complete | 5/5 | 100.0% | 112.0 | 36.513129028212276 |
| `libero_spatial` | 7 | complete | 5/5 | 100.0% | 113.8 | 37.134463728172705 |
| `libero_spatial` | 8 | complete | 5/5 | 100.0% | 153.6 | 49.19488035161048 |
| `libero_spatial` | 9 | complete | 3/5 | 60.0% | 287.2 | 90.22886953358538 |
| `libero_object` | 0 | complete | 3/5 | 60.0% | 348.6 | 108.02452308463398 |
| `libero_object` | 1 | complete | 5/5 | 100.0% | 148.6 | 47.092365742637774 |
| `libero_object` | 2 | complete | 3/5 | 60.0% | 334.6 | 103.56882314302493 |
| `libero_object` | 3 | complete | 5/5 | 100.0% | 141.6 | 44.88604160081595 |
| `libero_object` | 4 | complete | 2/5 | 40.0% | 349.8 | 108.0497031393461 |
| `libero_object` | 5 | complete | 5/5 | 100.0% | 143.4 | 45.520283313584514 |
| `libero_object` | 6 | complete | 2/5 | 40.0% | 373.4 | 115.34347955838311 |
| `libero_object` | 7 | running | 0/1 | 0.0% | 480.0 | 147.3321228249697 |
| `libero_object` | 8 | pending | 0/0 | - | - | - |
| `libero_object` | 9 | pending | 0/0 | - | - | - |
