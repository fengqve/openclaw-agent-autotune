# Autotune Program (Example)

## Goal
Improve response quality for OpenClaw group-chat execution tasks while reducing token usage.

## Constraints
- Do not reduce success rate by more than 2%
- No high-risk tool misuse
- Token increase must stay under 20%

## Allowed edit scope
- AGENTS.md
- skills/*/SKILL.md

## Iteration policy
- One minimal candidate change per run
- Always benchmark against fixed tasks
- Keep only if score improves and hard gates pass

## Scoring
score = 0.55*success_rate - 0.20*token_cost_norm - 0.15*latency_norm - 0.10*tool_error_rate

## Budget
- Max 10 runs per day
- Max 60 minutes per day

## Reporting
For each run report:
- change summary
- base score / candidate score
- keep or rollback
- risk notes
