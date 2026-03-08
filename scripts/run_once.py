#!/usr/bin/env python3
"""Single-run decision helper for OpenClaw Agent Autotune.

Compares base vs candidate metrics and prints keep/rollback based on:
- weighted score improvement
- hard fail gates
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


def decide(base: dict, cand: dict) -> tuple[str, str, float, float]:
    base_score = compute_score(base)
    cand_score = compute_score(cand)

    success_drop = float(base["success_rate"]) - float(cand["success_rate"])
    token_increase = float(cand["token_cost_norm"]) - float(base["token_cost_norm"])
    tool_error = float(cand["tool_error_rate"])

    if success_drop > HARD_GATES["success_drop_max"]:
        return "rollback", "hard_gate: success_rate dropped >2%", base_score, cand_score
    if tool_error > HARD_GATES["tool_error_max"]:
        return "rollback", "hard_gate: tool_error_rate > 0", base_score, cand_score
    if token_increase > HARD_GATES["token_increase_max"]:
        return "rollback", "hard_gate: token_cost increase >20%", base_score, cand_score

    if cand_score > base_score:
        return "keep", "score improved", base_score, cand_score
    return "rollback", "score not improved", base_score, cand_score


def append_tsv(path: str, run_id: str, base_score: float, cand_score: float, decision: str, note: str) -> None:
    p = Path(path)
    if not p.exists():
        p.write_text("run_id\tbase_score\tcandidate_score\tdecision\tnotes\n", encoding="utf-8")
    with p.open("a", encoding="utf-8") as f:
        f.write(f"{run_id}\t{base_score:.6f}\t{cand_score:.6f}\t{decision}\t{note}\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="Base metrics json path")
    ap.add_argument("--candidate", required=True, help="Candidate metrics json path")
    ap.add_argument("--results", default="autotune/results.tsv", help="TSV output path")
    ap.add_argument("--run-id", default=None, help="Run id (default timestamp)")
    args = ap.parse_args()

    base = load(args.base)
    cand = load(args.candidate)
    decision, note, base_score, cand_score = decide(base, cand)

    run_id = args.run_id or datetime.now().strftime("%Y%m%d-%H%M%S")
    append_tsv(args.results, run_id, base_score, cand_score, decision, note)

    print(json.dumps({
        "run_id": run_id,
        "base_score": round(base_score, 6),
        "candidate_score": round(cand_score, 6),
        "decision": decision,
        "note": note,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
