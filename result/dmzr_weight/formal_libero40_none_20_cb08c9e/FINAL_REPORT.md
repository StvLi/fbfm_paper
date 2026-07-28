# DreamZero NONE LIBERO-40 Final Report

Audited: `2026-07-27T01:45:44+08:00`

Code: `cb08c9e552730d26cc446885e79a3e270a270d0c` | Mode: `NONE`

## Overall

| Tasks | Trials | Successes | Failures | Success rate |
| ---: | ---: | ---: | ---: | ---: |
| 40 | 800 | 561 | 239 | 70.125% |

## Suites

| Suite | Tasks | Successes | Trials | Success rate |
| --- | ---: | ---: | ---: | ---: |
| `libero_spatial` | 10 | 157 | 200 | 78.500% |
| `libero_object` | 10 | 146 | 200 | 73.000% |
| `libero_goal` | 10 | 137 | 200 | 68.500% |
| `libero_10` | 10 | 121 | 200 | 60.500% |

## Tasks

| Suite | Task | Successes | Trials | Success rate | Description |
| --- | ---: | ---: | ---: | ---: | --- |
| `libero_spatial` | 0 | 19 | 20 | 95.00% | pick up the black bowl between the plate and the ramekin and place it on the plate |
| `libero_spatial` | 1 | 19 | 20 | 95.00% | pick up the black bowl next to the ramekin and place it on the plate |
| `libero_spatial` | 2 | 19 | 20 | 95.00% | pick up the black bowl from table center and place it on the plate |
| `libero_spatial` | 3 | 19 | 20 | 95.00% | pick up the black bowl on the cookie box and place it on the plate |
| `libero_spatial` | 4 | 10 | 20 | 50.00% | pick up the black bowl in the top drawer of the wooden cabinet and place it on the plate |
| `libero_spatial` | 5 | 3 | 20 | 15.00% | pick up the black bowl on the ramekin and place it on the plate |
| `libero_spatial` | 6 | 20 | 20 | 100.00% | pick up the black bowl next to the cookie box and place it on the plate |
| `libero_spatial` | 7 | 19 | 20 | 95.00% | pick up the black bowl on the stove and place it on the plate |
| `libero_spatial` | 8 | 14 | 20 | 70.00% | pick up the black bowl next to the plate and place it on the plate |
| `libero_spatial` | 9 | 15 | 20 | 75.00% | pick up the black bowl on the wooden cabinet and place it on the plate |
| `libero_object` | 0 | 14 | 20 | 70.00% | pick up the alphabet soup and place it in the basket |
| `libero_object` | 1 | 18 | 20 | 90.00% | pick up the cream cheese and place it in the basket |
| `libero_object` | 2 | 15 | 20 | 75.00% | pick up the salad dressing and place it in the basket |
| `libero_object` | 3 | 16 | 20 | 80.00% | pick up the bbq sauce and place it in the basket |
| `libero_object` | 4 | 12 | 20 | 60.00% | pick up the ketchup and place it in the basket |
| `libero_object` | 5 | 20 | 20 | 100.00% | pick up the tomato sauce and place it in the basket |
| `libero_object` | 6 | 7 | 20 | 35.00% | pick up the butter and place it in the basket |
| `libero_object` | 7 | 9 | 20 | 45.00% | pick up the milk and place it in the basket |
| `libero_object` | 8 | 17 | 20 | 85.00% | pick up the chocolate pudding and place it in the basket |
| `libero_object` | 9 | 18 | 20 | 90.00% | pick up the orange juice and place it in the basket |
| `libero_goal` | 0 | 18 | 20 | 90.00% | open the middle drawer of the cabinet |
| `libero_goal` | 1 | 20 | 20 | 100.00% | put the bowl on the stove |
| `libero_goal` | 2 | 8 | 20 | 40.00% | put the wine bottle on top of the cabinet |
| `libero_goal` | 3 | 9 | 20 | 45.00% | open the top drawer and put the bowl inside |
| `libero_goal` | 4 | 14 | 20 | 70.00% | put the bowl on top of the cabinet |
| `libero_goal` | 5 | 13 | 20 | 65.00% | push the plate to the front of the stove |
| `libero_goal` | 6 | 14 | 20 | 70.00% | put the cream cheese in the bowl |
| `libero_goal` | 7 | 20 | 20 | 100.00% | turn on the stove |
| `libero_goal` | 8 | 20 | 20 | 100.00% | put the bowl on the plate |
| `libero_goal` | 9 | 1 | 20 | 5.00% | put the wine bottle on the rack |
| `libero_10` | 0 | 13 | 20 | 65.00% | put both the alphabet soup and the tomato sauce in the basket |
| `libero_10` | 1 | 9 | 20 | 45.00% | put both the cream cheese box and the butter in the basket |
| `libero_10` | 2 | 13 | 20 | 65.00% | turn on the stove and put the moka pot on it |
| `libero_10` | 3 | 14 | 20 | 70.00% | put the black bowl in the bottom drawer of the cabinet and close it |
| `libero_10` | 4 | 16 | 20 | 80.00% | put the white mug on the left plate and put the yellow and white mug on the right plate |
| `libero_10` | 5 | 17 | 20 | 85.00% | pick up the book and place it in the back compartment of the caddy |
| `libero_10` | 6 | 14 | 20 | 70.00% | put the white mug on the plate and put the chocolate pudding to the right of the plate |
| `libero_10` | 7 | 8 | 20 | 40.00% | put both the alphabet soup and the cream cheese box in the basket |
| `libero_10` | 8 | 10 | 20 | 50.00% | put both moka pots on the stove |
| `libero_10` | 9 | 7 | 20 | 35.00% | put the yellow and white mug in the microwave and close it |

## Integrity

- 800 records and 800 unique `(suite, task_id, trial_id)` identities.
- Exactly 40 tasks with contiguous trial IDs 0-19.
- No duplicate or missing trials; no malformed JSON rows.
- Every record has `status=ok`, `mode=NONE`, and `actions_finite=true`.
- All 800 trajectory files exist and are non-empty.
- Atomic `summary.json`, `task_summary.csv`, and `trials.csv` agree with the independent ledger audit.
