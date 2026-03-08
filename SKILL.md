---
name: openclaw-agent-autotune
version: 0.1.0
description: >
  Optimize OpenClaw agents with a safe eval loop: propose small prompt/skill
  changes, run fixed benchmark tasks, keep only improvements, and roll back
  regressions. Use this whenever users ask to improve agent quality, reduce
  token cost/latency, or build continuous self-improvement for OpenClaw.
author: FengQve
---

# OpenClaw Agent Autotune

**Public name:** OpenClaw 自动优化器（越跑越好）

Build a controlled "improve → evaluate → keep/rollback" loop for OpenClaw agents.

## What this skill does

This skill helps you:

1. Define a fixed benchmark set (real tasks)
2. Propose small candidate changes (prompt/skill only)
3. Evaluate candidates with consistent scoring
4. Keep only improvements, rollback regressions
5. Run this loop repeatedly (manual or scheduled)

## When to use this skill

Use this skill when users ask things like:

- "优化我的 OpenClaw agent"
- "让提示词越跑越好"
- "降低 token 成本/响应延迟"
- "做一个自动评测+回滚机制"
- "想要一个安全的自我进化流程"

Do **not** use this skill for one-off simple edits that do not need benchmarking.

---

## Core principle

**No benchmark, no claim.**

You only say "improved" when metrics improve on a fixed benchmark.

---

## Scope and safety

### Allowed change targets (default allowlist)

- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `skills/*/SKILL.md`
- Non-sensitive workflow docs and scripts under workspace

### Forbidden by default

- Gateway auth/security config
- Payment/account credentials
- External destructive actions
- Unreviewed changes outside workspace

If user asks to expand scope, ask for explicit confirmation first.

---

## Standard workspace layout

```text
autotune/
  program.md                 # Human strategy and constraints
  benchmark/
    tasks.jsonl              # Frozen benchmark tasks
  candidates/
    candidate-001.diff
  runs/
    run-YYYYMMDD-HHMM/
      score.json
      report.md
  results.tsv
```

If missing, create these files/directories.

---

## Step-by-step workflow

### Step 1) Freeze benchmark

Create `autotune/benchmark/tasks.jsonl` with 10-30 representative tasks.
Each line should include:

- `id`
- `prompt`
- `expected` (brief success criteria)
- `risk_level` (`low|medium|high`)

Do not change benchmark during one tuning cycle.

### Step 2) Define scoring

Use this default weighted score:

```text
score =
  0.55 * success_rate
- 0.20 * token_cost_norm
- 0.15 * latency_norm
- 0.10 * tool_error_rate
```

Hard fail gates (any one fails => candidate rejected):

- success_rate drops > 2%
- high-risk tool misuse > 0
- token cost increases > 20%

### Step 3) Generate one small candidate

Generate only **one minimal change** per iteration.
Prefer reversible edits and clear diffs.

### Step 4) Run benchmark

Run all tasks with consistent settings:

- same model
- same timeout policy
- same environment

Store raw outputs and metrics in `autotune/runs/...`.

### Step 5) Decide keep/rollback

- If score improves and no hard gate fails → `keep`
- Otherwise → `rollback`

Record decision in `autotune/results.tsv`.

### Step 6) Report

Always produce a concise report:

- what changed
- score before/after
- keep/rollback
- risk notes
- next candidate idea

---

## Results format

Use tab-separated `autotune/results.tsv`:

```tsv
run_id	base_score	candidate_score	decision	notes
20260308-1400	0.742	0.761	keep	Better success rate on planning tasks
20260308-1430	0.761	0.748	rollback	Higher latency, no quality gain
```

---

## OpenClaw integration recommendations

1. Start manually until stable
2. Then schedule with cron (isolated `agentTurn`)
3. Post daily summary to target channel
4. Keep a strict budget cap (time/tokens)

For cron-based runs, include reminder-like summary text with:

- baseline score
- current best score
- last decision
- top failure pattern

---

## Communication style for this skill

When running autotune tasks, use this output structure:

1. 目标
2. 约束
3. 动作
4. 结果
5. 风险

Be explicit when evidence is incomplete.
Never claim improvement without metrics.

---

## Minimal deliverable checklist

Before declaring done:

- [ ] benchmark frozen
- [ ] scoring formula documented
- [ ] at least 1 candidate evaluated
- [ ] keep/rollback decision recorded
- [ ] results.tsv updated
- [ ] risk notes written

If any unchecked, do not claim completion.

---

## Out of scope

This skill does not automatically:

- tune core model weights
- bypass platform safeguards
- guarantee monotonic improvement

It is an **evaluation discipline + safe iteration loop**.
