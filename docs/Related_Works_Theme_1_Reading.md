# Related Works Theme 1: Generative Modeling and World Models

本文档记录第一主题的结构化精读、精度筛选和工作正文。阅读范围包括每篇论文的摘要、Introduction、方法框架、核心实验结论与 Conclusion；只有直接前驱和近邻工作进一步核对到关键公式或生成接口。表中的“主要贡献”均尽量复述论文自身主张，不代表 FBFM 对其作出的价值判断。

筛选标记：

- **Core**：本主题的论证不可缺少，预计进入最终正文；
- **Grouped**：适合与同方向文献合并引用，不单独展开；
- **Reserve**：已读，但当前正文不需要；仅在篇幅、审稿意见或论证缺口出现时启用。

## 1. 精读与筛选表

| # | 文献 | 主要贡献（简短） | 在 FBFM 论述中的作用 | 筛选 |
|---:|---|---|---|---|
| 1 | Sohl-Dickstein et al., *Deep Unsupervised Learning using Nonequilibrium Thermodynamics*, 2015 | 以逐步破坏数据结构的前向扩散和学习得到的反向过程构造生成模型。 | diffusion 的历史起点；与 DDPM 合并引用即可。 | Grouped |
| 2 | Ho et al., *Denoising Diffusion Probabilistic Models*, 2020 | 通过加权变分目标和噪声预测参数化，使 diffusion model 获得高质量图像生成能力。 | 建立现代 iterative denoising 生成范式。 | Core |
| 3 | Song, Meng, and Ermon, *Denoising Diffusion Implicit Models*, 2021 | 在不改变 DDPM 训练目标的情况下引入非马尔可夫、可确定性的更短采样过程。 | 说明训练目标与具体采样轨迹可以解耦。 | Grouped |
| 4 | Song et al., *Score-Based Generative Modeling through Stochastic Differential Equations*, 2021 | 用连续时间 SDE 统一 score-based 与 diffusion models，并给出 reverse SDE 和 probability-flow ODE。 | 连接 stochastic diffusion、deterministic ODE 与 inverse-problem conditioning。 | Grouped |
| 5 | Lipman et al., *Flow Matching for Generative Modeling*, 2023 | 提出无需模拟轨迹的 Flow-Matching/Conditional-Flow-Matching 目标来训练 CNF，并容纳 diffusion 与 OT probability paths。 | Flow Matching 的直接基础引用。 | Core |
| 6 | Liu, Gong, and Liu, *Flow Straight and Fast*, 2022/2023 | 通过 rectification 学习尽量笔直的 ODE transport paths，并用 reflow 降低粗步长求解误差。 | 说明直线路径与较低采样成本的 Flow-Matching 发展方向。 | Grouped |
| 7 | Rombach et al., *High-Resolution Image Synthesis with Latent Diffusion Models*, 2022 | 在预训练 autoencoder 的 latent space 中运行 diffusion，并以 cross-attention 支持通用条件生成。 | 连接 pixel-space generation 与 FBFM 所依赖的 latent generative space。 | Grouped |
| 8 | Lugmayr et al., *RePaint*, 2022 | 仅修改预训练 unconditional DDPM 的反向采样与 resampling schedule，实现无需 mask-specific training 的 inpainting。 | 说明迭代生成天然适合 inference-time mask conditioning。 | Grouped |
| 9 | Song et al., *Pseudoinverse-Guided Diffusion Models for Inverse Problems*, 2023 | 根据已知 measurement model 近似 conditional score，并通过 pseudoinverse residual 的 VJP 引导问题无关的 diffusion model。 | FBFM pseudoinverse guidance 的直接来源，必须单独说明。 | Core |
| 10 | Pokle et al., *Training-Free Linear Image Inverses via Flows*, 2024 | 将 ΠGDM correction 迁移到 pretrained flow vector field，并利用 conditional OT paths 求解线性 inverse problems。 | 从 diffusion pseudoinverse guidance 到 flow sampling 的直接桥梁。 | Core |
| 11 | Mardani et al., *A Variational Perspective on Solving Inverse Problems with Diffusion Models*, 2023 | 将 inverse-problem posterior sampling 写成 SNR 加权的 variational/regularization-by-denoising 优化。 | 表明 training-free inverse solving 还有 variational 路线；不是 FBFM 的直接来源。 | Reserve |
| 12 | Ha and Schmidhuber, *World Models*, 2018 | 用 VAE、MDN-RNN 和小型 controller 学习压缩视觉动态，并展示在 learned dream 中训练控制器。 | 经典 world-model 起点。 | Core |
| 13 | Hafner et al., *Learning Latent Dynamics for Planning from Pixels* (PlaNet), 2019 | 以 deterministic/stochastic recurrent latent dynamics 和 latent overshooting 支持 pixel-based online planning。 | 建立 latent dynamics 与视觉控制的直接联系。 | Core |
| 14 | Hafner et al., *Dream to Control* (Dreamer), 2020 | 通过 imagined latent trajectories 上的解析梯度训练 actor--critic，而非每步执行 online planning。 | 说明 imagined futures 可以直接用于策略学习。 | Core |
| 15 | Hafner et al., *Mastering Atari with Discrete World Models* (DreamerV2), 2021 | 使用 discrete latent world model 将 Dreamer 扩展到 Atari，并达到人类水平的综合表现。 | 支撑 Dreamer 路线的扩展；不单独展开。 | Grouped |
| 16 | Hafner et al., *Mastering Diverse Control Tasks through World Models* (DreamerV3), 2025; preprint 2023 | 通过归一化、平衡和鲁棒训练设计，以统一配置覆盖 150 余项不同任务。 | 支撑 world-model control 的跨域扩展；与 Dreamer 系列合并引用。 | Grouped |
| 17 | Hansen, Wang, and Su, *Temporal Difference Learning for Model Predictive Control* (TD-MPC), 2022 | 联合学习 task-oriented latent dynamics 与 terminal value，以短时域 MPC 兼顾局部规划和长期价值。 | 说明 world-model latent 可由控制目标塑形，而不必承担 observation reconstruction。 | Grouped |
| 18 | Yang et al., *Learning Interactive Real-World Simulators* (UniSim), 2024 | 将异构图像、视频、导航与机器人数据统一为 action-in-video-out diffusion simulator，并用于策略训练。 | 从 latent control 过渡到 action-conditioned visual simulation。 | Core |
| 19 | Bruce et al., *Genie: Generative Interactive Environments*, 2024 | 从无动作标注视频中学习 latent actions 和 autoregressive dynamics，生成可逐帧交互的环境。 | 证明大规模视频模型可成为可交互 world model；与 UniSim 合并引用。 | Grouped |
| 20 | Zhu et al., *IRASim: A Fine-Grained World Model for Robot Manipulation*, 2024/2025 | 以 diffusion transformer 和 frame-level action conditioning 对齐机器人动作与生成视频，并用于 policy evaluation/planning。 | 连接 action-conditioned video prediction 与机器人应用。 | Core |
| 21 | Zhen et al., *3D-VLA*, 2024 | 将 3D LLM、interaction tokens 和目标图像/点云 diffusion generation 用于 3D reasoning 与 planning。 | 更接近 goal imagination，而非本文所需的执行期多步 WAM feedback。 | Reserve |
| 22 | Cheang et al., *GR-2*, 2024 | 先在 3800 万互联网视频上学习动态，再用机器人轨迹联合微调视频生成与动作预测。 | 作为 video pretraining 进入 video-action policy 的早期代表。 | Core |
| 23 | Li et al., *Causal World Modeling for Robot Control* (LingBot-VA), 2026 | 论文提出统一的 autoregressive video-action diffusion framework，并强调真实观测刷新、持续历史与异步执行。 | 论文用于说明统一 video-action modeling 的研究主张；发布代码中的 stage-wise inference 另作实现事实处理。 | Core |
| 24 | Ye et al., *World Action Models are Zero-shot Policies* (DreamZero), 2026 | 在 14B pretrained video diffusion backbone 中联合生成未来视频与动作，并实现实时闭环和跨 embodiment transfer。 | FBFM 的 joint-generation implementation carrier。 | Core |
| 25 | Yuan et al., *Fast-WAM*, 2026 | 通过控制实验分离 video co-training 与 test-time future generation，并在推理时跳过未来视频生成。 | 与 FBFM 构成互补定位：FBFM研究保留未来生成时如何在线重锚定。 | Core |
| 26 | Kaiser et al., *Model-Based Reinforcement Learning for Atari* (SimPLe), 2020 | 学习 pixel-space video predictor，并在生成的短 rollout 中训练策略。 | 与 latent world models 对照，说明显式视觉预测也是 imagined control 的早期接口。 | Grouped |
| 27 | Schrittwieser et al., *Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model* (MuZero), 2020 | 学习仅预测 reward、value 和 policy 等 planning-relevant quantities 的隐式动力学，而不重建 observation。 | 支撑 latent representation 从重建导向转向 task-oriented abstraction。 | Grouped |
| 28 | Voleti et al., *MCVD*, 2022 | 以 masked conditional video diffusion 统一视频预测、生成和插值。 | 建立 diffusion 从静态图像生成进入显式未来视频建模的桥梁。 | Grouped |
| 29 | Alonso et al., *Diffusion for World Modeling: Visual Details Matter in Atari* (DIAMOND), 2024 | 将 diffusion model 用作可交互环境动力学，并在其生成 rollout 中训练 agent。 | 直接展示 diffusion visual generation 与 world-model control 的汇合。 | Core |
| 30 | Wu et al., *GR-1*, 2023 | 通过大规模视频生成预训练，端到端预测未来图像与机器人动作。 | 从 video pretraining 过渡到联合 future-image/action robot model。 | Grouped |

### 补充审阅项

检索过程中同时核对了 Chung et al., *Diffusion Posterior Sampling for General Noisy Inverse Problems* (DPS, 2023)。其主要贡献是用 posterior-score approximation 处理 noisy linear/nonlinear inverse problems。它适合作为 inverse-problem guidance 的背景引用，但当前段落以 RePaint 建立 inpainting 背景，并以 ΠGDM 和 Pokle 建立 FBFM 的直接技术来源，因此 DPS 仍列为 **Reserve**。

### LingBot-VA 论文与代码的事实边界

LingBot-VA 论文与其发布代码不能作为同一个架构事实来源：

- **论文主张**：论文将模型描述为统一的 autoregressive video-action framework，强调 interleaved representations、closed-loop observation refresh 和 asynchronous execution。
- **代码事实**：上游仓库 `Robbyant/lingbot-va` 的当前审阅 commit `7c6ffa9bfc4b83582cafc860fab4c82cc7deeeeb` 在 `wan_va/wan_va_server.py::_infer` 中先完整运行 `Video Generation Loop`，再运行独立的 action denoising loop；两者使用不同 scheduler 和 inference-step 配置。action pass 通过 `action_mode=True` 使用视频阶段写入的上下文/cache。
- **写作规则**：Related Works 只复述论文所提出的统一 video-action modeling 及其闭环目标；Method 将 stage-wise generation 作为一般化架构；Experiments 再明确本工作的 LingBot-VA 实例基于发布代码中的 frame-first/action-second inference。不得把代码的 stage-wise 顺序写成 LingBot-VA 论文的原始主张，也不得用论文的“统一生成”替代实际实验代码路径。

## 2. 筛选结论

### 2.1 建议进入正文的引用组

- **生成基础**：Sohl-Dickstein、DDPM、DDIM/score-SDE、Latent Diffusion、Flow Matching、Rectified Flow；
- **Inference-time conditioning**：RePaint、ΠGDM、Pokle；
- **潜空间动力学与 imagined control**：World Models、SimPLe、PlaNet、Dreamer 系列、MuZero、TD-MPC；
- **生成视频到交互式 world model**：MCVD、UniSim、Genie、DIAMOND、IRASim；
- **机器人 video-action/WAM**：GR-1、GR-2、LingBot-VA、DreamZero、Fast-WAM。

最终正文保留 28 篇文献，但不以篇数作为筛选目标。新增文献只用于补齐 latent representation 的发展，以及 diffusion/video generation 与 classical world models 汇合到 WAM 的桥梁。RED-Diff、3D-VLA 和 DPS 仍保留为备用，不为扩大引用规模而写入正文。

### 2.2 论述顺序

本主题适合写成四个连续段落，而不在最终排版中暴露子标题：

1. **从 diffusion 到 latent/flow generation**：解释共同的 noise-to-data transport、latent generation 和不同的训练/采样参数化；
2. **从 inpainting 到 pseudoinverse-guided flows**：建立 RePaint → ΠGDM → Pokle 的技术迁移；
3. **latent dynamics and imagined control**：从 reconstructive continuous latent，经过 stochastic/discrete latent，发展到 planning-oriented 或 decoder-free latent；
4. **两条路线在 WAM 汇合**：MCVD/UniSim/Genie/DIAMOND/IRASim 提供显式视觉未来，GR-1/GR-2/LingBot-VA/DreamZero 将其与 action prediction 结合。

第四段最后必须限定本文范围：FBFM不主张所有使用视频训练的 policy 都需要 test-time feedback；它只研究推理时仍显式生成 future-state stream 的 WAM。

## 3. English Expanded Draft v0.2

以下版本保留逐步论证，作为文献审阅和引用追溯底稿。最终主文已在不改变四段结构的
前提下压缩为更高层次的 grouped-citation 版本，以
`docs/Chapters/6_Related_Works.md` 为准。

Diffusion models were initially developed as iterative generative processes that recover data by reversing a gradual corruption process [Sohl-Dickstein et al., 2015; Ho et al., 2020]. DDIM and the score-SDE formulation subsequently decoupled the learned denoiser or score from a single stochastic sampler and connected diffusion to continuous-time probability dynamics [Song et al., 2021a; Song et al., 2021b]. Latent diffusion moved this iterative process from pixels into a learned perceptual space, making high-dimensional conditional generation more tractable [Rombach et al., 2022]. Flow Matching provides a related continuous generative view by learning a velocity field along a chosen probability path, while Rectified Flow favors straighter transport trajectories that tolerate coarser numerical integration [Lipman et al., 2023; Liu et al., 2023]. Although these formulations use different objectives and path parameterizations, they all generate structured samples through an iterative transport from a simple source distribution to data.

The iterative sampling interface also permits partial observations to constrain generation at inference time. RePaint injects known pixels by modifying the reverse diffusion schedule without mask-specific training [Lugmayr et al., 2022]. More generally, Pseudoinverse-Guided Diffusion Models (ΠGDM) use a known measurement map and its pseudoinverse to approximate a conditional score, then propagate the lifted measurement residual through the denoiser with a vector--Jacobian product [Song et al., 2023]. This construction replaces a task-specific conditional generator with a measurement correction applied to a frozen generative prior. Pokle et al. transfer the same principle to pretrained continuous flows by correcting the velocity field during sampling, again without retraining the generator [Pokle et al., 2024]. These two works provide the direct generative mechanism that FBFM adapts from static inverse problems to time-aligned state and action coordinates.

Classical world models developed along a distinct but complementary line based on latent dynamics and imagined control, rather than diffusion or Flow Matching. World Models compressed images with a VAE and evolved the resulting latent through a recurrent mixture-density model, while SimPLe learned a video predictor for model-based rollouts [Ha and Schmidhuber, 2018; Kaiser et al., 2020]. PlaNet's recurrent state-space model combined deterministic memory with stochastic latent states for online planning, and Dreamer optimized a policy through trajectories imagined in that latent dynamics model [Hafner et al., 2019; Hafner et al., 2020]. Subsequent work diversified what the representation should preserve: DreamerV2 used discrete stochastic states; MuZero learned dynamics that predict planning-relevant quantities without reconstructing observations; and TD-MPC learned a task-oriented, decoder-free latent for short-horizon trajectory optimization [Hafner et al., 2021; Schrittwieser et al., 2020; Hansen et al., 2022]. DreamerV3 further demonstrated that latent imagination can scale across diverse control domains [Hafner et al., 2025]. This progression establishes the latent state as an interface among perception, predicted dynamics, and control. FBFM accordingly introduces real observations through the WAM's encoded state space, rather than requiring feedback to act directly on raw pixels.

In parallel, generative video models made explicit visual futures increasingly controllable. MCVD used conditional diffusion for video prediction and generation, UniSim formulated an action-in-video-out diffusion simulator, and Genie learned latent actions for interactive environment generation [Voleti et al., 2022; Yang et al., 2024; Bruce et al., 2024]. DIAMOND further placed a diffusion model inside an agent's learned environment, while IRASim introduced frame-level action conditioning for fine-grained robot--object dynamics [Alonso et al., 2024; Zhu et al., 2025]. World-Action Models arise where this explicit visual-generation line meets latent dynamics and action prediction: GR-1 and GR-2 transfer video pretraining into future-image and robot-action prediction, LingBot-VA formulates autoregressive video--action modeling with closed-loop observation refresh, and DreamZero jointly generates future video and actions from a pretrained video diffusion backbone [Wu et al., 2023; Cheang et al., 2024; Li et al., 2026; Ye et al., 2026]. Fast-WAM shows that video co-training can remain useful even when explicit future generation is removed at inference time [Yuan et al., 2026]. FBFM addresses the complementary regime in which future-state generation is retained and asks how its latent state stream can be re-grounded by observations arriving during execution.

## 4. 中文扩展对照稿 v0.2

Diffusion 模型最初被提出为一种迭代生成过程：通过反转逐步破坏数据结构的过程，从噪声中恢复数据 [Sohl-Dickstein et al., 2015; Ho et al., 2020]。DDIM 与 score-SDE 表述进一步使训练得到的 denoiser 或 score 不再绑定于单一随机采样器，并将 diffusion 与连续时间概率动力学联系起来 [Song et al., 2021a; Song et al., 2021b]。Latent Diffusion 将这一迭代过程从像素空间迁移到学习得到的感知潜空间，使高维条件生成更易处理 [Rombach et al., 2022]。Flow Matching 则提供了相关的连续生成视角：它沿指定的概率路径学习速度场；Rectified Flow 进一步倾向于更笔直的输运轨迹，使数值积分能够采用更粗的步长 [Lipman et al., 2023; Liu et al., 2023]。尽管这些方法的训练目标和路径参数化不同，它们都通过从简单源分布到数据的迭代输运来生成结构化样本。

这一迭代采样接口也允许部分观测在推理时约束生成过程。RePaint 通过修改反向 diffusion 调度注入已知像素，而不需要针对特定 mask 重新训练 [Lugmayr et al., 2022]。更一般地，Pseudoinverse-Guided Diffusion Models（ΠGDM）使用已知测量映射及其伪逆来近似 conditional score，再通过 vector--Jacobian product 将提升后的测量残差传播回 denoiser [Song et al., 2023]。这一构造用施加在冻结生成先验上的测量校正，替代了针对具体任务训练的条件生成器。Pokle 等人随后将相同原理迁移到预训练连续流，在采样过程中直接校正速度场，同样无需重新训练生成器 [Pokle et al., 2024]。这两项工作构成 FBFM 的直接生成机制来源；FBFM 将其从静态逆问题迁移到时间对齐的状态与动作坐标。

经典 world model 沿着另一条互补路线发展，其核心是 latent dynamics 与 imagined control，而非 Diffusion 或 Flow Matching。World Models 使用 VAE 压缩图像，并通过 recurrent mixture-density model 推演所得 latent；SimPLe 则学习视频预测器以产生 model-based rollout [Ha and Schmidhuber, 2018; Kaiser et al., 2020]。PlaNet 的 recurrent state-space model 将确定性记忆与随机 latent state 结合用于在线规划，Dreamer 则通过 latent dynamics 中想象出的轨迹优化策略 [Hafner et al., 2019; Hafner et al., 2020]。后续工作进一步改变了 latent representation 需要保留的内容：DreamerV2 使用离散随机状态；MuZero 不重建 observation，而是学习预测与规划直接相关的信息；TD-MPC 则学习面向任务、无需 decoder 的 latent，用于短时域轨迹优化 [Hafner et al., 2021; Schrittwieser et al., 2020; Hansen et al., 2022]。DreamerV3 进一步证明 latent imagination 可以扩展到多样的控制领域 [Hafner et al., 2025]。这条发展路线确立了 latent state 作为感知、预测动力学与控制之间的接口。因此，FBFM 选择通过 WAM 的编码状态空间引入真实观测，而不要求反馈直接作用于原始像素。

与此同时，生成式视频模型使显式视觉未来变得越来越可控。MCVD 使用 conditional diffusion 进行视频预测与生成；UniSim 将模型构造成 action-in-video-out 的 diffusion simulator；Genie 则学习 latent action 以生成可交互环境 [Voleti et al., 2022; Yang et al., 2024; Bruce et al., 2024]。DIAMOND 进一步将 diffusion model 直接放入 agent 的 learned environment 中，IRASim 则为细粒度机器人与物体动力学引入 frame-level action conditioning [Alonso et al., 2024; Zhu et al., 2025]。当这条显式视觉生成路线与 latent dynamics、action prediction 汇合时，World-Action Model 开始形成：GR-1 与 GR-2 将视频预训练迁移到未来图像和机器人动作预测；LingBot-VA 在论文中提出带闭环观测刷新的 autoregressive video-action modeling；DreamZero 则基于预训练 video diffusion backbone 联合生成未来视频与动作 [Wu et al., 2023; Cheang et al., 2024; Li et al., 2026; Ye et al., 2026]。Fast-WAM 表明，即使推理时移除显式未来生成，video co-training 仍然可能有效 [Yuan et al., 2026]。FBFM 研究的是互补情形：当 future-state generation 被保留时，如何使用执行期间到达的观测持续重锚定其 latent state stream。
