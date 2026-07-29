# DreamZero 中 FBFM 反馈速度与 Jacobian/VJP 的计算

本文说明权重实验所使用的精确数值实现。它记录的是 DreamZero parallel-WAM 路线，
不改变 DreamZero 原生 16-step UniPC scheduler 或 8 次 DiT evaluation 预算。

## 1. 联合状态与动作流

令当前联合 solver sample 为：

```text
X = (Z, A)
```

其中 `Z` 是视频 latent，`A` 是 `16 x 32` 的模型动作张量。只有前 7 个物理动作
通道会被 LIBERO 执行或进入 action overlap。

一次 DreamZero DiT evaluation 返回 conditional/unconditional 视频速度和
conditional action 速度。实现使用：

```text
v_Z = v_Z_uncond + cfg_scale * (v_Z_cond - v_Z_uncond)
v_A = v_A_cond
v   = (v_Z, v_A)
```

action 分支不额外做视频式 CFG。这保持 released DreamZero checkpoint 的原生语义。

## 2. Clean endpoint 与反馈残差

DreamZero scheduler 使用递减的噪声坐标 `sigma`。当前 clean endpoint 估计为：

```text
Xhat = X - sigma * v
Zhat = Z - sigma * v_Z
Ahat = A - sigma * v_A
```

令反馈 target 为 `Y=(Y_Z,Y_A)`。`W_Z/W_A` 是二值 hard-overlap 支持矩阵，
`P_Z/P_A` 是模态预条件器。当前实现固定 `P_A=1`，并通过 state weight 设置
`P_Z`：

```text
e_Z = P_Z * W_Z * (Y_Z - Zhat)
e_A =       W_A * (Y_A - Ahat)
e   = (e_Z, e_A)
```

L1 分支使用 `P_Z=56/9600`，RMS 对照使用 `P_Z=sqrt(56/9600)`。代码中为了减少
一次乘法，将 `P_Z` 原地乘入 `state_mask`；在理论表达中应保持 `P` 与二值 `W`
分离。

action target 是已经 committed 的 8 个 action，每个 7 个物理坐标，共 56 个二值
mask 坐标。state target 是一个 `48 x 10 x 20=9600` 坐标的 latent slot，由真实
observation 以 checkpoint 训练时的 stride 3 编码。窗口依次为
`[0,0,0,0,3]`、`[0,0,0,3,6]`；未观测未来帧不会被复制为 hard target。

## 3. Jacobian 不显式构造

定义联合 endpoint Jacobian：

```text
        [ dZhat/dZ  dZhat/dA ]
J =     [ dAhat/dZ  dAhat/dA ]
```

实现不会实例化这个巨大矩阵，而是通过一次 `torch.autograd.grad` 计算 vector-Jacobian
product：

```text
g = J^T e
```

展开后：

```text
g_Z = (dZhat/dZ)^T e_Z + (dAhat/dZ)^T e_A
g_A = (dZhat/dA)^T e_Z + (dAhat/dA)^T e_A
```

因此 `g_A` 保留 state-to-action cross-modal 项 `(dZhat/dA)^T e_Z`。这正是状态
反馈能够改变动作的来源，也是在 Jacobian 增益过大时产生动作正反馈的路径。

`grad_outputs=(e_Z.detach(),e_A.detach())`。反馈 residual 不继续反传，只有 endpoint
对当前 joint sample 的导数参与 VJP。诊断模式可以拆成 state-to-video、
state-to-action、action-to-video 和 action-to-action 四次分块统计；正式推理使用一次
联合 backward，避免额外开销和 BF16 运算顺序差异。

## 4. Guided velocity

FBFM 的 scheduler 权重在 `sigma` 坐标下计算：

```text
tau     = 1 - sigma
r_sq    = sigma^2 / (tau^2 + sigma^2)
lambda  = clip(sigma / (tau * r_sq), 0, beta)
beta    = 10
v_guide = v - lambda * g
```

减号来自 DreamZero 使用递减 `sigma`，而论文常以递增流时间书写。所有 guided
video/action velocity 在交给 scheduler 前 detach，并显式检查 finite。

## 5. 8 次 DiT 与 16 次 UniPC 的缓存边界

DreamZero 做 16 次 scheduler update，但只在 native `dit_step_mask` 的 8 个位置
计算 DiT。正确缓存策略为：

1. 在原生 DiT evaluation 处，用当前 `X` 建立 endpoint autograd graph 并得到 `J_k`；
2. 计算当前 index 的 residual、VJP 和 guided velocity；
3. 返回未引导的 native DiT predictions，使 DreamZero `prev_predictions` 只缓存
   `v_k`，绝不缓存 `v_guide`；
4. scheduler callback 只在当前 update 使用 `v_guide`；
5. 在跳过 DiT 的 index，以当前 `X_j`、`sigma_j` 和缓存的 native `v_k` 重算
   `Xhat_j`、`e_j` 和 `J_k^T e_j`；
6. 到下一次原生 DiT evaluation 时同时刷新 `v_k` 和 `J_k`。

这实现了“index 3/4/5 重算 `Y-Xhat`，但不增加 DiT/Jacobian 前向”的要求。旧实现
把 guided velocity 写入 `prev_predictions`，会把一次高噪声修正在多个 scheduler
index 重复积分；递归使用上一 index 的 guided velocity 更会产生百万量级速度。

## 6. Jacobian 复用的局部有效域

缓存 `J_k` 隐含一个局部线性假设：跳过 DiT 时的 solver sample 仍接近建立
linearization 的位置。RMS trial 18 表明该假设会失效。其 scheduler index 6-9 的
action correction 为：

```text
138.15 -> 699.83 -> 2928.63 -> 11260.61
```

guided action velocity 峰值达到 `46455.02`，最后生成 norm `168.37` 的物理动作。
L1 把相同 state residual 路径预条件得更弱，20 次测试中的 guided action velocity
最大值为 `68.68`，物理 action norm 最大值为 `1.612`。

当前证据支持将 `56/9600` 作为批量实验默认值，但它不是一般性的稳定性证明。
如后续任务仍出现尾部爆炸，应在不改变二值 hard overlap 的前提下评估：

- `||lambda g|| / ||v||` 相对 trust region；
- cached-index correction 增长率门控；
- 越界时仅对当前 index 回退到 native `v_k`；
- 必要时提前刷新 Jacobian，同时单独报告额外 DiT 成本。

## 7. 代码位置与版本

```text
FBFM repository: https://github.com/StvLi/FBFM
L1 handoff branch: experiment/dreamzero-l1mass-state-weight
L1 handoff commit: cb08c9e552730d26cc446885e79a3e270a270d0c
relinearized solver commit: 9d69cbc541c5e6c0c52c4875e2e9c42c7d9626b6
RMS numerical commit: 13de791f74139b165cff70ff8165b1cc4538ea64

joint VJP:
  src/dreamzero_fbfm/guidance.py

constraint weighting and DiT hook:
  src/dreamzero_fbfm/runtime.py

DreamZero scheduler callback patch:
  patches/dreamzero_external_step_guidance.patch
```
