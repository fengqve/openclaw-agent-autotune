#!/usr/bin/env python3
"""Single-run decision helper for OpenClaw Agent Autotune.

Compares base vs candidate metrics and outputs:
- keep/rollback decision
- machine-readable JSON
- optional human-readable markdown report
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from score import compute_score


HARD_GATES = {
    "success_drop_max": 0.02,   # >2% drop = fail
    "tool_error_max": 0.0,      # any high-risk misuse = fail
    "token_increase_max": 0.20, # >20% increase = fail
}


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def evaluate(base: dict, cand: dict) -> dict:
    base_score = compute_score(base)
    cand_score = compute_score(cand)

    success_drop = float(base["success_rate"]) - float(cand["success_rate"])
    token_increase = float(cand["token_cost_norm"]) - float(base["token_cost_norm"])
    tool_error = float(cand["tool_error_rate"])

    gate_checks = {
        "success_drop": {
            "value": round(success_drop, 6),
            "max": HARD_GATES["success_drop_max"],
            "pass": success_drop <= HARD_GATES["success_drop_max"],
        },
        "tool_error_rate": {
            "value": round(tool_error, 6),
            "max": HARD_GATES["tool_error_max"],
            "pass": tool_error <= HARD_GATES["tool_error_max"],
        },
        "token_cost_increase": {
            "value": round(token_increase, 6),
            "max": HARD_GATES["token_increase_max"],
            "pass": token_increase <= HARD_GATES["token_increase_max"],
        },
    }

    hard_fail_reason = None
    if not gate_checks["success_drop"]["pass"]:
        hard_fail_reason = "hard_gate: success_rate dropped >2%"
    elif not gate_checks["tool_error_rate"]["pass"]:
        hard_fail_reason = "hard_gate: tool_error_rate > 0"
    elif not gate_checks["token_cost_increase"]["pass"]:
        hard_fail_reason = "hard_gate: token_cost increase >20%"

    if hard_fail_reason:
        decision = "rollback"
        note = hard_fail_reason
    elif cand_score > base_score:
        decision = "keep"
        note = "score improved"
    else:
        decision = "rollback"
        note = "score not improved"

    deltas = {
        "success_rate": round(float(cand["success_rate"]) - float(base["success_rate"]), 6),
        "token_cost_norm": round(float(cand["token_cost_norm"]) - float(base["token_cost_norm"]), 6),
        "latency_norm": round(float(cand["latency_norm"]) - float(base["latency_norm"]), 6),
        "tool_error_rate": round(float(cand["tool_error_rate"]) - float(base["tool_error_rate"]), 6),
        "score": round(cand_score - base_score, 6),
    }

    reasons = []
    if decision == "keep":
        reasons.append("No hard gate violated")
        reasons.append("Candidate score is higher than baseline")
    else:
        if hard_fail_reason:
            reasons.append(f"Triggered {hard_fail_reason}")
        else:
            reasons.append("No hard gate violated, but candidate score is not higher")

    return {
        "decision": decision,
        "note": note,
        "base_score": round(base_score, 6),
        "candidate_score": round(cand_score, 6),
        "deltas": deltas,
        "gate_checks": gate_checks,
        "reasons": reasons,
    }


def append_tsv(path: str, run_id: str, base_score: float, cand_score: float, decision: str, note: str) -> None:
    p = Path(path)
    if not p.exists():
        p.write_text("run_id\tbase_score\tcandidate_score\tdecision\tnotes\n", encoding="utf-8")
    with p.open("a", encoding="utf-8") as f:
        f.write(f"{run_id}\t{base_score:.6f}\t{cand_score:.6f}\t{decision}\t{note}\n")


def render_report(run_id: str, result: dict, base: dict, cand: dict, change_meta: dict | None) -> str:
    change_meta = change_meta or {}
    change_title = change_meta.get("change_title", "(demo run) no real patch metadata provided")
    files_changed = change_meta.get("files_changed", [])
    hypothesis = change_meta.get("hypothesis", "N/A")

    file_lines = "\n".join([f"- `{x}`" for x in files_changed]) if files_changed else "- (not provided)"
    reason_lines = "\n".join([f"- {x}" for x in result["reasons"]])

    return f"""# OpenClaw Agent Autotune Report

## 结论
- run_id: `{run_id}`
- decision: **{result['decision']}**
- note: {result['note']}

## 为什么是这个结论
{reason_lines}

### Gate 检查
- success_drop: {result['gate_checks']['success_drop']['value']} (max {result['gate_checks']['success_drop']['max']}) → {result['gate_checks']['success_drop']['pass']}
- tool_error_rate: {result['gate_checks']['tool_error_rate']['value']} (max {result['gate_checks']['tool_error_rate']['max']}) → {result['gate_checks']['tool_error_rate']['pass']}
- token_cost_increase: {result['gate_checks']['token_cost_increase']['value']} (max {result['gate_checks']['token_cost_increase']['max']}) → {result['gate_checks']['token_cost_increase']['pass']}

## 修改了哪里
- change_title: {change_title}
- hypothesis: {hypothesis}
- files_changed:
{file_lines}

## 修改带来了什么提升
- base_score: {result['base_score']}
- candidate_score: {result['candidate_score']}
- score_delta: {result['deltas']['score']}

### 指标变化（candidate - base）
- success_rate: {result['deltas']['success_rate']}
- token_cost_norm: {result['deltas']['token_cost_norm']}
- latency_norm: {result['deltas']['latency_norm']}
- tool_error_rate: {result['deltas']['tool_error_rate']}

## 原始指标
### baseline
```json
{json.dumps(base, ensure_ascii=False, indent=2)}
```

### candidate
```json
{json.dumps(cand, ensure_ascii=False, indent=2)}
```
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="Base metrics json path")
    ap.add_argument("--candidate", required=True, help="Candidate metrics json path")
    ap.add_argument("--results", default="autotune/results.tsv", help="TSV output path")
    ap.add_argument("--run-id", default=None, help="Run id (default timestamp)")
    ap.add_argument("--change-meta", default=None, help="Optional change metadata json path")
    ap.add_argument("--report-md", default=None, help="Optional markdown report output path")
    args = ap.parse_args()

    base = load(args.base)
    cand = load(args.candidate)
    run_id = args.run_id or datetime.now().strftime("%Y%m%d-%H%M%S")

    result = evaluate(base, cand)
    append_tsv(args.results, run_id, result["base_score"], result["candidate_score"], result["decision"], result["note"])

    change_meta = load(args.change_meta) if args.change_meta else None
    if args.report_md:
        report = render_report(run_id, result, base, cand, change_meta)
        Path(args.report_md).write_text(report, encoding="utf-8")

    output = {
        "run_id": run_id,
        **result,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
