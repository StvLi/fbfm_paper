# FBFM Theory-to-Implementation Handover

本文档仅记录理论整理过程中经确认的问题及其关闭状态，供负责代码与实验的同学核查。

**当前审计基线：** FBFM `3ecac79bb1730b426f5338afa32a9e77b4bf74cb`；上游 LingBot-VA `7c6ffa9bfc4b83582cafc860fab4c82cc7deeeeb`。

## 当前状态

此前在 `3604b457a24485cddf326a997e48955b7ca6b548` 确认的两项问题已在当前分支代码路径中关闭：

1. FBFM 模式已同时启用 dynamic state feedback 和 previous-action constraint；其 action target/mask 与 RTC 模式一致。
2. 新到达的 state feedback 进入队列，并在后续 video-flow solver 边界更新 active chunk 的 target/mask，而非只在推理开始时读取一次快照。

以上为代码审计结论。正式实验仍需通过 solver-step 日志和消融结果验证这两条路径在最终实验 commit 中保持生效。当前未记录新的、已经确认但尚未关闭的代码与理论不一致问题。
