# SignalDesk Weekly Health Check

**Track A — Fictional Domain Packet**

I built a small web app to help a SignalDesk product teammate answer three questions: what is working, what looks suspicious, and what should we investigate next?

The dashboard compares the three workflows, highlights the biggest concern, and shows the data-quality issues that affect how much we should trust the results. I also included a dependency-free Python script that cleans the provided CSV and reproduces the metrics in `REPORT.md`.

## Run the analysis

Requires Python 3.9+ with no third-party packages.

```bash
python3 health_check.py data/product_usage_events.csv --output REPORT.md
python3 -m unittest -v
```

## Run the dashboard

Requires Node.js 22.13+ and pnpm.

```bash
cd webapp
pnpm install
pnpm run dev
```

## Decisions I made

- Acceptance and review rates use completed outputs as the denominator.
- I removed the duplicate row and normalized inconsistent team casing.
- I kept the demo spike in the raw data but excluded it from comparisons.
- I treated estimated time saved as directional, not verified impact.
- I excluded August 7 from the prompt comparison because coverage is incomplete and the Reply draft review policy changed mid-day.

The data also contains a missing confidence value and small samples. The pre/post comparison is useful for deciding what to investigate, but it is not causal.

With more time, I would add explicit prompt and policy version fields, separate review reasons, validate time-saved estimates, and analyze several complete weeks.
