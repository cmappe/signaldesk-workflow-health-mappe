#!/usr/bin/env python3
"""Generate a compact, reproducible weekly health check for SignalDesk."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path


COUNT_FIELDS = ("sessions", "completed", "accepted_output", "flagged_for_review")


def load_and_clean(path: Path) -> tuple[list[dict], list[str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    issues: list[str] = []
    seen: set[tuple] = set()
    cleaned: list[dict] = []
    for raw in rows:
        row = dict(raw)
        row["team"] = row["team"].strip().title()
        for field in COUNT_FIELDS:
            row[field] = int(row[field])
        for field in ("avg_minutes_saved", "median_confidence", "user_rating"):
            try:
                row[field] = float(row[field])
            except (TypeError, ValueError):
                row[field] = None

        # Exclude exact metric duplicates even if their note differs.
        key = tuple(row[field] for field in row if field != "notes")
        if key in seen:
            issues.append(f"Removed duplicate metric row: {row['date']} / {row['workflow']} / {row['source']}.")
            continue
        seen.add(key)
        cleaned.append(row)

    if len({r["team"] for r in rows}) != len({r["team"] for r in cleaned}):
        issues.append("Normalized team labels case-insensitively (for example, product → Product).")
    missing_conf = sum(r["median_confidence"] is None for r in cleaned)
    if missing_conf:
        issues.append(f"Treated {missing_conf} non-numeric confidence value(s) as missing.")
    return cleaned, issues


def aggregate(rows: list[dict]) -> dict:
    totals = {field: sum(r[field] for r in rows) for field in COUNT_FIELDS}
    completed = totals["completed"]
    sessions = totals["sessions"]
    totals["completion_rate"] = completed / sessions if sessions else 0
    totals["acceptance_rate"] = totals["accepted_output"] / completed if completed else 0
    totals["review_rate"] = totals["flagged_for_review"] / completed if completed else 0
    totals["minutes_saved"] = sum(r["avg_minutes_saved"] * r["completed"] for r in rows)
    return totals


def pct(value: float) -> str:
    return f"{value:.1%}"


def pp(after: float, before: float) -> str:
    delta = 100 * (after - before)
    return f"{delta:+.1f} pp"


def build_report(rows: list[dict], issues: list[str], source: str) -> str:
    by_workflow: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_workflow[row["workflow"]].append(row)

    # The demo traffic is real activity but not representative product usage.
    representative = [r for r in rows if "demo account" not in r["notes"].lower()]
    dates = sorted({r["date"] for r in rows})
    expected_pairs = {(r["workflow"], r["source"]) for r in rows if r["date"] != dates[-1]}
    last_pairs = {(r["workflow"], r["source"]) for r in rows if r["date"] == dates[-1]}
    missing_pairs = sorted(expected_pairs - last_pairs)

    lines = [
        "# SignalDesk weekly health check",
        "",
        f"**Window:** {dates[0]} to {dates[-1]}  ",
        f"**Source:** `{source}`  ",
        "**Decision:** Keep Lead summary as the best current expansion candidate; investigate Reply draft before broader rollout.",
        "",
        "## Workflow scorecard",
        "",
        "Rates use completed outputs as the denominator for acceptance and review. Minutes saved are directional estimates.",
        "",
        "| Workflow | Sessions | Completion | Acceptance | Review | Est. hours saved |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for workflow in sorted(by_workflow):
        metric_rows = [r for r in representative if r["workflow"] == workflow]
        m = aggregate(metric_rows)
        lines.append(
            f"| {workflow} | {m['sessions']:,} | {pct(m['completion_rate'])} | "
            f"{pct(m['acceptance_rate'])} | {pct(m['review_rate'])} | {m['minutes_saved']/60:.1f} |"
        )

    lines += ["", "## What changed after the August 4 prompt launch", ""]
    for workflow in sorted(by_workflow):
        relevant = [r for r in representative if r["workflow"] == workflow and r["date"] != dates[-1]]
        before = aggregate([r for r in relevant if r["date"] < "2026-08-04"])
        after = aggregate([r for r in relevant if r["date"] >= "2026-08-04"])
        lines.append(
            f"- **{workflow}:** acceptance {pp(after['acceptance_rate'], before['acceptance_rate'])}; "
            f"review {pp(after['review_rate'], before['review_rate'])}."
        )

    lines += [
        "",
        "This is a directional pre/post comparison, not a causal estimate: the window is short, traffic mix changed, and no control group is available.",
        "",
        "## Investigate next",
        "",
        "1. **Reply draft on August 7:** completion and acceptance fell while review flags rose, despite confidence increasing. This is consistent with the noted mid-day review-policy change and shows why confidence should not be treated as quality.",
        "2. **Instrument prompt and policy versions explicitly:** notes are not reliable experiment fields. Add version IDs and separate user-, policy-, and automated-review flags.",
        "3. **Validate the time-saved estimate:** Feedback clustering leads estimated hours saved, but its samples are small and the metric is self-reported/directional.",
        "",
        "## Data-quality warnings",
        "",
    ]
    lines.extend(f"- {issue}" for issue in issues)
    lines.append("- Excluded the August 5 Lead summary demo-account spike from comparative metrics; it remains in the source data.")
    if missing_pairs:
        pairs = ", ".join(f"{w} / {s}" for w, s in missing_pairs)
        lines.append(f"- Final-day coverage is incomplete; missing expected pairs: {pairs}.")
    lines += [
        "",
        "## Metric trust",
        "",
        "Trust **model confidence least**: it is self-reported, has a missing value, and moves opposite observed outcomes for Reply draft on August 7. Acceptance and review are more actionable but still policy- and behavior-dependent.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="Path to product_usage_events.csv")
    parser.add_argument("--output", type=Path, help="Write Markdown here (otherwise print to stdout)")
    args = parser.parse_args()
    rows, issues = load_and_clean(args.csv)
    report = build_report(rows, issues, args.csv.name)
    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
