# Related Works Theme 2: Diffusion and Flow-Matching Robot Policies

本文档记录第二主题的文献定位、筛选结论与中英文工作稿。本主题关注生成模型如何从轨迹规划进入机器人 action chunk，再发展为大规模 Diffusion/Flow-Matching policy。文献数量服从论述需要；经典背景工作合并引用，\(\pi_0\) 等关键路线节点单独分析。

## 1. 精读与筛选表

| # | 文献 | 主要贡献（简短） | 在 FBFM 论述中的作用 | 筛选 |
|---:|---|---|---|---|
| 1 | Janner et al., *Planning with Diffusion for Flexible Behavior Synthesis* (Diffuser), 2022 | 将完整 state-action trajectory 建模为 diffusion sample，并将 guidance 与 inpainting 用作规划约束。 | diffusion 从视觉生成进入 sequential decision-making 的起点。 | Core |
| 2 | Ajay et al., *Is Conditional Generative Modeling All You Need for Decision-Making?* (Decision Diffuser), 2023 | 将 offline decision-making 表述为 return、constraint 或 skill 条件下的轨迹生成。 | 说明条件生成可以直接承担决策接口。 | Grouped |
| 3 | Zhao et al., *Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware* (ACT), 2023 | 用 Transformer 生成 temporally correlated action chunks，降低逐步预测误差并支持精细双臂任务。 | action chunking 的代表性基础；不是 diffusion 方法。 | Grouped |
| 4 | Chi et al., *Diffusion Policy*, 2023 | 将 visuomotor policy 表述为 observation-conditioned action-horizon diffusion，并结合 receding-horizon execution。 | diffusion action chunk policy 的核心工作。 | Core |
| 5 | Ze et al., *3D Diffusion Policy* (DP3), 2024 | 将紧凑 point-cloud representation 引入 Diffusion Policy，提高少样本与空间泛化。 | 展示 diffusion policy 对感知模态和场景泛化的扩展。 | Grouped |
| 6 | Liu et al., *RDT-1B*, 2025 | 将 diffusion action model 扩展到 1.2B 参数、多机器人数据与统一动作空间。 | 支撑 diffusion policy 的模型、数据和 embodiment 规模增长。 | Core |
| 7 | Brohan et al., *RT-1*, 2023 | 以大规模真实机器人数据训练 Transformer policy，并系统研究数据与模型规模。 | generalist robot policy 的数据扩展背景。 | Grouped |
| 8 | Brohan et al., *RT-2*, 2023 | 将 robot actions 表示为 token，与 Internet vision-language tasks 共同微调 VLM。 | Internet semantic knowledge 进入 direct-action VLA 的代表。 | Grouped |
| 9 | Octo Model Team et al., *Octo*, 2024 | 在 Open X-Embodiment 上训练可适配新 observation/action space 的开源 generalist policy。 | cross-embodiment pretraining 与 action-chunk readout 背景。 | Grouped |
| 10 | Kim et al., *OpenVLA*, 2024 | 开源 7B VLA，并系统研究跨任务微调与部署效率。 | 大规模 autoregressive/direct-action VLA 的代表。 | Grouped |
| 11 | Braun et al., *Riemannian Flow Matching Policy*, 2024 | 将 Flow Matching policy 定义在机器人状态的 Riemannian manifold 上，生成平滑多模态轨迹。 | 说明 Flow Matching 在专用机器人运动策略中的早期探索与技术广度。 | Core |
| 12 | Rouxel et al., *Flow Matching Imitation Learning for Multi-Support Manipulation*, 2024 | 用 Flow Matching 学习多模态 whole-body trajectory，并与 multi-contact controller 结合。 | 展示 Flow Matching 在 whole-body/contact-rich imitation 中的独立发展。 | Grouped |
| 13 | Zhang and Gienger, *Affordance-based Robot Manipulation with Flow Matching*, 2025 | 以视觉 affordance 条件引导随机 waypoint 到动作轨迹的 flow。 | 展示 Flow Matching 与 task-conditioned visuomotor action generation 的结合。 | Grouped |
| 14 | Ding et al., *Fast and Robust Visuomotor Riemannian Flow Matching Policy*, 2025 | 以稳定性约束扩展 RFMP，并在欧氏与 Riemannian action spaces 上评估。 | 后续几何与稳定性扩展；当前正文无需单独展开。 | Reserve |
| 15 | Zhang et al., *FlowPolicy*, 2024 | 用 consistency flow matching 逼近单步 3D action generation。 | Flow policy 的采样加速分支；与本主题主线重复。 | Reserve |
| 16 | Black et al., *\(\pi_0\)*, 2024 | 在预训练 VLM 旁加入较小的 Flow-Matching action expert，生成连续高频 action chunks，并采用跨 embodiment 预训练与 post-training。 | Flow Matching 与大规模通用 VLA 汇合的关键节点。 | Core |
| 17 | Physical Intelligence et al., *\(\pi_{0.5}\)*, 2025 | 通过异构数据 co-training 和 semantic subtask prediction 扩展到开放世界长时域操作。 | 说明 \(\pi\) 系列持续沿用并扩展 Flow-Matching VLA 路线。 | Core |
| 18 | Black et al., *Real-Time Execution of Action Chunking Flow Policies*, 2025 | 通过伪逆引导的 inference-time inpainting，使冻结的 Flow-Matching policy 以已承诺 action prefix 约束新 chunk。 | 说明 \(\pi\) 系列的 Flow-Matching action interface 如何进一步支持 training-free asynchronous execution。 | Core |
| 19 | Black et al., *Training-Time Action Conditioning for Efficient Real-Time Chunking*, 2025 | 在训练中模拟 inference delay，并直接学习 prefix-conditioned postfix generation，以消除推理期 VJP 开销。 | 补全 RTC 的训练期分支，并与 training-free RTC 形成清晰边界。 | Core |

## 2. 筛选与论述顺序

正文使用三段，但不暴露小标题：

1. **trajectory generation → action chunk generation**：Diffuser/Decision Diffuser → ACT/Diffusion Policy → DP3/RDT-1B；
2. **generalist policy scaling**：RT-1/RT-2/Octo/OpenVLA 只用于说明数据、cross-embodiment 和 VLM 预训练背景，不展开架构细节；
3. **specialized robot Flow Matching → \(\pi\) series → RTC**：RFMP/multi-support/affordance-conditioned flows 补全专用机器人运动策略的发展背景；随后重点说明 \(\pi_0\) 和 \(\pi_{0.5}\) 如何将这条路线扩展为受到广泛认可的大规模通用 VLA。段末指出其 iterative velocity-field interface 使 action prefix 能够在生成过程中约束新 chunk，并以两版 RTC 为下一主题埋下伏笔，但暂不展开算法比较。

Stable RFMP 和 FlowPolicy 暂列备用。它们可在需要补充几何稳定性或 sampling acceleration 时启用，但当前不承担不可替代的论点。

## 3. English Working Draft v0.1

Diffusion-based decision methods treat decisions as structured samples rather than pointwise regressions. Diffuser denoises complete state-action trajectories and reinterprets guidance and inpainting as planning constraints, while Decision Diffuser casts offline decision-making as return-, constraint-, or skill-conditioned generation [Janner et al., 2022; Ajay et al., 2023]. In visuomotor imitation learning, ACT modeled temporally correlated action chunks through a generative sequence model, and Diffusion Policy directly modeled an observation-conditioned action horizon with iterative denoising and receding-horizon execution [Zhao et al., 2023; Chi et al., 2023]. DP3 extended this formulation with compact 3D observations, whereas RDT-1B scaled a diffusion Transformer to multi-robot pretraining, a unified action representation, and billion-parameter capacity [Ze et al., 2024; Liu et al., 2025]. Together, these works established chunk-level generative modeling as a scalable interface for multimodal continuous robot actions.

In parallel, RT-1, RT-2, Octo, and OpenVLA demonstrated that robot policies benefit from larger and more diverse datasets, cross-embodiment training, and pretrained vision-language representations, while adopting different action readouts [Brohan et al., 2023a; Brohan et al., 2023b; Octo Model Team et al., 2024; Kim et al., 2024]. RT-2 and OpenVLA, in particular, express actions through discrete tokens so that robot trajectories can share an autoregressive interface with language. This scaling trajectory motivates continuous generative action heads that retain the semantic priors of a VLM without reducing high-frequency, multimodal action chunks to a point estimate or a long sequence of discretized outputs.

Flow Matching developed into a robot action generator across both specialized motion policies and generalist VLA models. RFMP transported robot motions on Riemannian state spaces, while related work applied Flow Matching to multi-support whole-body imitation and affordance-conditioned manipulation [Braun et al., 2024; Rouxel et al., 2024; Zhang and Gienger, 2025]. This technical route gained much broader visibility through \(\pi_0\), which brought Flow Matching into a large-scale generalist VLA by pairing a pretrained VLM backbone with a smaller robotics-specific action expert and combining cross-embodiment pretraining with post-training. Its strong performance on high-frequency dexterous manipulation helped establish Flow Matching as a practical and scalable route for continuous robot action generation [Black et al., 2024]. \(\pi_{0.5}\) retained this action-generation design while adding heterogeneous co-training and semantic subtask prediction for open-world, long-horizon manipulation [Physical Intelligence et al., 2025]. Beyond predictive performance, this conditional Flow-Matching action expert exposes an iterative velocity-field interface through which an action prefix can constrain a chunk as it is generated. The two RTC formulations exploit this interface through training-free pseudoinverse-guided inpainting and training-time action-prefix conditioning, respectively [Black et al., 2025a; Black et al., 2025b]. This connection motivates the following discussion of asynchronous execution and feedback.

## 4. 中文对照稿 v0.1

Diffusion-based decision methods 将决策视为结构化样本，而不是逐点回归结果。Diffuser 对完整 state-action trajectory 进行去噪，并把 guidance 与 inpainting 重新解释为规划约束；Decision Diffuser 则将 offline decision-making 表述为以 return、constraint 或 skill 为条件的生成问题 [Janner et al., 2022; Ajay et al., 2023]。在 visuomotor imitation learning 中，ACT 使用生成式序列模型建模具有时间相关性的 action chunk，Diffusion Policy 则直接使用迭代去噪建模 observation-conditioned action horizon，并采用 receding-horizon execution [Zhao et al., 2023; Chi et al., 2023]。DP3 使用紧凑 3D observation 扩展这一表述，RDT-1B 则将 diffusion Transformer 扩展到多机器人预训练、统一动作表征和十亿参数规模 [Ze et al., 2024; Liu et al., 2025]。这些工作共同确立了 chunk-level generative modeling 作为多模态连续机器人动作的可扩展接口。

与此同时，RT-1、RT-2、Octo 和 OpenVLA 证明了机器人策略可以受益于更大、更多样的数据，cross-embodiment training 和预训练 vision-language representation；这些模型采用了不同的 action readout [Brohan et al., 2023a; Brohan et al., 2023b; Octo Model Team et al., 2024; Kim et al., 2024]。其中，RT-2 与 OpenVLA 将动作表示为离散 token，使机器人轨迹能够与语言共享 autoregressive interface。这条规模化路线进一步推动了 continuous generative action head：它需要保留 VLM 的语义先验，同时避免把高频、多模态 action chunk 压缩成单一点估计或很长的离散输出序列。

Flow Matching 已经在专用运动策略与通用 VLA 模型中逐步发展为机器人动作生成器。RFMP 在 Riemannian state space 上输运机器人运动，相关工作还将 Flow Matching 用于 multi-support whole-body imitation 和 affordance-conditioned manipulation [Braun et al., 2024; Rouxel et al., 2024; Zhang and Gienger, 2025]。这条技术路线经由 \(\pi_0\) 获得了更广泛的关注：\(\pi_0\) 将 Flow Matching 带入大规模通用 VLA，把预训练 VLM backbone 与较小的机器人专用 action expert 结合，并配合 cross-embodiment pretraining 与 post-training。它在高频灵巧操作任务中的突出表现，推动 Flow Matching 成为连续机器人动作生成中具有现实可行性和可扩展性的技术路线 [Black et al., 2024]。\(\pi_{0.5}\) 延续这一动作生成设计，并加入异构数据 co-training 与 semantic subtask prediction，以支持开放世界长时域操作 [Physical Intelligence et al., 2025]。除了预测性能以外，这种条件 Flow-Matching action expert 还提供了可在生成过程中进行干预的迭代速度场接口，使 action prefix 能够约束正在生成的 chunk。两种 RTC 表述分别通过 training-free pseudoinverse-guided inpainting 与 training-time action-prefix conditioning 利用了这一接口 [Black et al., 2025a; Black et al., 2025b]。这一联系自然引出下一主题关于异步执行与反馈机制的讨论。
