# OpenClaw Agent Autotune

![CI](https://github.com/fengqve/openclaw-agent-autotune/actions/workflows/ci.yml/badge.svg)

> Public name: **OpenClaw 自动优化器（越跑越好）**

它会自动执行，只有指标变好时才保留改动。

---

## 用户怎么安装（对话方式）

直接对 OpenClaw 说：

- `帮我安装 openclaw-agent-autotune`

安装后再说：

- `用 openclaw-agent-autotune 跑一轮优化并汇报结果`

> 目标是让最终用户无需手动跑脚本。

---

## 效果在哪里看（自动展示）

无需用户执行命令，结果自动出现在 GitHub Actions：

1. **CI 徽章**：一眼看当前是否通过
2. **Actions Run Summary**：可读报告，包含：
   - 结论（keep / rollback）
   - 为什么是这个结论（gate 检查 + 分数比较）
   - 修改了哪里（change metadata）
   - 修改带来什么提升（各指标 delta）
3. **Artifacts**：完整机器可读输出
   - `run_once_output.json`
   - `results.tsv`
   - `decision_report.md`

---

## 仓库包含

- `SKILL.md` — skill 行为定义
- `scripts/score.py` — 计算综合评分
- `scripts/run_once.py` — 单轮 keep/rollback 决策 + 解释报告
- `examples/benchmark.tasks.example.jsonl`
- `examples/base.metrics.example.json`
- `examples/candidate.metrics.example.json`
- `examples/change.example.json`
- `.github/workflows/ci.yml` — 自动验证与自动展示
- `LICENSE` — MIT

---

## 核心机制

- 固定 benchmark
- 每轮只改一个小候选
- 统一打分 + 硬门槛
- 只保留更优结果
- 不达标自动回滚

---

## License

MIT
