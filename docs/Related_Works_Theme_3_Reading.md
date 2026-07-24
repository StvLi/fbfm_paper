# Related Works Theme 3: Inference-Time Guidance, Asynchronous Execution, and Feedback

本文档记录第三主题的近邻方法精读、统一比较与中英文工作稿。本主题中的论文与
FBFM 关注同一组部署矛盾：生成式策略需要 action chunk 以保持时间一致性并摊薄推理
成本，但 inference delay、open-loop execution 和模型误差又要求控制器及时吸收新的
环境信息。因此，本主题不按论文名称中的 `asynchronous`、`feedback` 或
`training-free` 归类，而是检查反馈究竟来自哪里、作用于什么变量、何时进入生成器，
以及为此需要训练哪些组件。

阅读范围覆盖各论文的摘要、Introduction、方法、核心实验、Conclusion 和与训练边界
有关的附录。所有核心论文均按计算机科学方法论文处理，即按“建立在什么接口上、改变
什么机制、由哪些实验支持”定位。下面明确区分论文自身的 claim、可由方法直接确认的
事实，以及本文对其与 FBFM 关系的判断。

## 1. 统一比较维度

每项近邻工作均沿以下维度审阅：

1. **问题**：主要解决跨 chunk 连续性、prediction--execution misalignment、反应
   延迟、目标 steering，还是 WAM prediction drift？
2. **反馈来源**：previous actions、最新 observation、proprioceptive state、模型内部
   confidence、外部 objective，还是 success/failure activation pairs？
3. **反馈对象**：action sample、action queue、policy condition、one-step world-model
   prediction、WAM hidden activation，还是显式生成的 multi-step state future？
4. **进入位置**：候选选择、initial noise、sampling velocity/score、residual head、
   context routing、observer state，还是 transformer activation？
5. **生效时序**：生成前、生成中但执行前、执行与 solver 交错、环境 step 之间，还是
   active chunk 的后续 solver evaluation？
6. **训练边界**：冻结 base policy 是否等于完整方法无需训练；是否还需要 correction
   head、specialized noise schedule、dynamics model、offset augmentation 或 architecture
   co-training？
7. **WAM 范围**：方法是否显式生成未来状态；真实状态是否对齐到 future slot；state
   residual 是否能直接影响 action generation？

## 2. 精读与筛选表

筛选标记：**Core** 为正文中不可替代的直接来源或近邻；**Grouped** 适合合并引用；
**Reserve** 已审阅但当前不承担必要论点。

| # | 文献 | 主要贡献（简短） | 在 FBFM 论述中的作用 | 筛选 |
|---:|---|---|---|---|
| 1 | Liu et al., *Bidirectional Decoding* (BID), ICLR 2025, arXiv:2408.17355 | 每个控制步采样多个 action chunks，以 backward coherence 和 forward contrast 选择兼顾历史一致性与未来可行性的候选。 | RTC 之前的 action-chunk test-time decoding 代表；说明连续性也可通过 sample selection 处理。 | Core |
| 2 | Black et al., *Real-Time Execution of Action Chunking Flow Policies*, NeurIPS 2025 | 将必然执行的 prefix、soft overlap 和自由 suffix 写成 inference-time inpainting，并通过伪逆引导修改冻结 Flow-Matching policy。 | FBFM previous-action constraint 与 sampling-time VJP 的直接技术来源。 | Core |
| 3 | Black et al., *Training-Time Action Conditioning for Efficient Real-Time Chunking*, 2025, arXiv:2512.05964 | 训练时模拟 delay，以 clean prefix 条件化 postfix generation，从而移除部署时 VJP。 | RTC 的训练期分支；用于精确定义 FBFM 的 training-free 对照。 | Core |
| 4 | Liu et al., *Learning Native Continuation for Action Chunking Flow Policies* (Legato), RSS 2026 | 通过部分已知 action 与 noise 的 schedule-shaped initialization 学习 policy-native continuation。 | RTC 后续的 training-time continuity 分支。 | Grouped |
| 5 | Ho et al., *Start Right, Arrive Right* (PAINT), 2026, arXiv:2606.19774 | 通过 backward Euler inversion 选择 initial noise，并以 repainting 构造一致的新 chunk。 | 说明 action continuity 可在 flow 起点而非 velocity guidance 中实现。 | Grouped |
| 6 | Liu et al., *Action-Prior Denoising for Smooth Real-Time Chunking* (Soft RTC), 2026, arXiv:2605.25537 | 以 partially denoised overlap tokens 表示可编辑的 action prior，扩展 training-time RTC 的 binary prefix。 | RTC action-overlap 约束的软先验扩展。 | Reserve |
| 7 | Zhan et al., *SEAM*, 2026, arXiv:2607.04609 | 使用前一 chunk 的未执行 tail 构造 time-dependent target，并在 Euler step 后作 closed-form correction。 | 无反向传播的 inference-time action-continuity 分支。 | Reserve |
| 8 | Ye et al., *RA-DP*, IROS 2025, arXiv:2503.04051 | 用 mixed-noise action queue 将一次 denoising、队首执行和队尾入队交错，并允许 inference-time loss guidance。 | 环境交互与 denoising 细粒度交错的重要近邻；必须限定其专门训练的 queue model。 | Core |
| 9 | Sendai et al., *Leave No Observation Behind* (A2C2), 2025, arXiv:2509.23224 | 每个控制步用最新 observation、base action、chunk position 和 base features 预测 residual action。 | 真实观测逐步修正待执行动作的强 action-space peer。 | Core |
| 10 | Tang et al., *VLASH*, 2025, arXiv:2512.01031 | 用 committed actions roll forward robot state，并通过 temporal-offset fine-tuning 使策略使用 execution-time state。 | 处理 prediction--execution state misalignment，但使用预测 proprioception 而非新到达环境测量。 | Core |
| 11 | Jiang et al., *AsyncVLA*, 2025/2026, arXiv:2511.14148 | 首轮 SFM 后估计 token confidence，再以 AFM 选择性重生成 low-confidence actions。 | 生成中 action self-correction 近邻；反馈来自模型内部 confidence，且依赖统一训练。 | Grouped |
| 12 | Sun et al., *TIDAL*, 2026, arXiv:2601.14945 | 低频 semantic intent 与高频 micro-control 解耦，交错 single-step flow integration 和短 action execution。 | 执行--生成交错的架构化方案；依赖 misalignment training 与 motion predictor。 | Grouped |
| 13 | Wu et al., *DCDP*, ICRA 2026, arXiv:2603.01953 | 使用 observation history 的 learned dynamic features 和 action VAE decoder 对冻结 Diffusion Policy 的 chunk 做逐步修正。 | 真实 observation history 的 action correction peer；`training-free` 只指不重训 base policy。 | Grouped |
| 14 | Lu et al., *FASTER*, 2026, arXiv:2603.19199 | 以 horizon-aware flow schedule 优先求解 near-term actions，降低 time-to-first-action。 | 主要解决 reaction latency，而非吸收真实状态测量；作为侧向边界。 | Reserve |
| 15 | Du and Song, *DynaGuide*, NeurIPS 2025, arXiv:2506.13922 | 用单独训练的 latent dynamics model 预测候选动作后果，并将 desired/undesired outcome objective 的梯度回传到 action denoising。 | world-model-based sampling guidance 近邻；来源是目标条件而非执行误差反馈。 | Core |
| 16 | An et al., *Feedback World Model Enables Precise Guidance of Diffusion Policy*, 2026, arXiv:2605.15705 | 维护 observer-like feedback state，以真实 prediction--observation residual 校正 one-step latent prediction，再指导独立 diffusion policy。 | 与 FBFM 共享“真实 observation 在推理时校正 latent dynamics”的核心认识，是最重要的同期概念近邻。 | Core |
| 17 | Cai et al., *AHA-WAM*, 2026, arXiv:2606.09811 | 低频 video planner 产生可复用 context，高频 action DiT 通过最新 observation 路由该 context，并配合 horizon-adaptive offset training。 | WAM 内异步 world/action rhythm 和 observation refresh 的架构近邻。 | Core |
| 18 | Hong et al., *Steering Robustness into World Action Models via Mechanistic Interpretability and Optimal Control* (WA-LQR), 2026, arXiv:2607.14943 | 在 contrastive activation subspace 中局部线性化 WAM block dynamics，并以 LQR feedback steering hidden activations。 | training-free WAM inference steering 的最新直接近邻，但其 reference signal 与可适用性不同。 | Core |
| 19 | Agouzoul, *Understanding Asynchronous Inference Methods for Vision-Language-Action Models*, 2026, arXiv:2605.08168 | 在统一代码与 delay sweep 中比较 IT-RTC、TT-RTC、VLASH 和 A2C2。 | 作为训练成本、delay sensitivity 和实现 caveat 的二级交叉证据，不替代原论文。 | Reserve |
| 20 | Yan et al., *ProgressVLA*, 2026, arXiv:2603.27670 | 以 inverse-dynamics world model 和 progress estimator 构造 differentiable action-token guidance。 | 与 DynaGuide 同属 objective steering；不使用真实 execution residual。 | Reserve |

## 3. 核心方法卡片

### 3.1 BID：候选选择式 closed-loop decoding

- **论文主张**：action chunking 能捕获 demonstration 中的长时依赖，但会降低对意外状态的
  reactivity；BID 试图同时保留两者。
- **机制事实**：每个 timestep 从冻结的 generative policy 采样多个 chunks。Backward
  coherence 偏好与先前决策对齐的样本；forward contrast 使用强、弱 checkpoints 的相对
  likelihood 选择更可信的未来计划。
- **反馈时序**：最新 observation 触发下一轮多候选采样，但不存在对单个 active flow
  trajectory 的连续测量注入。
- **训练与计算边界**：不修改 policy 参数，但需要批量采样；forward contrast 还依赖弱
  checkpoint。因此它是 test-time decoding，而不是零额外模型/计算的单轨生成。
- **与 FBFM 的共同点**：都处理 action chunk 带来的一致性--反应性矛盾，并使用之前的
  决策稳定跨 chunk 行为。
- **关键区别**：BID 在 sample level 选择 action chunks；FBFM 在一条 active WAM flow
  内，用时间对齐的 state/action measurements 修改 velocity field。

### 3.2 两版 RTC：FBFM 的直接 action-space 来源

- **Inference-time RTC 的贡献**：机器人继续执行前一 chunk 时生成后一 chunk，将必然
  执行的 prefix 固定，将后续 overlap 设为 soft constraint，并保留自由生成的 suffix。
- **生成接口**：RTC 预测 clean action endpoint，根据 mask discrepancy 构造
  pseudoinverse-guided correction，并以 VJP 修改后续 flow evaluations。Base flow policy
  保持冻结。
- **Training-time RTC 的贡献**：训练时采样 inference delay，把 clean prefix 作为条件，
  只对 postfix 计算 Flow-Matching loss；部署时直接生成 prefix-consistent postfix，避免
  inference-time VJP。
- **与 FBFM 的继承关系**：FBFM 的 previous-action branch 直接继承 RTC 的跨 chunk
  committed-action 约束思想，且同样利用可微 clean-endpoint predictor。
- **FBFM 的增量**：RTC 的 measurement coordinates 位于 action chunk。FBFM 进一步把
  执行产生的真实 latent state 对齐到 WAM future-state slots，并允许每次新测量在同一
  active solver 的后续 evaluation 中生效。
- **不应使用的表述**：不能把 RTC 简化为“只冻结 prefix”，也不能说 RTC 已提供 WAM
  state feedback；两者都会模糊 FBFM 的真正增量。

### 3.3 RTC 后续连续性方法：约束可以放在不同生成位置

- **Legato** 将 continuation 纳入训练分布，以 known-action/noise mixture 和 per-step
  schedule reshaping 学习自然延续；其优势来自 training-time adaptation。
- **PAINT** 将连续性重写为 initial-noise selection：先用 backward Euler inversion 找到
  合适噪声，再让未修改的 flow ODE 生成下一 chunk。它无需梯度或重训，但仍以 action
  prefix consistency 为目标。
- **Soft RTC** 在 training-time RTC 中把非 prefix 的 overlap 从纯噪声改为 partially
  denoised action prior，表达“可编辑但应接近旧计划”的连续程度。
- **SEAM** 使用 previous unexecuted tail 作为 analytic reference，在 Euler step 后进行
  closed-form correction，避免穿过 policy network 的反向传播。
- **对 FBFM 的启示**：这些工作改进了同一个 action-continuity 目标的训练位置、起点或
  solver update。它们没有使用真实环境 observation 去约束 WAM future-state stream，
  因而适合合并引用而非逐一展开差异。

### 3.4 RA-DP：denoising 与环境执行交错

- **论文主张**：以 action queue 将 diffusion sampling 重新安排为高频 replanning，并在
  sampling 中接收动态 guidance。
- **机制事实**：队列中的 action coordinates 具有递增 noise levels；每个循环做一次
  denoising，计算基于最新 dynamic feedback 的 differentiable loss guidance，执行并移除
  队首 clean action，再向队尾加入新 noisy action。
- **训练边界**：新增 guidance signal 可以在 inference time 使用，不需为该 signal 重训；
  但 mixed-noise queue 本身与标准 Diffusion Policy 的 uniform-noise training 不匹配，
  论文明确为 varying-noise action queue 训练了专用 U-Net。因此不应把 RA-DP 写成适用于
  任意冻结 Diffusion Policy 的完整 training-free wrapper。
- **与 FBFM 的共同点**：两者都允许环境演化和 iterative generation 交错，并使后到信息
  影响尚未完成的生成。
- **关键区别**：RA-DP 的在线变量是 action queue，反馈通常被编码为 action-space loss；
  FBFM 的真实 observation 被编码为 time-aligned latent-state measurement，并在 WAM 中
  与 committed actions 共享受约束生成接口。

### 3.5 A2C2：每步 observation-conditioned residual correction

- **论文主张**：不重训大型 base VLA，在每个控制步用轻量 correction head 恢复 action
  chunk 的 closed-loop responsiveness。
- **机制事实**：correction head 输入最新 observation、base action、chunk position 和
  base-policy features，并输出要加在当前待执行 action 上的 residual。
- **训练边界**：base policy 可冻结，但 correction head 必须使用 demonstration target 与
  base-policy outputs 训练。Kinetix 实例约 0.31M 参数；LIBERO 实例包含视觉编码与
  transformer，约 32M 参数。
- **与 FBFM 的共同点**：真实 observation 逐步到达，且可以在不重新调用大型 base model
  的情况下影响 chunk 内后续执行。
- **关键区别**：A2C2 在 action execution interface 上修正单步动作，不修改 active
  Flow-Matching trajectory，也不维护或校正显式 WAM future-state stream。

### 3.6 VLASH：用已承诺动作估计 execution-time state

- **论文主张**：异步推理的核心错位是 policy 在 (s_t) 开始计算，但新动作在
  (s_{t+\Delta}) 才执行。VLASH 使用已知 actions roll forward robot state，并让 policy
  以该 future state 为条件。
- **机制事实**：视觉 observation 仍来自 inference-start time；被更新的是 robot
  proprioceptive state。论文发现原 VLA 不会自然利用这一组合，因此使用 temporal-offset
  augmentation 同时偏移 state 和 target action，并保持视觉帧固定。
- **训练边界**：没有新增部署网络和推理 guidance，但需要 fine-tuning 使 policy 学会使用
  rolled-forward state；不是对冻结 checkpoint 的纯 inference-time correction。
- **实现 caveat**：统一比较论文报告，在 LIBERO 中 state/action 维度不匹配，所复现版本
  使用 demonstration 中的 ground-truth future state，应将该组结果视为 privileged upper
  bound。该 caveat 是二级研究的实现报告，不宜反推 VLASH 的全部实验。
- **与 FBFM 的共同点**：都利用前一 chunk 已承诺动作处理 generation 与 execution 的时间
  对齐。
- **关键区别**：VLASH 预测未来 robot state 以修正 conditioning；FBFM 使用执行后实际
  获得的 environment observation 作为 measurement，约束正在生成的 future slots。

### 3.7 AsyncVLA 与 TIDAL：专门训练的异步 Flow-Matching 架构

**AsyncVLA**：

- 先以 synchronous FM 完成初始 action chunk，再由 4-layer transformer confidence
  rater 标记 low-confidence tokens；AFM 仅重新噪化并生成这些 tokens，高置信动作作为
  context。
- 修正在动作执行前完成，反馈信号来自模型内部 token error proxy，而非物理执行返回的
  observation。
- SFM 与 AFM 必须 unified training；confidence rater 另行训练且约 308M 参数。论文
  ablation 显示去除 unified training 会显著损害性能。

**TIDAL**：

- 低频 macro loop 缓存 VLM semantic intent，高频 micro loop 使用最新 proprioception
  与 differential motion feature，交错 single-step flow integration 和短 chunk execution。
- 其高频性来自计算预算重排，而不是在一个多步 active flow 上持续追加 measurement mask。
- 需要 temporally misaligned training、time-biased Flow-Matching loss、horizon weighting
  和额外 motion predictor。

**与 FBFM 的关系**：两者证明异步 schedule 可以被直接学习，并可能获得更低延迟；FBFM
研究互补的 deployment setting，即不改变 WAM training objective 或架构，而在冻结
stage-wise/joint WAM 的现有 solver interface 上注入真实反馈。

### 3.8 DCDP：冻结 base policy 不等于完整方法无需训练

- **机制事实**：base Diffusion Policy 先产生 open-loop chunk；observation history 经
  self-supervised dynamic feature encoder、temporal/cross attention 形成 fast feature；
  pretrained action VAE encoder/decoder 再逐步输出修正动作。
- **训练边界**：论文的 Stage 1 使用 labeled demonstrations 和 self-supervised differential
  loss 训练 dynamic module 与 asymmetric action VAE；Stage 2 才冻结这些组件和 base
  policy。因此 `training-free` 准确含义是“不重训原 Diffusion Policy 并在第二阶段不更新
  参数”，而非“无需训练任何新增模块”。
- **与 FBFM 的共同点**：都使用最新 observation 对 action chunk 作 step-level correction。
- **关键区别**：DCDP 的 correction 由另训 fast policy/decoder 完成，作用于 base chunk 的
  action readout；FBFM 直接使用 pretrained WAM endpoint Jacobian，不引入 task-specific
  correction network，并同时约束 latent state future。

### 3.9 DynaGuide：dynamics-model objective steering

- **论文主张**：将 dynamics model 与 base diffusion policy 解耦，使 off-the-shelf policy
  可以在推理时朝多个 desired outcomes、远离 undesired outcomes。
- **机制事实**：单独训练的 transformer dynamics model 在冻结 DINOv2 latent 中预测
  candidate action 的远期 outcome；与 goal/anti-goal images 的 latent distance 构成
  guidance metric，其 action gradient 修改 diffusion denoising。
- **训练边界**：base policy 可冻结，但 dynamics model 必须使用多样 robot interaction
  data 训练，并对 noisy actions 做 augmentation。
- **与 FBFM 的共同点**：都通过 differentiable dynamics-related signal 修改 iterative
  action generation。
- **关键区别**：DynaGuide 的信号是用户给定的 outcome preference，目标是 behavior
  steering；FBFM 的信号是物理执行揭示的 time-aligned state measurement，目标是消除
  WAM prediction 与实际转移之间的不一致。

### 3.10 Feedback World Model：最接近的 latent feedback peer

- **论文主张**：执行后 observation 能揭示 learned dynamics 的误差，因此 world model
  不应始终作为 open-loop predictor；轻量 feedback state 可在部署时校正预测，无需参数
  更新。
- **机制事实**：方法维护 auxiliary belief \(\bar z_t\)，以
  \(e_t=z_t-\bar z_t\) 修正 candidate action 的 one-step latent velocity。执行 clean action
  后用同一 corrected velocity 推进 \(\bar z_{t+1}\)，下一真实 observation 再形成新的
  residual。Corrected one-step prediction 通过 expert-latent energy 指导独立 diffusion
  policy。
- **训练边界**：部署时无 parameter update，但需要预先训练 task-specific world model，
  并从 expert latent set 构造 policy guidance；“无额外训练数据”不等于无需已有
  demonstration/world-model training。
- **理论边界**：附录证明在 bounded dynamics residual 与适当 feedback gain 下，observer
  error 收敛到有界邻域，并将该结果关联到 executed action 的 corrected one-step
  prediction。它不是 pseudoinverse guidance 或 multi-step WAM flow 的收敛证明。
- **与 FBFM 的共同点**：两者独立得出同一高层认识，即真实 observation 应在 inference
  time 进入 latent dynamics，而不是只刷新下一次 open-loop history。
- **关键区别**：Feedback World Model 在环境 decision 之间更新 observer residual，并以
  one-step world model 指导独立 policy；FBFM 将 \(z_{t+i}\) 对齐到显式 multi-step WAM
  future 的特定 slot，并在该 chunk 仍在 Flow Matching 时更新 mask/velocity。FBFM 同时
  处理 state measurement 和 cross-chunk action commitment。
- **互补性**：其 observer stability analysis 支持“反馈可以抑制 latent drift”的一般动机；
  FBFM 则给出 sampling-time、time-aligned pseudoinverse formulation。两种证明对象和
  system boundary 不应混写。

### 3.11 AHA-WAM：以训练得到的异步 world/action rhythm 吸收 observation

- **论文主张**：world prediction 与 action execution 不必共享相同 temporal resolution；
  video branch 可作为低频 planner，action branch 作为高频 executor。
- **机制事实**：video DiT 维护 rolling K/V memory 和 reusable layerwise context；最新
  observation 经 Observation-Guided Video-Context Routing 将 planner context 变为
  chunk-specific context，再供 action DiT denoise。
- **训练边界**：需要 dual-DiT architecture、joint world/action Flow-Matching training、
  horizon-adaptive offset training；快速版本还使用 action-path ODE distillation。
- **重要范围**：部署时不显式 decode future frames；video DiT 的主要输出是 planner
  context。其 `observation-guided` 含义是 context adaptation，不是把观测作为 endpoint
  measurement 施加到 active video flow。
- **与 FBFM 的共同点**：都认可 WAM 中 world 与 action stream 应在执行期间接收新
  observation，并显式讨论 asynchronous world/action timing。
- **关键区别**：AHA-WAM 把这一能力学习进专门架构；FBFM 是冻结现有 WAM 的
  inference-time mechanism，并保留和校正显式 future-state generation。

### 3.12 WA-LQR：对 WAM hidden dynamics 的 feedback steering

- **论文主张**：部分 WAM 的 robustness-relevant features 在 activation space 中具有
  低维线性结构，可通过 mechanistic intervention 提高 OOD robustness。
- **机制事实**：从 nominal/perturbed 或 success/failure pairs 提取 contrastive activation
  directions；randomized SVD 建立低维 subspace；沿 nominal trajectory 用 JVP/VJP 获得
  local block Jacobians；LQR 根据当前 feature-setpoint error 调整 transformer activations。
- **训练边界**：不微调 WAM weights，但部署前需要为目标 perturbation/task 收集 paired
  activations、做 separability analysis、SVD 和 local model construction。因此它是
  weight-preserving steering，而非无准备的 generic observation feedback。
- **架构边界**：论文在 Cosmos-Policy 和 DiT4DiT 中发现较强 steerability，在
  LingBot-VA 中发现较弱线性分离和不稳定的 intervention gain；作者也将跨 task/model
  applicability 列为 limitation。
- **与 FBFM 的共同点**：都在不更新 WAM parameters 的情况下，利用可微内部动态对
  inference trajectory 做 feedback correction。
- **关键区别**：WA-LQR 的 reference 是预先识别的 robustness feature setpoint，作用于
  hidden activations；FBFM 的 reference 是执行中直接获得的真实 states 与已承诺 actions，
  作用于具有明确时间坐标的 generated endpoints。FBFM 不依赖某个 robustness factor 在
  activation space 中线性可分。

## 4. 统一比较矩阵

| 方法 | 主要问题 | 信息/反馈来源 | 直接作用对象与位置 | 时序 | 新增训练 | 显式 WAM future-state feedback |
|---|---|---|---|---|---|---|
| BID | chunk consistency + reactivity | previous decisions、候选 likelihood | 多候选 action chunk 选择 | 每个 control step 重采样 | 否；需弱 checkpoint/多样本 | 否 |
| IT-RTC | inference delay + chunk continuity | committed/overlap actions | active action flow 的 pseudoinverse VJP | execution 与 next-chunk generation 并行 | 否 | 否 |
| TT-RTC | 同上，降低 inference overhead | clean action prefix | learned postfix generation | 训练时模拟 delay | 是 | 否 |
| PAINT | chunk continuity | previous action prefix | initial noise inversion/repainting | flow 开始前 | 否 | 否 |
| RA-DP | high-frequency replanning | dynamic loss signal + action queue | action denoising/queue | 每个 denoising step 执行动作 | queue policy 需要专门训练 | 否 |
| A2C2 | stale action correction | 最新 observation + base action | per-step residual action | chunk 执行期间 | correction head | 否 |
| VLASH | prediction--execution misalignment | committed actions 推演的 proprio state | policy conditioning | new chunk inference 开始时 | offset fine-tuning | 否 |
| AsyncVLA | action self-correction | internal confidence | low-confidence action-token AFM | 执行前二阶段生成 | unified SFM/AFM + rater | 否 |
| TIDAL | reaction latency | latest proprio + motion feature | single-step action flow | integration 与短执行交错 | misalignment training + predictor | 否 |
| DCDP | dynamic action response | observation history | learned fast feature/action decoder | chunk 内每个执行 step | fast module + action VAE | 否 |
| DynaGuide | objective steering | desired/undesired outcome images | dynamics gradient to action denoising | inference-time sampling | latent dynamics model | 否 |
| Feedback World Model | world-model drift | actual next observation residual | observer-corrected one-step latent prediction，再指导 policy | environment steps 之间 | pretrained WM + policy | one-step observer；非 active multi-step WAM flow |
| AHA-WAM | asynchronous WAM planning/execution | latest observation | routed planner context to action DiT | low-frequency planner/high-frequency executor | 专门架构与 offset training | context routing；部署时不显式 decode future |
| WA-LQR | WAM OOD robustness | contrastive feature setpoint + current activation | transformer hidden activation | layer/denoising-step feedback | 无 weight update；需 activation-system identification | 否 |
| **FBFM** | chunk-internal WAM re-grounding + action continuity | actual time-aligned latent states + committed actions | active WAM clean-endpoint velocity/context | 新反馈在同一 active chunk 的后续 solver evaluation 生效 | **否** | **是；stage-wise 或 joint multi-step future** |

## 5. 文献定位结论

### 5.1 不宜把第三主题写成单一“异步方法排行榜”

这些方法改变的 system layer 不同：BID 和 PAINT 处理 action sample/initialization；RTC、
RA-DP 和 DynaGuide 改变 iterative action generation；A2C2/DCDP 在执行接口加 learned
corrector；VLASH 改 policy conditioning；Feedback World Model 改 one-step latent
observer；AHA-WAM 改 WAM architecture；WA-LQR 改 hidden activation dynamics。
因此正文应先说明各自贡献，再限定问题边界，而不是暗示一种方法在所有维度“优于”另一种。

### 5.2 FBFM 的最小、可防守定位

FBFM 不主张首次提出 asynchronous action execution、inference-time action guidance 或
latent feedback。可以防守的组合增量是：

1. 在推理时保留 WAM 参数与训练目标不变；
2. 将 RTC 风格的 previous-action constraint 与真实 latent-state feedback 放入一个统一的
   masked pseudoinverse interface；
3. 把每个新到达的 \(z_{t+i}\) 对齐到 active multi-step future 的特定时间 slot，而不是
   聚合为 observer residual 或 history update；
4. 让该 measurement 在当前 chunk 后续 solver evaluations 中生效，而不是等到下一次
   inference call；
5. 覆盖 stage-wise 和 joint-generation WAM，并在 joint flow 中通过 cross-modal endpoint
   Jacobian 使 state discrepancy 直接产生 action-coordinate correction；
6. 不训练 correction head、dynamics model、confidence rater、offset-conditioned policy 或
   perturbation-specific activation controller。

### 5.3 写作风险

- 不写 `the first feedback method for WAMs`：Feedback World Model、AHA-WAM 和 WA-LQR
  已覆盖不同形式的 WAM/latent feedback。
- 不写 `all prior asynchronous methods are action-only`：AHA-WAM 使用 observation-guided
  context，Feedback World Model 校正 latent prediction，VLASH 使用 future proprio state。
- 不写 `RA-DP is fully plug-and-play`：其 novel guidance 可 training-free，但 action queue
  需要 mixed-noise training。
- 不写 `A2C2/DCDP are training-free` 而不加范围：它们冻结 base policy，但训练额外模块。
- 不把 Feedback World Model 的 observer bound 描述为 pseudoinverse guidance convergence。
- 不把 WA-LQR 的 activation feedback 与 environment measurement feedback 等同。
- 不在正文使用统一比较论文的 LIBERO VLASH 结果作强优劣结论；其 oracle future-state
  caveat 使该结果更适合作为实现提醒。

## 6. English Working Draft v0.1

Action chunking creates two coupled deployment problems: computation must overlap
with execution, while independently generated chunks must remain temporally
coherent. Bidirectional Decoding addresses this trade-off by sampling multiple
candidate chunks and selecting among them using backward coherence with previous
decisions and forward contrast between policy checkpoints [Liu et al., 2025].
Inference-time RTC instead acts inside a single Flow-Matching trajectory: it
represents actions already committed by the executing chunk as a frozen prefix,
uses a soft mask over later overlap, and applies pseudoinverse-guided inpainting to
a frozen policy [Black et al., 2025a]. Its training-time counterpart learns
prefix-conditioned postfix generation under simulated inference delays, removing
the sampling-time vector--Jacobian products at the cost of modifying training
[Black et al., 2025b]. Later approaches place the same continuity prior elsewhere,
including policy-native continuation learned by Legato and initial-noise selection
in PAINT [Liu et al., 2026; Ho et al., 2026]. These methods establish a rich design
space for cross-chunk action consistency; their constrained variables nevertheless
remain actions inherited from an earlier plan.

Other work targets responsiveness to information that becomes available during
execution. RA-DP interleaves one denoising update with dequeueing an executable
action and appending a noisy action, while admitting differentiable guidance from
dynamic signals [Ye et al., 2025]. Although new guidance objectives can be added
without retraining, its heterogeneous-noise action queue is itself learned with a
specialized training schedule. VLASH rolls the robot state forward under committed
actions and fine-tunes the policy with temporal offsets so that actions are
conditioned on an estimated execution-time proprioceptive state [Tang et al.,
2025]. A2C2 and DCDP instead use the latest observations to correct stale actions
through separately trained residual or dynamics-aware modules while keeping the
large base policy frozen [Sendai et al., 2025; Wu et al., 2026]. AsyncVLA refines
low-confidence action tokens before execution through a jointly trained
synchronous/asynchronous Flow-Matching model, whereas TIDAL combines stale semantic
intent with current proprioception in a trained micro-controller that interleaves
single-step flow integration and short action execution [Jiang et al., 2026; Sun et
al., 2026]. These approaches provide complementary choices among online
computation, specialized training, and action-space reactivity.

Dynamics-based guidance extends this discussion beyond action continuity.
DynaGuide backpropagates desired- or undesired-outcome objectives through a
separately trained latent dynamics model to steer the denoising of an off-the-shelf
diffusion policy [Du and Song, 2025]. More closely related to our motivation,
Feedback World Model independently closes the prediction--observation loop at
inference time: it maintains an auxiliary latent belief, uses the residual to the
observed state to correct one-step predictions, and converts those predictions
into action-aware guidance for a separate diffusion policy [An et al., 2026]. Its
analysis bounds the latent observer error; it does not analyze pseudoinverse
guidance of a multi-step WAM flow. AHA-WAM learns a different WAM-specific solution,
routing each current observation into reusable context from a low-frequency video
planner for a high-frequency action DiT [Cai et al., 2026]. WA-LQR preserves WAM
weights but steers robustness-related hidden activations toward setpoints identified
from contrastive rollouts and locally linearized block dynamics [Hong et al., 2026].
These studies demonstrate several useful forms of world or dynamics feedback, but
they differ in whether the reference is a task objective, an observer residual, a
routed context, or a learned activation feature.

FBFM connects the action-continuity and WAM-feedback lines through a common
measurement interface. It retains RTC-style committed actions as a fixed
cross-chunk constraint, while treating each newly observed latent state as a
dynamic, time-aligned measurement of the multi-step future that a WAM is still
generating. Updating the target and mask before subsequent solver evaluations lets
the measurement affect the active chunk rather than only the next inference call.
The same formulation applies to stage-wise and joint-generation WAMs; in the joint
case, cross-modal blocks of the clean-endpoint Jacobian transmit a state residual
directly to action coordinates. Unlike learned residual heads, offset-conditioned
policies, external dynamics models, or activation controllers, this correction
uses the frozen WAM's existing differentiable generation interface and introduces
no additional training.

## 7. 中文对照稿 v0.1

Action chunking 带来了两个彼此耦合的部署问题：一方面，模型计算必须与物理执行并行；
另一方面，彼此独立生成的 chunks 仍需保持时间一致性。Bidirectional Decoding 通过采样
多个候选 chunks，并依据与先前决策的 backward coherence 以及不同 policy checkpoints
之间的 forward contrast 进行选择，从而处理这一权衡 [Liu et al., 2025]。Inference-time
RTC 则直接作用于单条 Flow-Matching trajectory：它把 executing chunk 中已经承诺的
动作表示为 frozen prefix，对后续 overlap 使用 soft mask，并在冻结 policy 上施加
pseudoinverse-guided inpainting [Black et al., 2025a]。其 training-time 版本在模拟的
inference delay 下学习 prefix-conditioned postfix generation，以修改训练为代价消除
sampling-time vector--Jacobian product [Black et al., 2025b]。后续工作又把相同的
continuity prior 放在生成过程的不同位置，例如 Legato 学习 policy-native continuation，
PAINT 则通过选择 initial noise 获得一致的新 chunk [Liu et al., 2026; Ho et al., 2026]。
这些工作建立了丰富的跨 chunk 动作一致性设计空间；不过，其受约束变量仍然是从先前
计划中继承的动作。

另一组工作关注如何响应执行过程中才变得可用的信息。RA-DP 将一次 denoising update、
取出并执行队首动作以及向队尾加入 noisy action 相互交错，同时允许动态信号提供可微
guidance [Ye et al., 2025]。新的 guidance objective 可以在不重新训练的情况下加入，但
其 heterogeneous-noise action queue 本身需要专门的训练调度。VLASH 使用 committed
actions 推演 robot state，并以 temporal offsets 微调 policy，使动作生成以估计得到的
execution-time proprioceptive state 为条件 [Tang et al., 2025]。A2C2 与 DCDP 则使用最新
observations，通过另行训练的 residual 或 dynamics-aware module 修正 stale actions，
同时保持大型 base policy 冻结 [Sendai et al., 2025; Wu et al., 2026]。AsyncVLA 使用统一
训练的 synchronous/asynchronous Flow-Matching model，在执行前重新生成低置信 action
tokens；TIDAL 则在经过专门训练的 micro-controller 中结合 stale semantic intent 与当前
proprioception，并交错 single-step flow integration 和短 action execution [Jiang et al.,
2026; Sun et al., 2026]。这些方法在 online computation、specialized training 与
action-space reactivity 之间提供了互补选择。

基于 dynamics 的 guidance 将讨论从动作连续性进一步扩展出去。DynaGuide 将期望或不
期望 outcome 的 objective 通过另行训练的 latent dynamics model 反向传播，以引导现成
diffusion policy 的去噪过程 [Du and Song, 2025]。与本文动机更接近的是，Feedback World
Model 独立地在 inference time 闭合了 prediction--observation loop：它维护辅助 latent
belief，使用该 belief 与 observed state 之间的 residual 校正 one-step prediction，并将
校正后的预测转化为对独立 diffusion policy 的 action-aware guidance [An et al., 2026]。
其理论分析约束的是 latent observer error，而不是 multi-step WAM flow 上的
pseudoinverse guidance。AHA-WAM 学习了另一种 WAM-specific solution：它把每次当前
observation 路由到低频 video planner 的可复用 context，再供高频 action DiT 使用 [Cai
et al., 2026]。WA-LQR 保持 WAM weights 不变，但根据 contrastive rollouts 与局部线性化
block dynamics 所识别的 setpoint，对 robustness-related hidden activations 进行反馈控制
[Hong et al., 2026]。这些工作展示了多种有价值的 world/dynamics feedback，但它们使用
的 reference 分别是 task objective、observer residual、routed context 或 learned
activation feature。

FBFM 通过统一的 measurement interface 连接 action continuity 与 WAM feedback 两条
路线。它保留 RTC 风格的 committed actions，将其作为固定的跨 chunk 约束；同时，它把
每个新观测到的 latent state 视为 WAM 仍在生成的 multi-step future 上动态到达且时间
对齐的 measurement。在后续 solver evaluation 之前更新 target 与 mask，使该测量能够
影响 active chunk，而不是只能等待下一次 inference call。这一表述同时适用于 stage-wise
和 joint-generation WAM；在 joint case 中，clean-endpoint Jacobian 的 cross-modal blocks
会把 state residual 直接传递到 action coordinates。与 learned residual head、
offset-conditioned policy、external dynamics model 或 activation controller 不同，这一
校正直接使用冻结 WAM 已有的可微生成接口，不引入任何额外训练。

