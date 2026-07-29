# Prompt for the Next Agent

Copy the prompt below to the agent taking over the FBFM paper. Replace `<PASSPHRASE_PROVIDED_SEPARATELY>` with the separately transferred passphrase; never commit the filled prompt.

---

请接管 FBFM AAAI 论文项目，并恢复上一台设备上的完整 Codex 会话上下文。论文仓库为 `https://github.com/StvLi/fbfm_paper.git`，当前交接分支为 `figures/latex-formula-assets`。

请依次完成以下操作：

1. 将仓库克隆或更新到本机工作区，并检出 `figures/latex-formula-assets` 的 origin 最新提交。保留任何已有的、与本次交接无关的本地改动。
2. 仓库中的 `handover/codex_chat_2026-07-29_019fa9b0.tar.gpg` 是 AES-256 加密的原始 Codex 会话。使用密码 `<PASSPHRASE_PROVIDED_SEPARATELY>` 解密，将归档内容恢复到 `~/.codex/`。不要在终端输出、回复或新文件中复述会话原文、密码或其中包含的其他凭据。
3. 恢复后的会话 ID 是 `019fa9b0-8b8a-7073-af26-c2ba1c1e8b13`。如果当前界面支持原会话恢复，使用该 ID 恢复；如果你已经处于一个新的 agent 会话，则读取该 JSONL 作为项目上下文，重点理解论文的符号体系、Method、Experiment/Appendix 边界、实验分支工作流和用户已经确认的写作判断，不要从头重复已经完成的工作。
4. 检查仓库分支、HEAD、工作树状态以及 `docs/preview.pdf` 的本地编译能力。不要运行大型模型或实验代码，也不要改动未获授权的实验数据。
5. 完成恢复后，只需向我报告：当前分支与 HEAD、会话是否恢复、论文是否能继续编译、是否发现阻塞项。然后等待我的下一项写作任务。

可采用以下恢复命令；其中密码只在本次受信任交接中使用：

```bash
mkdir -p "$HOME/.codex"
gpg --batch --yes --pinentry-mode loopback \
  --passphrase '<PASSPHRASE_PROVIDED_SEPARATELY>' \
  --decrypt handover/codex_chat_2026-07-29_019fa9b0.tar.gpg \
  | tar -xvf - -C "$HOME/.codex"
```

---
