#!/usr/bin/env python3
"""Compute OpenClaw autotune score from metrics JSON.

Input JSON example:
{
  "success_rate": 0.82,
  "token_cost_norm": 0.44,
  "latency_norm": 0.31,
  "tool_error_rate": 0.00
}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def compute_score(m: dict) -> float:
    return (
        0.55 * float(m["success_rate"])
        - 0.20 * float(m["token_cost_norm"])
        - 0.15 * float(m["latency_norm"])
        - 0.10 * float(m["tool_error_rate"])
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("metrics", help="Path to metrics json")
    args = ap.parse_args()

    data = json.loads(Path(args.metrics).read_text(encoding="utf-8"))
    score = compute_score(data)
    print(f"score={score:.6f}")


if __name__ == "__main__":
    main()
