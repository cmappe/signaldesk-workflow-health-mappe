# SignalDesk weekly health check

**Window:** 2026-08-01 to 2026-08-07  
**Source:** `product_usage_events.csv`  
**Decision:** Keep Lead summary as the best current expansion candidate; investigate Reply draft before broader rollout.

## Workflow scorecard

Rates use completed outputs as the denominator for acceptance and review. Minutes saved are directional estimates.

| Workflow | Sessions | Completion | Acceptance | Review | Est. hours saved |
|---|---:|---:|---:|---:|---:|
| Feedback clustering | 207 | 66.7% | 65.9% | 18.8% | 29.9 |
| Lead summary | 450 | 77.8% | 78.0% | 9.7% | 46.5 |
| Reply draft | 510 | 80.6% | 75.7% | 16.8% | 26.9 |

## What changed after the August 4 prompt launch

- **Feedback clustering:** acceptance -1.0 pp; review -2.1 pp.
- **Lead summary:** acceptance +1.0 pp; review -1.5 pp.
- **Reply draft:** acceptance +0.2 pp; review +2.2 pp.

This is a directional pre/post comparison, not a causal estimate: the window is short, traffic mix changed, and no control group is available.

## Investigate next

1. **Reply draft on August 7:** completion and acceptance fell while review flags rose, despite confidence increasing. This is consistent with the noted mid-day review-policy change and shows why confidence should not be treated as quality.
2. **Instrument prompt and policy versions explicitly:** notes are not reliable experiment fields. Add version IDs and separate user-, policy-, and automated-review flags.
3. **Validate the time-saved estimate:** Feedback clustering leads estimated hours saved, but its samples are small and the metric is self-reported/directional.

## Data-quality warnings

- Removed duplicate metric row: 2026-08-05 / Lead summary / email.
- Normalized team labels case-insensitively (for example, product → Product).
- Treated 1 non-numeric confidence value(s) as missing.
- Excluded the August 5 Lead summary demo-account spike from comparative metrics; it remains in the source data.
- Final-day coverage is incomplete; missing expected pairs: Lead summary / manual, Reply draft / manual.

## Metric trust

Trust **model confidence least**: it is self-reported, has a missing value, and moves opposite observed outcomes for Reply draft on August 7. Acceptance and review are more actionable but still policy- and behavior-dependent.
