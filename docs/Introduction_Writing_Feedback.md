# Introduction 写作反馈与改进建议

本文档基于 FBFM Introduction 初稿整理，目的是说明本次修改的原因，并给出以后撰写论文 Introduction 时可以复用的方法。当前修订稿见 [1_Introduction.md](Chapters/1_Introduction.md)。

## 1. 初稿中值得保留的思路

初稿已经抓住了几个重要问题：

- 能够从 WAM 的未来预测能力出发，引出预测偏离真实环境时的部署风险；
- 意识到真实观测不应只被压缩为全局误差，而应保留其数值和时间位置；
- 能够主动比较 RTC、FWM 和 RA-DP 等相邻工作，寻找 FBFM 的研究增量；
- 提出了将 WAM 未来状态生成理解为部分观测生成问题的关键洞察。

这些内容构成了可用的研究叙事基础。本次修改主要解决的是事实边界、章节分工和论证重心，而不是推翻上述思路。

## 2. 本次初稿的主要问题

### 2.1 Introduction 中的方法描述与正式 Method 不一致

初稿将反馈描述为在下一次 generation call 前构造的固定 target，并在整段采样过程中保持不变。这对应的是一次 pre-inference snapshot，而不是论文正式定义的 FBFM。完整方法要求新到达的状态反馈作用于仍在生成的 active chunk，并在后续 solver evaluation 前更新相应 target 和 mask。

改进原则：涉及方法时序、变量更新和适用边界的表述，必须以 [3_Method.md](Chapters/3_Method.md) 为事实来源。Introduction 可以省略公式，但不能为了简化而改变方法实际含义。

### 2.2 为了强调相对 RTC 的增量，弱化了完整 FBFM

初稿重点强调 latent-state feedback，这有助于说明 FBFM 与 RTC 的区别，但 previous-action constraint 因此被降成了附属实现细节。完整 FBFM 的特点恰恰是使用统一的受约束生成接口处理 states 和 actions：真实状态是动态到达的测量，前一 chunk 的动作则构成固定的跨 chunk 承诺。

改进原则：比较基线时，应明确“基线解决了什么”和“本文增加了什么”，但不能让增量遮蔽完整方法。可以突出 RTC 只约束 action overlap，而 FBFM 进一步约束 WAM 的未来状态流，同时仍保留动作连续性约束。

### 2.3 专业术语和架构分类没有与全文统一

初稿使用了 `cascaded dual-stream`、`unified joint-prediction`、`dominant` 和 `exclusive conditioning` 等表述。这些词有的与全文已经确定的 `stage-wise generation`、`joint generation` 不一致，有的则包含未经充分文献支持的强判断。

改进原则：开始写作前应建立术语表，记录每个核心概念的唯一正式名称。描述架构时先给出论文采用的抽象分类，再将具体模型作为实例；除非有系统性文献证据，不使用 `dominant`、`all`、`only`、`exclusive` 等扩大适用范围的词。

### 2.4 Introduction、Related Works、Method 和 Experiments 的分工混杂

初稿用了较大篇幅解释 Fast-WAM、FWM 和 RA-DP 的具体机制，同时提前写入 persistent buffer、isolated VAE stream 和 cache 等实现细节。这使 Introduction 同时承担了相关工作评述和实验实现说明，削弱了主问题的推进速度。

各章节应承担不同职责：

- **Introduction**：说明问题为什么重要、现有方法缺少什么、本文的核心洞察和贡献是什么；
- **Related Works**：准确讨论前人工作的机制、假设、优点和边界；
- **Method**：描述不依赖具体代码路径的通用理论设计；
- **Experiments**：交代模型、buffer、VAE、cache、调度方式和超参数等具体实现。

### 2.5 贡献列表没有覆盖论文的完整事实

初稿第三项贡献只声称在一种 stage-wise WAM 上完成实例化，而论文实际覆盖 stage-wise generation 和 joint generation 两类 WAM。该条目还混入了较多模型专用工程组件，导致贡献看起来像一次代码适配，而不是可以迁移的研究方法。

改进原则：贡献列表应分别对应“问题形式化、方法创新、实验验证”，并与 Abstract、Method 和 Experiments 一一对应。贡献项不应包含只有单个实现使用的工程细节。

### 2.6 文献判断和强事实声明缺少核验

初稿对部分 WAM 的 KV cache 更新方式、conditioning 关系及 FWM、RA-DP 的适用范围作出了较强判断。这类内容必须逐条回到原论文确认，不能根据二手概括推断整个方法类别。

改进原则：为每个关键判断保留“claim--source”记录。无法定位到原论文具体章节、公式或实验的判断，应删除、弱化，或者明确限定到某个具体模型。

## 3. 推荐的 Introduction 组织方法

FBFM 的 Introduction 可以采用以下论证顺序：

1. **研究价值与部署矛盾**：WAM 的未来预测支持长时程决策，但错误未来也会误导动作生成。
2. **现有反馈的粒度缺口**：真实观测通常只在 chunk 边界更新上下文，不能纠正 active chunk 内的逐步预测误差。
3. **相邻技术与未解决问题**：RTC 已能通过 inpainting 保持 action overlap 一致，但没有约束 WAM 显式生成的未来状态。
4. **核心洞察**：执行和生成的重叠使未来状态 chunk 成为动态部分观测对象，真实状态可以按时间位置对齐到 latent slots。
5. **方法概述与适用范围**：FBFM 统一处理动态 state feedback 和固定 action consistency，并适用于 stage-wise 与 joint generation。
6. **贡献总结**：依次列出问题形式化、training-free 方法和跨架构实验验证。

每一段只承担一个主要功能。段首提出该段判断，段中给出必要解释，段尾自然引向下一段。不要在同一段同时完成背景介绍、方法推导和文献批评。

## 4. 推荐的写作流程

1. 先用一句话写出论文主张，例如：“FBFM 将 WAM 执行期间新到达的状态和既有动作承诺转化为 active Flow-Matching chunk 上的时间对齐约束。”
2. 为每一段写一句功能说明，再开始扩展正文；如果两段承担相同功能，应合并或重新分工。
3. 对照 Abstract 和 Method 建立事实清单，特别检查反馈何时到达、作用于哪个 chunk、哪些量动态更新，以及模型参数是否冻结。
4. 建立术语表，统一架构名称、反馈名称、Flow-Matching 时间和环境时间等概念。
5. 将所有模型专用实现词暂时标记出来；如果它不是理解核心贡献所必需的，就移动到 Experiments。
6. 对所有前人工作判断补充原始引用，并记录能够支持该判断的章节或公式。
7. 最后检查贡献列表是否分别对应正文的问题、方法和证据，且没有超出实验实际完成的范围。

## 5. 交稿前自查清单

- [ ] Introduction 中的方法时序是否与 Method 完全一致？
- [ ] 是否同时说明了 state feedback 和 previous-action consistency？
- [ ] 是否准确解释了相对 RTC 的区别，而没有将 RTC 描述成 FBFM？
- [ ] 是否统一使用 `stage-wise generation` 和 `joint generation`？
- [ ] 是否删除了不必要的 buffer、VAE、cache 和服务器实现细节？
- [ ] 每个强事实判断是否有原论文依据？
- [ ] Related Works 的内容是否只在 Introduction 中保留了支持 GAP 所需的最小部分？
- [ ] 三项贡献是否分别对应问题、方法和实验，并与 Abstract 保持一致？
