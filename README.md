# OpenClaw Agent Autotune

![CI](https://github.com/fengqve/openclaw-agent-autotune/actions/workflows/ci.yml/badge.svg)

> Public name: **OpenClaw 自动优化器（越跑越好）**

A production-friendly OpenClaw skill for continuous agent improvement with a strict loop:

**small change → benchmark → keep or rollback**

---

## 1) What this is

Most agent tuning is guesswork.

This skill gives you a repeatable method to improve agent quality while controlling cost and risk:

- Freeze a benchmark task set
- Try one small candidate change at a time
- Score quality/cost/latency/tool safety
- Keep only improvements
- Roll back regressions automatically

---

## 2) Who this is for

### Professional/technical users

Use this when you need:

- prompt/skill optimization with evidence
- lower token usage or latency without quality drop
- safe continuous improvement loops for OpenClaw

### Non-technical explanation

Think of it as an **automatic A/B tester for your AI assistant**:

- It tries a small improvement
- runs a fixed test set
- keeps it only if results are better

---

## 3) What is included

- `SKILL.md` — full operational instructions
- `scripts/score.py` — compute weighted score from metrics
- `scripts/run_once.py` — one-shot keep/rollback decision + TSV logging
- `examples/benchmark.tasks.example.jsonl` — benchmark example
- `examples/program.example.md` — strategy template
- `examples/results.example.tsv` — result log format
- `examples/base.metrics.example.json` — baseline metrics sample
- `examples/candidate.metrics.example.json` — candidate metrics sample
- `LICENSE` — MIT

---

## 4) Safety defaults

Allowed by default (editable):

- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `skills/*/SKILL.md`

Forbidden by default:

- gateway auth/security config
- secrets/payment/account actions
- destructive external actions

---

## 5) Quick start

1. Copy/install this skill into your OpenClaw skills directory.
2. Create `autotune/benchmark/tasks.jsonl` from the example file.
3. Set your scoring policy (default in `SKILL.md`).
4. Run one iteration: candidate change → benchmark → decision.
5. Append result to `autotune/results.tsv`.

### Script quick demo

```bash
cd skills/openclaw-agent-autotune
python3 scripts/run_once.py \
  --base examples/base.metrics.example.json \
  --candidate examples/candidate.metrics.example.json \
  --results examples/results.example.tsv
```

---

## 6) Naming strategy (for branding)

- Professional name: **openclaw-agent-autotune**
- Public-facing name: **OpenClaw 自动优化器（越跑越好）**

---

## 7) License

MIT
