# DreamZero LIBERO Native-Synchronous Base Step26000 测评结果

> 归档说明（2026-07-28）：本文件记录的是 DreamZero 原生同步 rollout，未采用论文主实验预设的有延迟伪异步 overlap 协议。该结果仅保留用于历史审计，不得填入 Appendix D 或 Section 5.2 的 Base/NONE 行；主实验 Base 需要在匹配的伪异步协议下重新测评。

固定协议：4 个标准 suite，每 suite 10 tasks，每 task 使用 reset ID 0–19，共 800 条轨迹。

| Suite | Task ID | Trials | Success | Success Rate | Status | Log |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| libero_spatial | 0 | 20 | 18 | 90.00% | complete | `logs/20260723-16:19:56-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-16:53:29-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_spatial | 1 | 20 | 17 | 85.00% | complete | `logs/20260723-16:19:56-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-16:53:29-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_spatial | 2 | 20 | 19 | 95.00% | complete | `logs/20260723-16:19:56-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-16:53:29-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_spatial | 3 | 20 | 20 | 100.00% | complete | `logs/20260723-16:19:56-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-16:53:29-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_spatial | 4 | 20 | 19 | 95.00% | complete | `logs/20260723-16:19:56-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-16:53:29-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_spatial | 5 | 20 | 11 | 55.00% | complete | `logs/20260723-16:19:56-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-16:53:29-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_spatial | 6 | 20 | 20 | 100.00% | complete | `logs/20260723-16:19:56-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-16:53:29-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_spatial | 7 | 20 | 18 | 90.00% | complete | `logs/20260723-16:19:56-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-16:53:29-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_spatial | 8 | 20 | 19 | 95.00% | complete | `logs/20260723-16:19:56-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-16:53:29-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_spatial | 9 | 20 | 20 | 100.00% | complete | `logs/20260723-16:19:56-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-16:53:29-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_object | 0 | 20 | 19 | 95.00% | complete | `logs/20260723-17:08:07-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_object | 1 | 20 | 20 | 100.00% | complete | `logs/20260723-17:08:07-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_object | 2 | 20 | 19 | 95.00% | complete | `logs/20260723-17:08:07-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_object | 3 | 20 | 15 | 75.00% | complete | `logs/20260723-17:08:07-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_object | 4 | 20 | 16 | 80.00% | complete | `logs/20260723-17:08:07-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_object | 5 | 20 | 20 | 100.00% | complete | `logs/20260723-17:08:07-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_object | 6 | 20 | 18 | 90.00% | complete | `logs/20260723-17:08:07-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_object | 7 | 20 | 15 | 75.00% | complete | `logs/20260723-17:08:07-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_object | 8 | 20 | 19 | 95.00% | complete | `logs/20260723-17:08:07-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_object | 9 | 20 | 20 | 100.00% | complete | `logs/20260723-17:08:07-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_goal | 0 | 20 | 20 | 100.00% | complete | `logs/20260723-17:44:43-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:04:27-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:23:58-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:42:47-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_goal | 1 | 20 | 18 | 90.00% | complete | `logs/20260723-17:44:43-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:04:27-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:23:58-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:42:47-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_goal | 2 | 20 | 13 | 65.00% | complete | `logs/20260723-17:44:43-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:04:27-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:23:58-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:42:47-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_goal | 3 | 20 | 4 | 20.00% | complete | `logs/20260723-17:44:43-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:04:27-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:23:58-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:42:47-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_goal | 4 | 20 | 5 | 25.00% | complete | `logs/20260723-17:44:43-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:04:27-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:23:58-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:42:47-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_goal | 5 | 20 | 4 | 20.00% | complete | `logs/20260723-17:44:43-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:04:27-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:23:58-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:42:47-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_goal | 6 | 20 | 6 | 30.00% | complete | `logs/20260723-17:44:43-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:04:27-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:23:58-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:42:47-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_goal | 7 | 20 | 20 | 100.00% | complete | `logs/20260723-17:44:43-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:04:27-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:23:58-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:42:47-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_goal | 8 | 20 | 20 | 100.00% | complete | `logs/20260723-17:44:43-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:04:27-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:23:58-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:42:47-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_goal | 9 | 20 | 4 | 20.00% | complete | `logs/20260723-17:44:43-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:04:27-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:23:58-libero_dreamzero_base_20/eval_embodiment.log;logs/20260723-18:42:47-libero_spatial_dreamzero_missing_2/eval_embodiment.log` |
| libero_10 | 0 | 20 | 14 | 70.00% | complete | `logs/20260723-18:56:39-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_10 | 1 | 20 | 16 | 80.00% | complete | `logs/20260723-18:56:39-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_10 | 2 | 20 | 15 | 75.00% | complete | `logs/20260723-18:56:39-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_10 | 3 | 20 | 20 | 100.00% | complete | `logs/20260723-18:56:39-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_10 | 4 | 20 | 20 | 100.00% | complete | `logs/20260723-18:56:39-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_10 | 5 | 20 | 15 | 75.00% | complete | `logs/20260723-18:56:39-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_10 | 6 | 20 | 17 | 85.00% | complete | `logs/20260723-18:56:39-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_10 | 7 | 20 | 14 | 70.00% | complete | `logs/20260723-18:56:39-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_10 | 8 | 20 | 2 | 10.00% | complete | `logs/20260723-18:56:39-libero_dreamzero_base_20/eval_embodiment.log` |
| libero_10 | 9 | 20 | 9 | 45.00% | complete | `logs/20260723-18:56:39-libero_dreamzero_base_20/eval_embodiment.log` |

## 当前汇总

- 完整 task：40/40
- 有效轨迹：800/800
- 成功：618/800
- 当前平均成功率：77.25%
