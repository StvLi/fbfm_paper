# FBFM Related Works Literature Map

本文档为 Related Works 的检索与写作底稿，不是最终正文。检索更新时间为 2026-07-24。候选文献按三条论证链组织，每篇文献必须承担明确作用；不预设引用数量目标，也不把本表全部写入正文。经典背景工作可以在说明领域目标和通用方法后合并引用，路线转折工作需要用短分句交代具体增量，而与 FBFM 直接相关的工作应独立说明问题、机制、适用边界和差异。

三个主题的逐篇精读、筛选结果和工作正文分别见
[Related_Works_Theme_1_Reading.md](Related_Works_Theme_1_Reading.md)、
[Related_Works_Theme_2_Reading.md](Related_Works_Theme_2_Reading.md) 和
[Related_Works_Theme_3_Reading.md](Related_Works_Theme_3_Reading.md)。

优先级说明：

- **A / 必引**：直接建立技术来源、问题定义或最近邻差异；
- **B / 支撑**：用于补齐历史脉络或证明领域发展趋势；
- **C / 审阅后决定**：近期或侧向相关，必须读完方法和实验后再判断是否进入正文。

证据状态说明：

- `原文已核`：已经检查本地 PDF 的相关章节或关键方法表述；
- `元数据已核`：标题、时间和摘要已通过 arXiv/出版信息核对，强比较仍需阅读全文；
- `经典条目`：书目信息和领域定位稳定，写具体结论时仍应回看原文。

## 1. Generative Modeling and World Models

### 1.1 本部分要回答的问题

1. Diffusion 和 Flow Matching 如何形成两类彼此相关的连续生成方法？
2. 为什么已知像素、mask 或一般线性测量可以在不重新训练生成器时进入采样过程？
3. World models 如何从紧凑 latent dynamics，发展到 action-conditioned visual simulation，再发展到推理时显式生成未来状态和动作的 WAM？
4. FBFM 为什么只针对保留测试时未来生成的 WAM，而不是所有利用视频训练的机器人策略？

### 1.2 候选文献

| 优先级 | 文献 | 作用于正文的具体论点 | 状态 |
|---|---|---|---|
| B | Sohl-Dickstein et al., *Deep Unsupervised Learning using Nonequilibrium Thermodynamics*, 2015 | diffusion generative modeling 的早期基础 | 经典条目 |
| A | Ho et al., *Denoising Diffusion Probabilistic Models*, 2020 | 建立 iterative denoising 生成范式 | 经典条目；RTC 原文引用 |
| A | Song, Meng, and Ermon, *Denoising Diffusion Implicit Models*, 2021 | 说明同一训练目标可对应非马尔可夫、较高效的采样轨迹 | 经典条目 |
| B | Song et al., *Score-Based Generative Modeling through Stochastic Differential Equations*, 2021 | diffusion 的连续时间表达，与 velocity/ODE 视角衔接 | 经典条目 |
| A | Lipman et al., *Flow Matching for Generative Modeling*, 2023, arXiv:2210.02747 | Flow Matching 的直接理论来源 | 元数据已核；RTC 与 \(\pi_0\) 原文引用 |
| A | Liu, Gong, and Liu, *Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow*, 2022/2023, arXiv:2209.03003 | 直线传输路径和高效 ODE 生成的代表工作 | 元数据已核；RTC 原文引用 |
| B | Rombach et al., *High-Resolution Image Synthesis with Latent Diffusion Models*, 2022 | 从 pixel generation 过渡到 latent generative modeling | 经典条目；\(\pi_0\) 原文引用 |
| A | Lugmayr et al., *RePaint: Inpainting using Denoising Diffusion Probabilistic Models*, 2022 | mask-conditioned image inpainting 的代表性背景 | 原文书目已由 RTC 核对 |
| A | Song et al., *Pseudoinverse-Guided Diffusion Models for Inverse Problems*, 2023 | FBFM pseudoinverse guidance 的直接来源，必须明确引用 | 本地原文已核 |
| A | Pokle et al., *Training-Free Linear Image Inverses via Flows*, 2023, arXiv:2310.04432 | 将 training-free inverse guidance 明确迁移到 flow models；RTC 的直接算法来源 | RTC 原文已核 |
| B | Mardani et al., *A Variational Perspective on Solving Inverse Problems with Diffusion Models*, 2023 | 支撑 diffusion inverse-problem 文献脉络；不承担 FBFM 的直接来源主张 | RTC 书目已核 |
| A | Ha and Schmidhuber, *World Models*, 2018, arXiv:1803.10122 | 经典“学习环境压缩表征并在想象中训练/控制”的起点 | 元数据已核 |
| A | Hafner et al., *Learning Latent Dynamics for Planning from Pixels* (PlaNet), 2019 | pixel observation 到 latent dynamics 与 online planning | 元数据已核 |
| A | Hafner et al., *Dream to Control: Learning Behaviors by Latent Imagination* (Dreamer), 2020 | latent imagination 直接支持策略学习 | 元数据已核 |
| B | Hafner et al., *Mastering Atari with Discrete World Models* (DreamerV2), 2021 | discrete latent world model 与规模化控制能力 | 元数据已核 |
| B | Hafner et al., *Mastering Diverse Control Tasks through World Models* (DreamerV3), Nature 2025; preprint 2023 | world-model control 跨任务扩展的代表 | 原文与出版信息已核 |
| B | Hansen, Wang, and Su, *Temporal Difference Learning for Model Predictive Control* (TD-MPC), 2022 | learned latent dynamics 与 receding-horizon control 的另一条经典路线 | RTC 书目和元数据已核 |
| B | Kaiser et al., *Model-Based Reinforcement Learning for Atari* (SimPLe), 2020 | pixel-space video prediction 与 imagined policy rollout 的代表 | 元数据与摘要已核 |
| B | Schrittwieser et al., *MuZero*, 2020 | 无需 observation reconstruction 的 planning-oriented latent dynamics | 原文元数据与摘要已核 |
| B | Voleti et al., *MCVD*, 2022 | conditional diffusion 从图像生成进入显式视频未来建模 | 元数据与摘要已核 |
| A | Alonso et al., *DIAMOND*, 2024 | diffusion visual world model 与 imagined agent training 的直接汇合 | 元数据与摘要已核 |
| B | Yang et al., *Learning Interactive Real-World Simulators* (UniSim), 2023/2024, arXiv:2310.06114 | 从视频生成走向 action-conditioned interactive simulator | 元数据已核 |
| B | Bruce et al., *Genie: Generative Interactive Environments*, 2024, arXiv:2402.15391 | 大规模视频生成模型作为可交互 world model 的代表 | 元数据已核 |
| B | Zhu et al., *IRASim: A Fine-Grained World Model for Robot Manipulation*, 2024, arXiv:2406.14540 | action-frame alignment 和机器人视频 world model | 元数据已核 |
| B | Zhen et al., *3D-VLA: A 3D Vision-Language-Action Generative World Model*, 2024, arXiv:2403.09631 | VLA 与 generative world modeling 汇合的早期代表 | RTC 书目已核 |
| B | Cheang et al., *GR-2: A Generative Video-Language-Action Model with Web-Scale Knowledge for Robot Manipulation*, 2024, arXiv:2410.06158 | video-language-action 生成式机器人模型背景 | RTC 书目已核 |
| B | Wu et al., *GR-1: Unleashing Large-Scale Video Generative Pre-training for Visual Robot Manipulation*, 2023, arXiv:2312.13139 | 从大规模视频生成预训练过渡到 future-image/action joint prediction | 元数据与摘要已核 |
| A | Li et al., *Causal World Modeling for Robot Control* (LingBot-VA), 2026, arXiv:2601.21998 | 论文用于统一 autoregressive video-action WAM 背景；发布代码作为 stage-wise FBFM 实例 | 原文已核；上游代码 commit `7c6ffa9` 已核，二者须分开表述 |
| A | Ye et al., *World Action Models are Zero-shot Policies* (DreamZero), 2026, arXiv:2602.15922 | joint-generation FBFM 实例，预训练视频 diffusion backbone | 元数据已核；正式比较需复查原文 |
| A | Yuan et al., *Fast-WAM: Do World Action Models Need Test-time Future Imagination?*, 2026, arXiv:2603.16666 | 建立互补边界：视频协同训练与测试时显式未来生成可以分离 | 元数据已核；全文待精读 |

### 1.3 预期写作链

建议压缩为两段。第一段用 DDPM、Flow Matching、RePaint、ΠGDM 和 Pokle 建立“连续生成 + training-free measurement guidance”。第二段从 World Models、PlaNet/Dreamer 过渡到 UniSim/IRASim，再用 LingBot-VA、DreamZero 和 Fast-WAM 收束到推理时未来生成的 WAM。Dreamer 系列不逐篇展开，可合并引用。

## 2. Diffusion and Flow-Matching Policies for Robot Control

### 2.1 本部分要回答的问题

1. 生成模型何时从图像生成进入 trajectory planning 和 visuomotor action generation？
2. Diffusion Policy、Flow-Matching policy 与 autoregressive VLA 的关系是什么？
3. Flow Matching 如何从专用机器人运动策略发展到大规模通用 VLA action expert？
4. \(\pi_0\) 与 \(\pi_{0.5}\) 的应用性能和广泛影响，如何体现 Flow Matching 作为连续机器人动作生成路线的现实价值与可扩展性？

### 2.2 候选文献

| 优先级 | 文献 | 作用于正文的具体论点 | 状态 |
|---|---|---|---|
| B | Zhao et al., *Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware* (ACT), 2023 | action chunking 在模仿学习中的代表性基础 | RTC 与 \(\pi_0\) 原文已核 |
| A | Janner et al., *Planning with Diffusion for Flexible Behavior Synthesis* (Diffuser), 2022, arXiv:2205.09991 | diffusion 用于轨迹规划，并将 inpainting 解释为状态/动作约束 | 元数据与 RTC 原文已核 |
| B | Ajay et al., *Is Conditional Generative Modeling All You Need for Decision-Making?* (Decision Diffuser), 2022/2023, arXiv:2211.15657 | 条件生成模型用于决策的代表性延伸 | RTC 原文已核 |
| B | Wang, Hunt, and Zhou, *Diffusion Policies as an Expressive Policy Class for Offline Reinforcement Learning*, 2022/2023, arXiv:2208.06193 | diffusion policy 作为多峰策略分布的决策模型 | RTC 原文已核 |
| A | Chi et al., *Diffusion Policy: Visuomotor Policy Learning via Action Diffusion*, 2023 | action sequence/chunk 作为条件 diffusion 生成对象的核心工作 | RTC 与 \(\pi_0\) 原文已核 |
| B | Ze et al., *3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations* (DP3), 2024 | Diffusion Policy 向 3D、跨场景泛化扩展 | 原文摘要、元数据与 RSS 2024 信息已核 |
| B | Chi et al., *Universal Manipulation Interface: In-the-Wild Robot Teaching Without In-the-Wild Robots*, 2024 | diffusion action policy 在真实数据收集和部署中的扩展 | RTC 原文已核 |
| A | Liu et al., *RDT-1B: A Diffusion Foundation Model for Bimanual Manipulation*, 2025, arXiv:2410.07864 | diffusion policy 参数量、数据规模和双臂控制能力扩展 | 原文摘要、元数据与 RTC 原文已核 |
| B | Brohan et al., *RT-1: Robotics Transformer for Real-World Control at Scale*, 2022 | 大规模 direct action prediction/VLA 背景 | 经典条目 |
| B | Brohan et al., *RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control*, 2023 | VLA 利用互联网语义知识进行动作预测 | RTC 原文已核 |
| B | Octo Model Team et al., *Octo: An Open-Source Generalist Robot Policy*, 2024 | 通用 action-chunk policy 和大规模跨 embodiment 数据背景 | RTC 原文已核 |
| B | Kim et al., *OpenVLA: An Open-Source Vision-Language-Action Model*, 2024 | autoregressive VLA 的开源代表，与 continuous generative action expert 对照 | RTC 原文已核 |
| A | Braun et al., *Riemannian Flow Matching Policy for Robot Motion Learning*, 2024, arXiv:2403.10672 | 补全 Flow Matching 在专用机器人运动策略中的早期发展与几何建模路径 | 原文摘要、元数据与 IROS 2024 信息已核 |
| B | Rouxel et al., *Flow Matching Imitation Learning for Multi-Support Manipulation*, 2024, arXiv:2407.12381 | Flow Matching 在连续机器人动作模仿中的早期扩展 | 原文摘要、元数据与 Humanoids 2024 信息已核 |
| B | Zhang and Gienger, *Affordance-based Robot Manipulation with Flow Matching*, 2025, arXiv:2409.01083 | Flow Matching 与 affordance-conditioned manipulation | 原文摘要与元数据已核 |
| B | Ding et al., *Fast and Robust Visuomotor Riemannian Flow Matching Policy*, 2024/2025, arXiv:2412.10855 | RFMP 从 proof-of-concept 向更强 visuomotor policy 扩展 | 元数据已核；全文待审 |
| B | Zhang et al., *FlowPolicy: Enabling Fast and Robust 3D Flow-based Policy via Consistency Flow Matching for Robot Manipulation*, 2024/2025, arXiv:2412.04987 | Flow Matching policy 的速度和 3D 泛化方向 | 元数据已核；全文待审 |
| A | Black et al., *\(\pi_0\): A Vision-Language-Action Flow Model for General Robot Control*, 2024, arXiv:2410.24164 | Flow-Matching action expert、大规模通用 VLA 与灵巧高频 action chunks 的代表性跃迁 | 本地原文已核 |
| A | Physical Intelligence et al., *\(\pi_0.5\): A Vision-Language-Action Model with Open-World Generalization*, 2025, arXiv:2504.16054 | \(\pi\) 系列对 Flow-Matching VLA 路线的延续和 open-world 扩展 | RTC 书目与元数据已核 |
| C | Gao et al., *VITA: Vision-to-Action Flow Matching Policy*, 2025, arXiv:2507.13231 | 视觉到动作 Flow Matching 的近期专用 policy | 元数据已核；需判断是否提供独特论点 |
| B | Zhao et al., *ALOHA Unleashed: A Simple Recipe for Robot Dexterity*, 2024 | action chunking/diffusion 路线在灵巧操作数据和训练 recipe 上的发展 | RTC 原文已核 |
| C | Bjorck et al., *GR00T N1: An Open Foundation Model for Generalist Humanoid Robots*, 2025 | 大规模通用机器人 policy 的双系统背景；并非 FBFM 直接前驱 | RTC 原文已核；视篇幅决定 |

### 2.3 预期写作链

建议使用三个连续段落。第一段为 Diffuser → Diffusion Policy → DP3/RDT，说明 diffusion 从 trajectory model 发展为可扩展 action generator。第二段用 RT-1/RT-2/Octo/OpenVLA 交代 generalist policy 的数据、cross-embodiment 与 VLM scaling 背景。第三段先以 RFMP 等工作简要补全 Flow Matching 在专用机器人运动策略中的发展，再重点定位 \(\pi_0\) 和 \(\pi_0.5\)：它们将 Flow-Matching action chunks 扩展到大规模通用 VLA，并以高频灵巧控制和开放世界泛化的应用效果推动这条技术路线获得广泛认可。由此自然引出 FBFM 对 Flow-Matching action generation 执行期反馈的关注。

## 3. Inference-Time Guidance, Asynchronous Execution, and Feedback

### 3.1 本部分要回答的问题

1. action chunking 的 inference delay、open-loop interval 和跨 chunk 不连续问题已有何种解决方案？
2. 哪些方法在采样时施加 constraints/guidance，哪些方法依赖专门训练、额外 dynamics model 或 rejection sampling？
3. 真实环境反馈进入的是动作生成、单步 world-model correction，还是 WAM 正在生成的多步 latent future？
4. FBFM 相对 RTC、RA-DP、DynaGuide、Feedback World Model 和近期 WAM steering 的增量是什么？

### 3.2 候选文献

| 优先级 | 文献 | 作用于正文的具体论点 | 状态 |
|---|---|---|---|
| A | Song et al., *Pseudoinverse-Guided Diffusion Models for Inverse Problems*, 2023 | masked pseudoinverse correction 的理论来源 | 本地原文已核 |
| A | Pokle et al., *Training-Free Linear Image Inverses via Flows*, 2023 | ΠGDM 到 continuous flows 的直接桥梁 | RTC 原文已核 |
| A | Janner et al., *Diffuser*, 2022 | diffusion inpainting 在 sequential decision-making 中用于 state/action constraints | RTC 原文已核 |
| A | Liu et al., *Bidirectional Decoding: Improving Action Chunking via Guided Test-Time Sampling*, ICLR 2025, arXiv:2408.17355v4 | 通过 backward coherence 与 forward contrast 在多候选 chunks 中兼顾历史一致性和 reactivity | 最新原文已核 |
| A | Black et al., *Real-Time Execution of Action Chunking Flow Policies* (RTC), 2025 | FBFM 的直接思想来源：frozen prefix、soft overlap、free suffix 与 training-free flow inpainting | 本地原文已核 |
| A | Black et al., *Training-Time Action Conditioning for Efficient Real-Time Chunking*, 2025, arXiv:2512.05964 | RTC 的训练期分支：模拟 inference delay 并学习 action-prefix conditioning，以替代推理期伪逆 guidance | 原文已核；需与 training-free RTC 分开表述 |
| B | Liu et al., *Learning Native Continuation for Action Chunking Flow Policies* (Legato), RSS 2026, arXiv:2602.12978 | 通过 training-time known-action/noise mixture 学习 policy-native continuation | 摘要与方法边界已核；合并引用 |
| B | Ho et al., *Start Right, Arrive Right* (PAINT), 2026, arXiv:2606.19774 | 通过 initial-noise inversion 与 repainting 保持 prefix consistency，无需梯度或重训 | 原文已核；合并引用 |
| B | Høeg, Du, and Egeland, *Streaming Diffusion Policy*, 2024, arXiv:2406.04806 | 通过 variable-noise training 实现少步、高频 policy synthesis | RTC 原文已核 |
| B | Prasad et al., *Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation*, 2024, arXiv:2405.07503 | 通过 distillation 降低 diffusion policy 采样延迟 | RTC 原文已核 |
| B | Wang et al., *One-Step Diffusion Policy: Fast Visuomotor Policies via Diffusion Distillation*, 2024, arXiv:2410.21257 | one-step policy 加速方向，与 feedback/inpainting 正交 | 元数据已核；全文待审 |
| A | Sendai et al., *Leave No Observation Behind* (A2C2), 2025, arXiv:2509.23224 | 用最新 observation 与 base action 每步预测 residual correction | 原文已核；base policy 冻结但 correction head 需训练 |
| A | Tang et al., *VLASH*, 2025, arXiv:2512.01031 | 用 committed actions roll forward robot state，并用 temporal-offset augmentation 学习 execution-time conditioning | 原文已核；统一比较中的 LIBERO oracle caveat 已记录 |
| A | Ye et al., *RA-DP: Rapid Adaptive Diffusion Policy for Training-Free High-frequency Robotics Replanning*, 2025, arXiv:2503.04051 | 环境交互与 denoising 交错、action queue 和外部 guidance 的近邻 | 原文已核；novel guidance 可 training-free，queue model 需 mixed-noise training |
| B | Xue et al., *Reactive Diffusion Policy: Slow-Fast Visual-Tactile Policy Learning for Contact-Rich Manipulation*, 2025, arXiv:2503.02881 | slow-fast feedback policy 的代表；依赖触觉和专门架构 | 元数据已核；全文待审 |
| A | Du and Song, *DynaGuide: Steering Diffusion Polices with Active Dynamic Guidance*, NeurIPS 2025, arXiv:2506.13922 | 外部 latent dynamics model 将 outcome objective 反传到 diffusion denoising | 原文已核；base policy 可冻结但 dynamics model 需单独训练 |
| C | *Real-Time Iteration Scheme for Diffusion Policy*, 2025, arXiv:2508.05396 | 另一种实时 diffusion-policy 迭代调度 | 元数据已核；需阅读全文判断是否与 RTC/RA-DP 重复 |
| A | Jiang et al., *AsyncVLA: Asynchronous Flow Matching for Vision-Language-Action Models*, 2025/2026, arXiv:2511.14148 | 非均匀 FM schedule、confidence-based token refinement；需要统一训练和另训 rater | 原文已核 |
| A | Sun et al., *TIDAL: Temporally Interleaved Diffusion and Action Loop for High-Frequency VLA Control*, 2026, arXiv:2601.14945 | 单步 flow integration 与 action execution 交错；采用 stale-intent compensation training 和 motion predictor | 原文已核 |
| A | Wu et al., *Closed-Loop Action Chunks with Dynamic Corrections for Training-Free Diffusion Policy* (DCDP), ICRA 2026, arXiv:2603.01953 | observation-history dynamic features 对冻结 Diffusion Policy chunk 作逐步修正 | 原文已核；额外 fast module/action VAE 需 Stage-1 training |
| C | *ProgressVLA: Progress-Guided Diffusion Policy for Vision-Language Robotic Manipulation*, 2026, arXiv:2603.27670 | world model + progress estimator 对 action tokens 的 differentiable guidance | 元数据已核；与 FBFM 共享 sampling-time guidance，但目标不同 |
| A | An et al., *Feedback World Model Enables Precise Guidance of Diffusion Policy*, 2026, arXiv:2605.15705 | observer-style latent feedback、单步预测修正和独立 diffusion-policy guidance | 原文与证明已核；收敛对象为 latent observer error |
| C | *FocalPolicy: Frequency-Optimized Chunking and Locally Anchored Flow Matching for Coherent Visuomotor Policy*, 2026, arXiv:2605.15944 | locally anchored FM 与 chunk coherence 的近期工作 | 元数据已核；需核查与 RTC/FBFM 的真实重叠 |
| C | *Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation*, 2026, arXiv:2604.23609 | tube-level reactive feedback；主要面向视觉触觉接触任务 | 元数据已核；视篇幅决定 |
| C | *Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA*, 2026, arXiv:2604.02965 | 执行期闭环 verification 的侧向近邻，不直接修改 Flow Matching | 元数据已核；需全文审阅 |
| A | Cai et al., *AHA-WAM*, 2026, arXiv:2606.09811 | latest-observation routing、低频 video context 与高频 action DiT 的异步 WAM 架构 | 原文已核；依赖 joint/offset training，部署时不显式 decode future frame |
| A | Hong et al., *Steering Robustness into World Action Models via Mechanistic Interpretability and Optimal Control*, 2026, arXiv:2607.14943 | training-free WAM steering 的最新直接近邻；activation directions 与 reduced-order WA-LQR | 原文已核；LingBot-VA steerability 与 architecture dependence 已审阅 |
| C | Agouzoul, *Understanding Asynchronous Inference Methods for Vision-Language-Action Models*, 2026, arXiv:2605.08168 | 统一比较 IT/TT-RTC、VLASH、A2C2 的 delay sensitivity、成本与实现边界 | 原文已核；仅作二级交叉证据 |
| B | Yuan et al., *Fast-WAM*, 2026 | 通过取消测试时未来生成解决延迟；与 FBFM 保留并校正未来生成形成互补 | 元数据已核；全文待精读 |
| B | Xiao et al., *Thinking While Moving: Deep Reinforcement Learning with Concurrent Control*, 2020 | 计算与物理执行并发的控制背景；不作为 FBFM 直接前驱 | RTC 原文已核 |
| B | Rawlings, Mayne, and Diehl, *Model Predictive Control: Theory, Computation, and Design*, 2017 | receding horizon、warm start 与并行 execution/planning 的经典背景 | RTC 原文已核 |

### 3.3 最近邻比较矩阵

| 方法 | 主要约束/反馈对象 | 反馈进入位置 | 时间机制 | 训练边界 |
|---|---|---|---|---|
| BID | action chunk | rejection/resampling | closed-loop resampling | 使用预训练 chunk policy |
| RTC | committed/overlapping actions | active flow 的 inpainting guidance | 当前 chunk 执行时生成下一 chunk | 对冻结 flow policy 的 inference-time 方法 |
| RA-DP | action queue + external guidance | denoising/action queue | 每个 denoising step 产出可执行动作 | guidance 可 training-free；queue model 需 mixed-noise training |
| A2C2 | latest observation + base action | learned per-step residual | chunk 执行期间逐步修正 | base policy 冻结；correction head 需训练 |
| VLASH | rolled-forward proprioceptive state | policy conditioning | inference-start state 对齐到 execution time | 需要 temporal-offset fine-tuning |
| DynaGuide | task objective via external dynamics model | diffusion denoising guidance | inference-time steering | base policy 可冻结，但需要外部 dynamics model |
| AsyncVLA | low-confidence action tokens | learned asynchronous FM refinement | 非均匀 token schedule | 需要 SFM/AFM unified training |
| Feedback World Model | one-step latent prediction residual | observer correction，再指导独立 diffusion policy | environment decision 之间更新 feedback state | 无在线参数更新；依赖 world model/observer 结构 |
| AHA-WAM | latest observation + reusable video context | context routing to action DiT | 低频 planner / 高频 executor | 专门架构与 horizon-offset training |
| WA-LQR | WAM internal activations | activation steering + reduced-order LQR | feedback optimal control | training-free，但要求可操纵的 activation dynamics |
| FBFM | time-aligned latent states + committed actions | active WAM Flow-Matching velocity | chunk 内新反馈在后续 solver evaluation 生效 | 冻结 WAM 上的 masked pseudoinverse guidance |

### 3.4 预期写作链

正文使用四个连续段落：第一段从 BID 收回两版 RTC 的技术伏笔，并以 Legato/PAINT
说明 action-continuity 分支；第二段比较 RA-DP、VLASH、A2C2/DCDP、AsyncVLA/TIDAL
在真实信息来源、执行时序与训练依赖上的差异；第三段转入 DynaGuide、Feedback World
Model、AHA-WAM 和 WA-LQR 的 dynamics/WAM feedback；第四段以统一 measurement
interface 定位 FBFM。完整证据与比较矩阵见 `Related_Works_Theme_3_Reading.md`。

## 4. 检索方向与查询词

后续检索不应只使用 `FBFM` 或 `world-action model`。建议保留以下查询组，并在投稿前进行最后一次时间窗口更新。

### 4.1 生成与逆问题

- `diffusion inverse problems pseudoinverse inpainting`
- `training-free inverse problems flow matching`
- `masked conditional flow matching inpainting`
- `posterior sampling rectified flow inverse problems`

### 4.2 World models 与 WAM

- `latent world model visual control imagination`
- `action-conditioned video world model robot manipulation`
- `world action model future imagination robot`
- `world action model feedback steering robustness`
- `stage-wise joint video action generation robot`

### 4.3 生成式机器人策略

- `diffusion policy action chunk robotics`
- `flow matching policy robot manipulation`
- `flow matching vision language action`
- `diffusion foundation model bimanual manipulation`
- `continuous generative policy action expert`

### 4.4 执行期反馈与异步推理

- `asynchronous action chunk flow matching`
- `real-time diffusion policy replanning feedback`
- `training-free diffusion policy guidance world model`
- `closed-loop action chunk correction`
- `WAM inference-time steering feedback`
- `interleaved denoising environment interaction robot`

## 5. 下一步精读顺序

1. **直接技术链**：ΠGDM → Pokle et al. → RTC。
2. **执行近邻**：BID → RA-DP → DynaGuide → AsyncVLA → TIDAL → DCDP。
3. **WAM 反馈近邻**：Feedback World Model → WA-LQR → Fast-WAM。
4. **WAM 架构实例**：LingBot-VA → DreamZero，再核对 GR-2/IRASim 作为历史过渡是否必要。
5. **政策发展链**：Diffuser → Diffusion Policy → RFMP → RDT-1B → \(\pi_0\)/\(\pi_0.5\)。

每次精读后需要补充：论文的明确 claim、关键机制、训练要求、反馈时序、实验对象、与 FBFM 的可比较维度，以及可安全写入正文的一句话。未完成这一步的 C 类文献不得用于强 novelty claim。
