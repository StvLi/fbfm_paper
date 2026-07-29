# Lingbot-VA x FBFM x RoboTwin 全任务实验实现记录

记录日期：2026-07-24；运行状态附记：2026-07-25

## 1. 实验边界与可复现基线

本记录对应 FBFM 仓库分支 `runnable-lingbot-fbfm-robotwin`、提交
`a116e48d9c8956c7ee66360ae68007bc146abcc3`。评测使用冻结的
`lingbot-va-posttrain-robotwin` checkpoint、RoboTwin 的 50 个标准任务和
`demo_clean` 配置，每个任务 20 个 episode，共 1,000 个 episode。运行模式固定为
`FBFM`，不训练、不更新模型权重，也不以实测推理耗时改变任何方法变量。

固定数学协议为 `H=32`、`d=16`、`s=16`。video flow 执行 25 个数值步和
1 个 cache-only evaluation；action flow 执行 50 个数值步和 1 个 cache-only
evaluation。cache-only endpoint 用于原生 cache 提交，不额外执行 Euler 数值更新。
Lingbot-VA 原生 VAE、KV cache、prediction cache、scheduler、动作归一化以及
state-first/action-second 的求解次序均保持不变。

## 2. 确定性伪异步调度

伪异步由离散 solver grant 实现，不使用 wall-clock 延迟。旧 action chunk 的
16 个仿真执行步中，客户端每一步都按固定整数比例释放 video solver evaluation，并等待已授权
evaluation 完成；observation feedback 则按默认 `observation_interval=4` 每四个 action step
采集和提交一次，不是每个仿真步提交一次。默认把全部 26 个 video evaluations 确定性分配到
16 个仿真步；因此相同输入、seed 和 solver budget 对应相同的反馈到达边界，主机调度或瞬时
推理速度不会改变 `d`、mask 或 solver step。

当前实现先把真实 observation 累积在 `feedback_pending_obs`；满 4 个后取出一个四帧
`obs_chunk`，一次调用 rolling VAE 编码并发布 1 个 feedback latent，而不是每到 1 个
observation 就单独推进一次 feedback VAE。代码证据是
`wan_va/wan_va_server.py:640-645`。这保证 temporal compression 与 latent slot 严格对齐，
但四帧凑齐前不会发布中间 state constraint。

服务端在 video solver step
边界排空反馈队列、进行 VAE 编码、更新带单调版本号的 chunk constraint context，然后
重新取得 state constraint snapshot。反馈窗口通过 action-step cutoff 区分已经提交到真实
KV history 的 observation 与当前 chunk 的动态反馈，避免同一 observation 在一次 generation
中既作为历史又作为未来约束。video flow 完成后才进入 action flow，保持 state-first、
action-second；迟到反馈不会插入正在运行的 action solver。

客户端的离散 grant 和 26/16 分配位于
`evaluation/robotwin/eval_polict_client_openpi.py:591-736`；服务端等待 grant、逐 video
evaluation 取 constraint snapshot，并在 video 完成后才进入 action flow，位于
`wan_va/wan_va_server.py:1056-1199`。

## 3. FBFM state/action constraint

FBFM 等于 RTC previous-action constraint 加实时 state constraint。video/state 与 action
分别使用两个 scheduler 实例，先完成 video flow 再运行 action flow；两者复用的是同一
`WrapperedFlowMatchScheduler.step` 约束修正实现，而不是同一个 solver 实例。动作预测长度为
`H=32` 个完整控制向量；`d=16`、`s=16`
时 `[0,16)` 是权重为 1 的硬 previous-action 前缀，`[16,32)` 自由生成，没有软区。
时间 mask 先在 `(B,1,F,N,1)` 上构造，再与 Lingbot-VA 原生 channel mask 相乘并广播到
动作 target；RoboTwin 的 30 维模型坐标中仅 16 个有效通道受约束。previous action 先经
原生 `preprocess_action` 归一化并补齐到模型坐标，不能直接用物理动作与 solver sample 作差。

state constraint 只对已经由真实 observation 对齐并到达的 latent slot 置 mask。反馈按
`global_slot_id = feedback_target_frame_st_id + local_slot` 映射到当前 chunk；重复 slot、
窗口外 slot 和已关闭 context 被拒绝。首个 chunk 没有 previous action，action mask 自然为
零；后续 chunk 的 state mask 随确定性 feedback grant 在 video solver 边界更新。

约束修正先由当前 sample 和 base velocity 估计 `x1 = x_t - sigma * v`，只在 mask 选中的
target 坐标上形成误差；再通过 masked loss 对 sample 求 VJP，并按 guidance scale 修正 base
velocity。修正范数受 scheduler 的 guidance cap 限制。state target/mask 只进入 video loop，
previous-action target/mask 只进入随后 action loop。

## 4. 三分片并行与隔离

在 `a116e48` 的原始全任务入口中，`run_robotwin_all_tasks_fbfm.sh` 固定使用 50 个标准任务，
默认创建 3 个 worker；第 `i` 个 worker 处理 `index mod 3 = i` 的任务。三个 worker 使用独立端口
`29256..29258` 和 torch master ports `29261..29263`，每个任务由独立 policy server、
RoboTwin simulator/client、KV cache、prediction cache、constraint context 和 feedback stream
完成。分片仅共享同一块 GPU 和只读 checkpoint，不共享模型运行态或反馈状态。

`adjust_bottle` 的已完成 20/20 结果从
`robotwin_outputs/fbfm_20_20260724_102818/aggregate.json` 导入，worker 不重复执行该任务。
其余任务每次均以 `demo_clean`、评测 seed 0 和 FBFM 固定协议启动。三分片并行只改变任务的
并发编排，不改变单个 episode 的方法变量。

当前本地入口在不改变上述单任务路径的前提下，增加了 manifest 子集、1 到 3 个顶层 shard、
旧结果符号链接复用和可配置目标次数。首次运行会固化 `task_manifest.txt`；同一输出根若换了
任务集合或顺序会拒绝启动。当前短任务运行的两个顶层 worker 与一个单任务辅助 shard 均使用
独立端口和独立模型运行态；辅助 shard 不属于顶层 launcher 的 worker 子进程树。

## 5. 断点恢复与监控边界

`a116e48` 的 worker skip 判据只检查固定路径
`tasks/<task>/client/stseed-10000/metrics/<task>/res.json`，且 `total_num` 必须恰好为 20；
聚合器另行要求任务目录中只有一个 `res.json` 并有恰好 20 个可解析视频。满足 worker 判据时
跳过该任务并重新聚合。未满足判据且已有任务目录时，目录被原子改名为
`<task>.interrupted.<timestamp>` 后保留，再创建干净任务目录；历史中断产物不计入当前结果。
这是任务级重启，不是从任务内第 N 个 episode 接续。运行中使用 `.running` 标记，非零退出使用
`.failed` 标记并写入 `logs/failures.log`。

当前本地入口把 worker 的“结果充分”定义为：固定位置有一个可读 `res.json`、
`total_num >= target`、成功数取值合法，且 `0..total_num-1` 的每个 index 至少存在一个可解析
结果视频。它不在 skip 判据中强制核验 `succ_num` 与视频标签一致，也不证明每个 index 只有一个
outcome。旧任务达到该门槛后通过符号链接整体复用；超过目标的 episode 不裁剪。严格有效性和
去重必须由最终 combiner/verifier 另行证明，不能由 worker skip 或 live `complete` 推断。

顶层 launcher PID 写入 `launcher.pid`。独立 monitor 重新聚合、记录 GPU 和顶层 launcher 快照
到 `status_reports.jsonl`，并以实际 launcher PID 判断存活。`a116e48` 是启动后每 1,800 秒轮询；
当前 monitor 对齐自然时间边界并写 `monitor.pid`。aggregate 尚未 complete 且 launcher PID
不再存活时最多自动重拉 3 次；monitor 不区分 launcher 是异常退出还是未完成状态下的正常退出。

monitor 不检查单独 worker/server/client 的 PID，不扫描活动日志中的 OOM、NaN 或 Traceback，
也不覆盖人工增加的辅助 shard。因此三路进程、三组日志和异常分类仍由人工半小时轮询完成；
发现异常只汇报，不自行修改数学协议。

## 6. 结果聚合与最终核验

`a116e48` 聚合器按固定 50 任务表读取结果。除导入的 `adjust_bottle` 外，每个任务只接受当前
任务目录中唯一的 `res.json`；episode 明细由文件名形如 `<index>_*_<True|False>.mp4` 的视频恢复，
seed 为 `stseed` 起点加 episode index。一个任务只有在 `res.json.total_num == 20` 且恰有 20 个
可解析 episode 视频时才标记为 `complete`。历史聚合器没有交叉核验 `succ_num` 与视频成功数，
也没有拒绝重复 episode index，因此不能仅凭其 `complete` 字段证明最终严格一致性。

当前聚合器优先读取输出根中已固化的 manifest，并将可验证 episode 数 `>= target` 的任务标为
`complete`，以支持“超过目标仍保留全部”的复用语义。`result_consistent` 比较 `res.json` 与视频的
数量和成功数，但目前不是阻止 `complete` 的硬门槛。聚合写入使用临时文件加 `os.replace`；调用方
以 `.aggregate.lock` 的 `flock` 串行化 worker/monitor 更新。各输出文件分别原子替换，但不是跨文件
单事务提交。

`aggregate.json` 汇总完成任务数、episode 数、成功/失败数、micro 成功率和已完成任务的
macro 成功率；每个任务同时记录成功率和 Wilson 95% CI。聚合器还原子刷新输出目录内的
`trials.csv`、`task_summary.csv`、`LIVE_STATUS.md`，并同步自动生成的论文 live status 与两份
CSV。运行中的 partial task 只表示进度，不作为论文最终任务级估计。

原始全任务实验的最终人工验收仍要求 50 个任务各恰好 20 个 episode、每任务明细恰好 20 条、
全局恰好 1,000 条、成功数加失败数等于 1,000，且任务、seed、视频无缺失、重复或额外项。
当前聚合器的 `complete` 本身不足以证明这些条件，最终必须另做严格 verifier。最终报告使用全
1,000 回合的 micro 成功率、50 个任务成功率的 macro 平均和逐任务 Wilson 95% CI。

OOM、NaN、Traceback、任务非零退出、自动重拉、结果数量不一致和连续失败目前没有统一自动
聚合字段；最终异常统计必须结合活动/历史日志、`failures.log`、`status_reports.jsonl`、
`.failed` 标记和人工轮询记录生成。

## 7. 运行与证据位置

- 批量入口：`FBFM/wam/lingbot-va/script/run_robotwin_all_tasks_fbfm.sh`
- 聚合器：`FBFM/wam/lingbot-va/script/aggregate_robotwin_all_tasks.py`
- 监控器：`FBFM/wam/lingbot-va/script/monitor_robotwin_all_tasks.py`
- 协议说明：`FBFM/wam/lingbot-va/docs/fbfm_runtime_modes.md`
- 输出根目录：`FBFM/wam/lingbot-va/robotwin_outputs/fbfm_all_tasks_20`
- 每任务日志：`tasks/<task>/logs/client.log` 和 `tasks/<task>/logs/server.log`
- 聚合与轮询：`aggregate.json` 和 `status_reports.jsonl`

### Claim-to-code 证据表

历史编排语义应使用 `git show a116e48:<path>` 查看，不能用当前已修改的普通脚本路径代替。

| 声明 | 冻结证据 |
| --- | --- |
| `H=32,d=16,s=16` | `wan_va/configs/va_robotwin_cfg.py:17,23,35-36`; `wan_va/wan_va_server.py:833` |
| video 25+1 / action 50+1 | `wan_va/configs/va_robotwin_cfg.py:31-33`; `wan_va/wan_va_server.py:1060-1190`; `wan_va/lingbot_va_bridge.py:787-794` |
| 26/16 离散 grant | `evaluation/robotwin/pseudo_async.py:48`; `evaluation/robotwin/eval_polict_client_openpi.py:591-736`; `wan_va/wan_va_server.py:1088` |
| 四 observation 成组编码一次 | `wan_va/wan_va_server.py:624-652`; 初始 feedback VAE prime 为 `567-580` |
| state/action mask 与原生归一化 | `wan_va/lingbot_va_bridge.py:121-156,177-247`; `wan_va/wan_va_server.py:818-914` |
| 原生 KV/prediction cache | `wan_va/wan_va_server.py:1222-1261,1418-1421`; `wan_va/modules/model.py:358` |
| `a116e48` 三分片与任务级恢复 | `git show a116e48:wam/lingbot-va/script/run_robotwin_all_tasks_fbfm.sh`, lines 12-108 |
| `a116e48` 聚合与 Wilson CI | `git show a116e48:wam/lingbot-va/script/aggregate_robotwin_all_tasks.py`, lines 70-157 and 263-326 |
| `a116e48` 监控/重拉边界 | `git show a116e48:wam/lingbot-va/script/monitor_robotwin_all_tasks.py`, lines 15-120 |

## 8. 2026-07-25 运行范围变更附记

原始 50 x 20 launcher 已按操作者要求暂停，输出目录完整保留。暂停快照为 4/50 个任务
完成、87/1,000 个已记录 episode、79 次成功和 8 次失败；该目录中的 `status: running`
是最后一次聚合时写入的陈旧字段，当前没有对应 launcher/server/client 进程。不得把这 87
个 partial episode 当作全任务最终估计，也不得把后续子集运行误写成原始 1,000 回合实验已恢复。

重启工作站后，当前授权范围改为 11 个不超过 800 仿真步的 `demo_clean` 任务；已有至少
10 个有效 episode 的任务保留全部旧结果，其余 7 个任务各收集 10 个新 episode。当前活动
输出根目录为 `robotwin_outputs/fbfm_short_le800_clean_10`，独立运行记录为
`robotwin_fbfm_short_le800_clean_10_runbook.md`，自动论文表位于
`robotwin_fbfm_short_le800_clean_10/`。启动时先用两个 shard；随后按操作者指示增加一个只运行
`move_pillbottle_pad` 的辅助 shard。此编排变更不修改本记录第 1-3 节的单 episode 数学协议。

当前进程 checkout 为 `fix/dreamzero-rolling-feedback` 的
`c6025989a25cd32338ef5579c58d229c7c15db1c`。只读 revision 审计确认，本实验实际加载的
server、RoboTwin client、bridge/scheduler、配置和 `run_constraint_ablation.sh` 与
`a116e48d9c8956c7ee66360ae68007bc146abcc3` 字节一致；差异只在任务编排、聚合和文档。

## 9. 2026-07-26 第二批与新增任务编排附记

第一阶段已正常结束，共保留 11 个任务的 150 个 episode，137 次成功、13 次失败。四个
legacy 任务各已有 20 次结果；其余七个任务第一阶段各有 10 次。为把这七个任务补齐到
20 次，第二阶段使用独立输出根
`robotwin_outputs/fbfm_short_le800_clean_stage2_seed20000_10`，以
`ROBOTWIN_EVAL_SEED=1` 生成实际 seed 从 20000 开始的十次新评测。该批次不符号链接或覆盖
第一阶段结果，仍以三个独立 server/simulator shard 在 `29256..29258` 和
`29261..29263` 上运行；15 分钟 monitor 记录到独立的 aggregate、status JSONL 和论文表。

第二阶段完成后，严格 combiner 必须从 client log 恢复实际环境 seed，并证明四个 legacy
任务为 `4 x 20 = 80`、七个分批任务为 `7 x (10 + 10) = 140`、合计恰好 220 个 episode。
同一任务的两批实际 seed 不得重复；`res.json`、结果视频和成功计数必须一致。最终独立结果
包含逐任务 Wilson 95% CI、micro/macro 成功率和验证异常统计，不能把 live aggregate 的
`complete` 字段单独当作严格验收。

操作者随后补充 `place_burger_fries`，要求 `demo_clean` 下独立运行 20 次。该任务最大 500
仿真步，本机没有可复用结果。创建了独立输出根
`robotwin_outputs/fbfm_place_burger_fries_clean_20`、`stseed=10000` 和独立论文目录。10000 只是
候选环境 seed 的起点；expert scene 检查可能跳过无效 seed，最终 20 个实际 seed 必须从
client log 恢复，不能预先写成连续的 10000..10019。
由于三路运行时 GPU 已占用约 77--83 GiB/97.9 GiB，不能直接启动第四个模型 server。
等待器只有在某个第二阶段 shard 的全部任务均被 live aggregate 标记 complete、对应 worker 已退出、
无 `.failed`，且活动模型 server 数稳定降到两个以内后，才使用新端口 29259/29264 接入该
任务。这样它会与剩余 shard 并行，但任意时刻最多仍是三路；短暂端口空档或 worker 异常退出
不会被误判为空槽。该门槛是并发准入判据，不等于最终严格结果验收；启动后使用同一 900 秒
monitor 和最多三次 launcher 自动重拉。

第二阶段启动时 checkout 为 `fix/dreamzero-rolling-feedback` 的
`e482dccb6841f3a2bea73128e05b0954371ee9be`；本附记复核时 checkout 为
`fix/dreamzero-binary-state-mask` 的 `f71ec2e240dc4af50c10e0c12da8d5ae6cc4a84d`。
两次 revision 对上述 Lingbot-VA server、RoboTwin client、bridge、pseudo-async、robotwin
配置和单任务 runner 的工作树内容均与 `a116e48d9c8956c7ee66360ae68007bc146abcc3`
字节一致。新增内容只涉及任务选择、端口/分片编排、严格聚合和实验记录，不改变第 1--3 节的
数学协议、模型权重或单 episode 推理路径。原始 50 x 20 输出仍保持暂停，未被这些子集运行恢复。

## 10. 2026-07-26 seed 元数据审计附记

RoboTwin 在每个候选 seed 上先执行场景和 expert 检查；被拒绝的候选不会形成 episode，因此下一条
正式回合的实际环境 seed 可能跳号。当前 live 聚合器没有解析 client log 的 `current seed`，而是把
`stseed + video_index` 写入 `aggregate.json` 和 `trials.csv` 的 seed 字段。该字段只能解释为名义
episode 序号，不能作为实际 simulator seed 用于配对、去重或逐 seed 分析。

08:30 的逐条审计覆盖 Stage 1 的 150 条、Stage 2 的 45 条和 Burger 的 7 条，共 202 条已提交
结果。源聚合记录中有 129/202 条名义 seed 与 client log 的实际 seed 不同：Stage 1 为 99/150，
Stage 2 为 30/45，Burger 当前为 0/7。该差异不影响成功率：三批的 episode 数、成功数、
`res.json`、client 累计结果和 202 个非空 outcome 视频逐条一致，视频 True/False 顺序也与累计
成功数增量一致。

严格 combiner 以 client log 的 `current seed` 恢复 `actual_seed`。当前核心 195/195 以及加入
Burger 后 202/202 个 `(task, actual_seed)` 均唯一；Stage 1 与 Stage 2 在同一任务内没有实际 seed
碰撞。论文统计和最终去重必须使用严格合并产物的 `actual_seed`，不得使用各 live source 的名义
seed 字段。本次只补充记录和审计口径，没有修改运行中的聚合器、推理协议或实验进程。
