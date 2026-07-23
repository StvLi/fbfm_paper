# 【Research Record】PiGDM\-based State\-Feedback Flow\-Matching for WAM

# （叠甲）统一说明

本方法主要就Flow\-matching进行讨论，文字表述中可能出现的**"去噪"**是Flow\-matching的正向积分过程的不严谨中文表述。

本方法主要讨论在潜空间\(Latent Space\)进行状态预测、在原本动作空间进行流匹配生成的Flow\-matching模型，在提及**“状态”**默认指的是在潜空间编码后的状态，**“观测”**默认指的是传感器直接获得的、未编码的物理信息，**“动作”**指的是动作矢量。模型流匹配生成的是潜空间“状态”和物理空间“动作”拼接得到的**复合矢量**。

# 基本思路

参考RTC通过将action chunk作为图像扩展进行chunk之间的拼合，可以将去噪过程中新获得的状态作为已知反馈，约束流匹配中状态的预测过程，从而影响动作序列的生成。

# 解决问题

1\. 基于WM的动作生成实时性较差（相当于增强RTC）；

2\. 在每个chunk执行过程中，没有对后续转移转移到的状态进行响应。

# 创新点

1. 提出了基于流匹配世界模型进行状态反馈的框架；

2. 完成了以上推理部署的所需的异步多线程工程实现。

# 原理公式

$v_{\Pi GDM}(X^\tau_t,o_t, \tau)
=
v(X^\tau_t,o_t, \tau)
+k_p(Y-\hat{X^1_\tau})^Tdiag(W)\frac{\partial\hat{X^1_t}}{\partial{X^\tau_t}}$

其中：

$X^\tau_t=[Z^\tau_t,A^\tau_t ]$

$\hat{X^1_t}=X^\tau_t+(1-\tau)v(X^\tau_t,o_t, \tau)$

$k_p=min(\beta,(\frac{1-\tau}{\tau})(\frac{1}{r_\tau^2}))$

$r_\tau^2=\frac{(1-\tau)^2}{\tau^2+(1-\tau)^2}$

$Y$反馈值，包括状态反馈和动作反馈。动作反馈来自于上一个chunk，状态反馈来自执行上一个chunk获得的物理观测的状态编码：

$Y=h†([s,a_{last}])$

$e.g. Y=[VAE.Enc(images).\mu , a_{last}]$

## 关于$h†$：

对于在集合$\mathbb{Z}$上，非线性映射$h(z)，z\in \mathbb{Z}$，

若存在$h†$使得：

$h(h†(h(z)))=h(z)$

则称：

$h†$是$h$在$\mathbb{Z}$上的**MP逆**。

$W$是动态掩码，用于标记状态反馈更新情况，仅在有相应反馈时置1，其他置0。

# 算法伪代码

|$\textbf{Algorithm 1} \text{\space VA\space  State \space Feedback}$||||||
|---|---|---|---|---|---|
|$\textbf{Require:}$||||||
|$\pi$||Flow policy||||
|$H$||Prediction Horizon||||
|$s_{chunk}$||Minimum Chunk Execution Horizon||||
|$s_{step}$||Minimum Step Execution Horizon||||
|$\mathcal{M}$||Mutex||||
|$\mathcal{C}$||Condition Variable||||
|$A_{init}$||Initial Action Chunk||||
|$d_{init}$||Initial Delay Estimate||||
|$b$||Delay Buffer Size||||
|$n$||Number of Denoisingh Steps||||
|$\beta$||Maximum Guidance Weight||||
|$\mathcal{PC}$||RTC Previous Chunk||||
|1|$\textbf{procedure}$$\text{INITIALIZESHAREDSTATE}$|||||
|2||$t=0;A_{cur}=A_{init                                                                                                                                                                                                                                                                                                                                                                           },o_{cur}=null$||||
|3||$\text{Initialize }\mathcal{PC}\text{ from }A_{cur}[s,s+1,...,H-1]$||||
|4|$\textbf{funtion}\space \text{GETACTION}(o_{next})$|||||
|5||$\textbf{with} \space \mathcal{M} \space \text{acquired} \space \textbf{do}$||||
|6||$t=t+1$||||
|7||$o_{cur}=o_{next}$||||
|8||$\text{notify} \space  \mathcal{C}$||||
|9||$\text{with }\mathcal{M}\text{ released } \textbf{do}$||||
|10|||$\text{encode } o_{cur} \text{ as } z_{cur}$|||
|11|||$\mathcal{PC}.\text{append state latent(} z_{cur} \text{)}$ |||
|12||$\textbf{return} \space \textbf{A}_{cur}[t-1]$||||
|13|$\textbf{procudure} \space  \text{INFERENCELOOP}$|||||
|14||$\text{acquire} \space \mathcal{M}$||||
|15||$\mathcal{Q}=new \space Queue([d_{init}],maxlen=b)$||||
|16||$\textbf{loop}$||||
|17|||$\text{wait on}\space\mathcal{C}\space\text{until }t\geq\space s_{chunk}$|||
|18|||$s=t$|||
|19|||$\text{new }\mathcal{PC}\text{ from }A_{cur}[s,s+1,...,H-1]$|||
|20|||$o=o_{cur}$|||
|21|||$d=max(\mathcal{Q})$|||
|22|||$\text{with }\mathcal{M}\text{ released } \textbf{do}$|||
|23||||$A_{new}=\text{GUIDEDINFERENCE}(\pi,o,A_{prev},d,s)$||
|24|||$\bf A_{cur}=A_{new}$|||
|25|||$t=t-s$|||
|26|||$\text{enqueue } \it{t} \text{ onto } \mathcal{Q}$|||
|27|$\textbf{function}\space \text{GUIDEDINFERENCE(}\pi, o,A_{prev},d,s\text{)}$|||||
|28||$\text{get } \textbf{W} <br>\text{ from } \mathcal {PC}<br>$||||
|29||$\text{get }X_{prev}\text{ from }\mathcal{PC} \text{ and right-pad} \space X_{prev} \space \text{to length }H; $||||
|30||$\text{initialize } X^0 \sim \mathcal{N}\text{(0,I)}$||||
|31||$\textbf{for } \tau \text{ = 0 to 1 with step size 1/n } \textbf{do} $||||
|32|||$f_{\hat{x^1}}= \bf{X`}\mapsto\bf{X`}+(1-\tau)\bf{v}_{\pi}(\bf{X`},o,\tau)$|||
|33|||$e = (X_{constrain} - f_{\hat{X^1}}(X^\tau))^\intercal diag(\bf{W})$|||
|34|||$\bf g=e·\left. \frac{\partial f_{\hat{X^1}}}{\partial{X`}}\right|^{}_{X`=X^\tau}$|||
|35|||$\bf{X^{\tau+\frac{1}{n}}}=X^\tau+\frac{1}{n}\left(\bf{v_\pi(X^\tau,o,\tau)}+min(\beta,\frac{1-\tau}{\tau·r^2_\tau})g \right)$|||
|36|$\bf return \space A^1$|||||

实验设计

1. 主实验：RoboTwin任务上的性能提升

实验目的：验证所提出的training\-free的方法的引入对于VA模型的性能提高具有正面效果。

实验方案：（原模型/RTC/Ours）\+（Lingbot\_VA/DreamZero）排列组合，分别记录在RoboTwin上的成功率。

实验记录表格：

|任务|指标<br>（要不要加其他指标？）|Lingbot|Lingbot\+<br>RTC|Lingbot\+<br>Ours|DreamZero|DreamZero\+RTC|DreamZero\+Ours|
|---|---|---|---|---|---|---|---|
|task1|成功率|||||||
|task2|成功率|||||||
|task3|成功率|||||||

预期结果：所提出方法相对于裸VA和VA\+RTC成功率有所上升。

讨论：关于显著提升效果任务进行针对分析。

2. 辅助实验1：测试反馈对状态估计准确性的提升

实验目的：验证所提出的方法确实通过反馈机制约束了状态生成，提高了准确率。

实验方案：使用不同后训练量的模型裸策略/所提出方法，对测试集轨迹的潜空间状态估计准确性\(MSE\)进行比较。

实验记录表格：

|任务|lingbot||||lingbot\+ours||||
|---|---|---|---|---|---|---|---|---|
||0|1000|2000|5000|0|1000|2000|5000|
|state MSE|||||||||

|任务|ZeroDream||||ZeroDream\+ours||||
|---|---|---|---|---|---|---|---|---|
||0|1000|2000|50000|0|1000|2000|5000|
|state MSE|||||||||

预期结果：Ours的latent state显著小

讨论：引入的train\-free新方法有效加速了状态预测收敛

3. 辅助实验2：真机部署测试chunk内鲁棒性

实验目的：验证这一方法增强了系统对chunk内干扰的鲁棒性

# 重要参考资料

RTC

使用PiGDM进行Action Chunk拼接：J Kim, Real\-Time Execution of Action Chunking Flow Policies：http://arxiv\.org/abs/2506\.07339

LeRobot中PiGDM的复现代码：https://github\.com/huggingface/lerobot/tree/main/src/lerobot/policies/rtc

数学原理：PiGDM：J Song, Pseudoinverse\-Guided Diffusion Models for Inverse Problems：https://openreview\.net/forum?id=9\_gsMA8MRKQ

蚂蚁灵波VA：

网站：https://github\.com/robbyant/lingbot\-va

论文：L LI, Causal World Modeling for Robot Control: http://arxiv\.org/abs/2601\.21998

踩坑：[Lingbot翠湖部署踩坑](https://jwolpxeehx.feishu.cn/wiki/CsnRwS1spi3ppZkHoxPcvbW8nxc)

# 计划与执行

## TODO List

**分锅：两个【核】或以上可以成为共一**

* [ ] 准备工作：在RoboTwin上进行VA模型推理

    * [ ] lingbot\-VA工具链 @李佩泽@飞书用户8879XR@王玎

        * [ ] 部署Lingbot\-va

        * [ ] RoboTwin微调lingbot\-va

        * [ ] 真机数据微调lingbot\-va

        * [ ] Lingbot VAE Latent编码调用

    * [ ] 【有时间再整】DreamZero

* [ ] 工程工作：将FBFM接入

    * [ ] 【核】根据lerobot RTC改写FBFM @李佩泽

    * [ ] 【核】FBFM \+ lingbot\-va \+ RoboTwin拼装的 @李佩泽

* [ ] 实验

    * [ ] 【核】主实验0：在RoboTwin测试 @飞书用户8879XR

        对比Lingbot和Lingbot\+FBFM在RoboTwin上的成功率差异

        @张芮萌（关于Horizon长度）

    * [ ] 【核】辅实验1：在简单仿真环境上状态预测 @王玎

        说明FBFM对状态估计的作用

    * [ ] 辅实验2：见下\[真机Demo\] @李佩泽

    说明FBFM增强了chunk内反馈能力

* [ ] 【核】真机Demo：Franka @李佩泽

    1. 能部署 真机有用

    2. 展现特性（对in\-chunk distribution有响应）

    * [ ] lingbot\-va

    * [ ] lingbot\-va \+ FBFM

    * [ ] lingbot\-va \+ RTC（对照组）

* [ ] 理论推导

    * [ ] 【核】FBFM核心理论：基于PGDM的状态反馈@李佩泽

    * [ ] VAE解\-编码器的MP逆近似理论@李佩泽

* [ ] **New Idea🎉**

    * [ ] 动态掩码衰减系数，协调新获得状态效果不明显，提出:@飞书用户8879XR

    * [ ] KF（之后在做？）@飞书用户8879XR

* [ ] 论文写作（后事）

    * [ ] Abstract

    * [ ] Introduction

    * [ ] Method

    * [ ] Experiment \& Result \& Discussion

    * [ ] Related Works

    * [ ] Conclusion \& Future Work

    * [ ] ~~Appendix~~

## 计划时间表

|进程|日期|@李佩泽|@王玎|@张芮萌||
|---|---|---|---|---|---|
||2026\.03\.06|* [x] 跑通lingbot\-va RoboTwin后训练||||
|→|2026\.03\.13|* [ ] 根据lerobot RTC改写FBFM|* [ ] 辅助实验1|||
||2026\.03\.20|* [ ] FBFM \+ lingbot\-va \+ RoboTwin拼装||3\.25 lingbotva\+fbfm 单线程跑通||
||2026\.03\.27|||threading||
||2026\.04\.03|* [ ] 真机pipeline搭建完毕||dreamzero\+fbfm||
||2026\.04\.10|||threading||
||2026\.04\.17|* [ ] 全部实验做完||||
||2026\.04\.24|||||
||2026\.04\.30|* [ ] Arxiv Preprint||||
||2026\.05\.07|预留备用||||
||2026\.05\.14|\-\-\-\- NeurIPS 截稿 \-\-\-\-||||
||Rebuttal|补齐appendix理论推导||||

## 研究日志

|日期|概述|详细说明|TODO|
|---|---|---|---|
|2026\-03\-11|1. 完成lingbot RoboTwin部署测试，成功率75%。|||
|2026\-03\-08|1. 完成lingbot后训练<br>2. 完成lingbot推理环境配置|1. 完成了50000步后训练<br>2. 配置robotwin\_lingbot\_va环境<br>3. 服务器和客户端分别可运行<br>4. 服务器和客户端不能通讯**×**||
|2026\-03\-02|九鼎部署Lingbot<br>阅读ZeroDream|Lingbot在下载RoboTwin材质中；<br>关注到ZeroDream通过极致优化流匹配过程也意图解决这一问题，但是会牺牲成功率作为代价。||
|2026\-02\-28|伪代码整理|将02\-27实现的代码整理为文档（真机部署部分有待讨论）。||
|2026\-02\-27|代码开发|在lerobot的RTC基础上完成了代码开发，实现了上一chunk封装、理论上可以接入VA模型了。|* [x] 配置服务器<br>* [x] 尝试接入lingbotVA进行测试。<br>* [ ] debug|



