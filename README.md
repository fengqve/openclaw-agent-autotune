# OpenClaw Agent Autotune

![CI](https://github.com/fengqve/openclaw-agent-autotune/actions/workflows/ci.yml/badge.svg)

> Public name: **OpenClaw 自动优化器（越跑越好）**

A production-friendly OpenClaw skill for continuous agent improvement with a strict loop:

**small change → benchmark → keep or rollback**

---

## 1) 一句话

它会**自动执行评测闭环**，并且**只有指标变好时才保留改动**。

---

## 2) 安装（给最终用户）

不需要用户跑命令。让用户直接对 OpenClaw 说：

- `帮我安装 openclaw-agent-autotune`

安装后再说：

- `用 openclaw-agent-autotune 跑一轮优化并汇报结果`

> 备注：这是面向最终用户的安装方式（对话安装）。

---

## 3) 效果展示（自动）

你不需要让用户手动执行脚本，效果通过自动化直接展示：

1. 每次 push / PR，GitHub Actions 会自动跑 demo
2. CI 徽章会实时显示是否通过
3. Run 页面会自动展示本轮 `keep/rollback` 结果（job summary + log）

也就是说：

- 有效果：CI 和运行结果会持续显示
- 没效果：不会保留改动（rollback）

---

## 4) 仓库包含内容

- `SKILL.md` — skill 行为定义
- `scripts/score.py` — 计算综合评分
- `scripts/run_once.py` — 单轮 keep/rollback 决策 + TSV 记录
- `examples/*` — benchmark / metrics / results 示例
- `.github/workflows/ci.yml` — 自动验证与自动展示
- `LICENSE` — MIT

---

## 5) 对外文案（推荐）

**它会自动执行，只有指标变好时才保留改动。**

---

## 6) License

MIT
