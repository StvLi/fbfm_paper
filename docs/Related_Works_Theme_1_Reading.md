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
| 7 | Rombach et al., *High-Resolution Image Synthesis with Latent Diffusion Models*, 2022 | 在预训练 autoencoder 的 latent space 中运行 diffusion，并以 cross-attention 支持通用条件生成。 | 可补充 latent generation 背景，但不直接支持 FBFM 的反馈主张。 | Reserve |
| 8 | Lugmayr et al., *RePaint*, 2022 | 仅修改预训练 unconditional DDPM 的反向采样与 resampling schedule，实现无需 mask-specific training 的 inpainting。 | 说明迭代生成天然适合 inference-time mask conditioning。 | Grouped |
| 9 | Song et al., *Pseudoinverse-Guided Diffusion Models for Inverse Problems*, 2023 | 根据已知 measurement model 近似 conditional score，并通过 pseudoinverse residual 的 VJP 引导问题无关的 diffusion model。 | FBFM pseudoinverse guidance 的直接来源，必须单独说明。 | Core |
| 10 | Pokle et al., *Training-Free Linear Image Inverses via Flows*, 2024 | 将 ΠGDM correction 迁移到 pretrained flow vector field，并利用 conditional OT paths 求解线性 inverse problems。 | 从 diffusion pseudoinverse guidance 到 flow sampling 的直接桥梁。 | Core |
| 11 | Mardani et al., *A Variational Perspective on Solving Inverse Problems with Diffusion Models*, 2023 | 将 inverse-problem posterior sampling 写成 SNR 加权的 variational/regularization-by-denoising 优化。 | 表明 training-free inverse solving 还有 variational 路线；不是 FBFM 的直接来源。 | Reserve |
| 12 | Ha and Schmidhuber, *World Models*, 2018 | 用 VAE、MDN-RNN 和小型 controller 学习压缩视觉动态，并展示在 learned dream 中训练控制器。 | 经典 world-model 起点。 | Core |
| 13 | Hafner et al., *Learning Latent Dynamics for Planning from Pixels* (PlaNet), 2019 | 以 deterministic/stochastic recurrent latent dynamics 和 latent overshooting 支持 pixel-based online planning。 | 建立 latent dynamics 与视觉控制的直接联系。 | Core |
| 14 | Hafner et al., *Dream to Control* (Dreamer), 2020 | 通过 imagined latent trajectories 上的解析梯度训练 actor--critic，而非每步执行 online planning。 | 说明 imagined futures 可以直接用于策略学习。 | Core |
| 15 | Hafner et al., *Mastering Atari with Discrete World Models* (DreamerV2), 2021 | 使用 discrete latent world model 将 Dreamer 扩展到 Atari，并达到人类水平的综合表现。 | 支撑 Dreamer 路线的扩展；不单独展开。 | Grouped |
| 16 | Hafner et al., *Mastering Diverse Control Tasks through World Models* (DreamerV3), 2025; preprint 2023 | 通过归一化、平衡和鲁棒训练设计，以统一配置覆盖 150 余项不同任务。 | 支撑 world-model control 的跨域扩展；与 Dreamer 系列合并引用。 | Grouped |
| 17 | Hansen, Wang, and Su, *Temporal Difference Learning for Model Predictive Control* (TD-MPC), 2022 | 联合学习 task-oriented latent dynamics 与 terminal value，以短时域 MPC 兼顾局部规划和长期价值。 | 重要的 latent-control 分支，但依赖 reward/value，偏离本文问题设定。 | Reserve |
| 18 | Yang et al., *Learning Interactive Real-World Simulators* (UniSim), 2024 | 将异构图像、视频、导航与机器人数据统一为 action-in-video-out diffusion simulator，并用于策略训练。 | 从 latent control 过渡到 action-conditioned visual simulation。 | Core |
| 19 | Bruce et al., *Genie: Generative Interactive Environments*, 2024 | 从无动作标注视频中学习 latent actions 和 autoregressive dynamics，生成可逐帧交互的环境。 | 证明大规模视频模型可成为可交互 world model；与 UniSim 合并引用。 | Grouped |
| 20 | Zhu et al., *IRASim: A Fine-Grained World Model for Robot Manipulation*, 2024/2025 | 以 diffusion transformer 和 frame-level action conditioning 对齐机器人动作与生成视频，并用于 policy evaluation/planning。 | 连接 action-conditioned video prediction 与机器人应用。 | Core |
| 21 | Zhen et al., *3D-VLA*, 2024 | 将 3D LLM、interaction tokens 和目标图像/点云 diffusion generation 用于 3D reasoning 与 planning。 | 更接近 goal imagination，而非本文所需的执行期多步 WAM feedback。 | Reserve |
| 22 | Cheang et al., *GR-2*, 2024 | 先在 3800 万互联网视频上学习动态，再用机器人轨迹联合微调视频生成与动作预测。 | 作为 video pretraining 进入 video-action policy 的早期代表。 | Core |
| 23 | Li et al., *Causal World Modeling for Robot Control* (LingBot-VA), 2026 | 论文提出统一的 autoregressive video-action diffusion framework，并强调真实观测刷新、持续历史与异步执行。 | 论文用于说明统一 video-action modeling 的研究主张；发布代码中的 stage-wise inference 另作实现事实处理。 | Core |
| 24 | Ye et al., *World Action Models are Zero-shot Policies* (DreamZero), 2026 | 在 14B pretrained video diffusion backbone 中联合生成未来视频与动作，并实现实时闭环和跨 embodiment transfer。 | FBFM 的 joint-generation implementation carrier。 | Core |
| 25 | Yuan et al., *Fast-WAM*, 2026 | 通过控制实验分离 video co-training 与 test-time future generation，并在推理时跳过未来视频生成。 | 与 FBFM 构成互补定位：FBFM研究保留未来生成时如何在线重锚定。 | Core |

### 补充审阅项

检索过程中同时核对了 Chung et al., *Diffusion Posterior Sampling for General Noisy Inverse Problems* (DPS, 2023)。其主要贡献是用 posterior-score approximation 处理 noisy linear/nonlinear inverse problems。它适合作为 inverse-problem guidance 的背景引用，但 ΠGDM 和 Pokle 已足以建立 FBFM 的直接技术来源，因此当前列为 **Reserve**。

### LingBot-VA 论文与代码的事实边界

LingBot-VA 论文与其发布代码不能作为同一个架构事实来源：

- **论文主张**：论文将模型描述为统一的 autoregressive video-action framework，强调 interleaved representations、closed-loop observation refresh 和 asynchronous execution。
- **代码事实**：上游仓库 `Robbyant/lingbot-va` 的当前审阅 commit `7c6ffa9bfc4b83582cafc860fab4c82cc7deeeeb` 在 `wan_va/wan_va_server.py::_infer` 中先完整运行 `Video Generation Loop`，再运行独立的 action denoising loop；两者使用不同 scheduler 和 inference-step 配置。action pass 通过 `action_mode=True` 使用视频阶段写入的上下文/cache。
- **写作规则**：Related Works 只复述论文所提出的统一 video-action modeling 及其闭环目标；Method 将 stage-wise generation 作为一般化架构；Experiments 再明确本工作的 LingBot-VA 实例基于发布代码中的 frame-first/action-second inference。不得把代码的 stage-wise 顺序写成 LingBot-VA 论文的原始主张，也不得用论文的“统一生成”替代实际实验代码路径。

## 2. 筛选结论

### 2.1 建议进入正文的引用组

- **生成基础**：Sohl-Dickstein、DDPM、DDIM/score-SDE、Flow Matching、Rectified Flow；
- **Inference-time conditioning**：RePaint、ΠGDM、Pokle；
- **经典 world models**：World Models、PlaNet、Dreamer 系列；
- **视频到交互式 world model**：UniSim、Genie、IRASim；
- **机器人 video-action/WAM**：GR-2、LingBot-VA、DreamZero、Fast-WAM。

以上共约 20 篇，但通过合并引用只承担 11 个独立论点。LDM、RED-diff、TD-MPC、3D-VLA 和 DPS 暂不进入第一版正文。

### 2.2 论述顺序

本主题适合写成三个连续段落，而不在最终排版中暴露子标题：

1. **从 diffusion 到 Flow Matching**：只解释共同的 noise-to-data transport 和不同的训练/采样参数化；
2. **从 inpainting 到 pseudoinverse-guided flows**：建立 RePaint → ΠGDM → Pokle 的技术迁移；
3. **从 latent imagination 到 WAM**：World Models/PlaNet/Dreamer → UniSim/Genie/IRASim → GR-2/LingBot-VA/DreamZero/Fast-WAM。

第三段最后必须限定本文范围：FBFM不主张所有使用视频训练的 policy 都需要 test-time feedback；它只研究推理时仍显式生成 future-state stream 的 WAM。

## 3. English Working Draft v0.1

Diffusion models were initially developed as iterative generative processes that recover data by reversing a gradual corruption process [Sohl-Dickstein et al., 2015; Ho et al., 2020]. Subsequent formulations decoupled the learned denoiser from a particular stochastic sampler through non-Markovian diffusion and continuous-time score dynamics [Song et al., 2021a; Song et al., 2021b]. Flow Matching provides a closely related continuous generative view: instead of learning the reverse of a prescribed noising process, it trains a velocity field that transports a simple source distribution to the data distribution along a chosen probability path [Lipman et al., 2023]. Rectified Flow further favors increasingly straight transport trajectories that can be integrated accurately with fewer solver evaluations [Liu et al., 2023]. Thus, diffusion and Flow Matching use different training and path parameterizations, but both generate structured samples through an iterative transport from noise to data.

Their iterative sampling procedures also permit observations to be introduced at inference time. RePaint conditions an unconditional diffusion prior on known pixels by modifying only the reverse sampling schedule, without mask-specific training [Lugmayr et al., 2022]. More generally, Pseudoinverse-Guided Diffusion Models (ΠGDM) use a known measurement model and its pseudoinverse to approximate a conditional score, with a vector--Jacobian product propagating measurement residuals back to the current sample [Song et al., 2023]. Pokle et al. subsequently transfer this correction to pretrained flow models, adding measurement guidance directly to the velocity field while retaining a training-free linear inverse solver [Pokle et al., 2024]. This progression establishes the technical basis for using partial measurements to steer a frozen continuous generator during sampling.

World models shift the generated object from a static sample to the future of an acting agent. Early neural world models learned compact visual dynamics and used imagined rollouts for controller training or latent-space planning [Ha and Schmidhuber, 2018; Hafner et al., 2019]. Dreamer and its successors further optimized policies through trajectories imagined in learned latent dynamics and scaled this principle across increasingly diverse control domains [Hafner et al., 2020; Hafner et al., 2021; Hafner et al., 2025]. With the emergence of large video generators, UniSim and Genie reframed video prediction as an interactive, action-conditioned simulation problem, while IRASim introduced frame-level action conditioning for fine-grained robot--object dynamics [Yang et al., 2024; Bruce et al., 2024; Zhu et al., 2025]. Recent video-action policies and World-Action Models (WAMs) move one step further by coupling future visual generation with robot action prediction: GR-2 transfers Internet-video dynamics into joint video--action fine-tuning, LingBot-VA combines autoregressive video-action modeling with closed-loop observation refresh and asynchronous execution, and DreamZero jointly generates future video and actions from a pretrained video diffusion backbone [Cheang et al., 2024; Li et al., 2026; Ye et al., 2026]. Fast-WAM shows that video co-training can remain beneficial even when explicit future generation is removed at inference time [Yuan et al., 2026]. FBFM addresses the complementary setting in which such future-state generation is retained, and asks how the generated state stream can be re-grounded with observations arriving during execution.

## 4. 中文对照稿 v0.1

Diffusion 模型最初被提出为一种迭代式生成过程：它通过反转逐步破坏数据结构的过程，从噪声中恢复数据 [Sohl-Dickstein et al., 2015; Ho et al., 2020]。后续工作通过非马尔可夫扩散和连续时间 score dynamics，使训练得到的去噪器不再绑定于某一种随机采样器 [Song et al., 2021a; Song et al., 2021b]。Flow Matching 提供了与之紧密相关的连续生成视角：它不再学习某个预设加噪过程的反过程，而是学习一个速度场，使简单源分布沿选定的概率路径输运至数据分布 [Lipman et al., 2023]。Rectified Flow 则进一步倾向于逐渐拉直输运轨迹，使其能够用更少的求解器调用得到准确积分 [Liu et al., 2023]。因此，Diffusion 与 Flow Matching 虽然使用不同的训练方式和路径参数化，但二者都通过从噪声到数据的迭代输运生成结构化样本。

这类迭代采样过程也允许在推理时引入观测。RePaint 仅修改反向采样调度，便可以使无条件 diffusion prior 服从已知像素，而无需针对特定 mask 重新训练 [Lugmayr et al., 2022]。更一般地，Pseudoinverse-Guided Diffusion Models（ΠGDM）利用已知 measurement model 及其伪逆近似 conditional score，并通过 vector--Jacobian product 将测量残差反向传播到当前样本 [Song et al., 2023]。随后，Pokle 等人将这一 correction 迁移到预训练 flow model，把 measurement guidance 直接加入 velocity field，同时保持线性逆问题求解过程无需重新训练 [Pokle et al., 2024]。这条技术发展路线为在采样过程中使用部分测量引导冻结的连续生成器奠定了基础。

World model 将生成对象从静态样本转向行动主体的未来。早期神经 world model 学习紧凑的视觉动态，并利用想象 rollout 训练控制器或在 latent space 中进行规划 [Ha and Schmidhuber, 2018; Hafner et al., 2019]。Dreamer 及其后续工作进一步通过 learned latent dynamics 中想象出的轨迹优化策略，并将这一思路扩展到越来越多样的控制领域 [Hafner et al., 2020; Hafner et al., 2021; Hafner et al., 2025]。随着大规模视频生成器出现，UniSim 和 Genie 将视频预测重新表述为可交互、由动作控制的仿真问题；IRASim 则引入 frame-level action conditioning，以刻画细粒度的机器人与物体动态 [Yang et al., 2024; Bruce et al., 2024; Zhu et al., 2025]。近期的 video-action policy 和 World-Action Model（WAM）进一步把未来视觉生成与机器人动作预测结合起来：GR-2 将互联网视频中的动态知识迁移到 video--action 联合微调，LingBot-VA 将 autoregressive video-action modeling 与真实观测刷新和异步执行结合，而 DreamZero 则基于预训练 video diffusion backbone 联合生成未来视频与动作 [Cheang et al., 2024; Li et al., 2026; Ye et al., 2026]。Fast-WAM 表明，即使在推理时取消显式未来生成，video co-training 仍可能带来收益 [Yuan et al., 2026]。FBFM 研究的是与之互补的情形：当未来状态生成在推理时被保留，如何使用执行期间到达的观测持续重锚定这一生成中的状态流。
