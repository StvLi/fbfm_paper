# FBFM Theory-to-Implementation Handover

本文档仅记录在理论整理过程中经确认的代码与理论不一致问题，供负责代码与实验的同学核查。

**代码基线：** `3604b457a24485cddf326a997e48955b7ca6b548`

## 1. Previous-Action Constraint 被临时关闭

当前 Lingbot-VA 路径将 previous-action constraint 的模式设为 `None`。该设置仅用于临时调试，不属于 FBFM 的设计。

完整 FBFM 应同时包含：

- state feedback；
- previous-action constraint。

因此，代码与实验需恢复并验证 previous-action constraint，主方法不应以 `None` 模式为准。

## 2. State Feedback 未实时作用于正在运行的 Flow-Matching Chunk

执行当前 action chunk 时，新获得的真实观测经编码得到 \(z_{t+i}\)。该反馈应实时注入**正在进行 Flow Matching 的当前 chunk**，并影响其后续生成过程，从而实现 chunk 内、step 颗粒度的 state feedback。

当前实现只在推理开始时导出一次反馈快照；推理启动后新到达的 \(z_{t+i}\) 不会更新已传入当前 solver 的副本。因此，现有实现尚未满足上述时序要求。
