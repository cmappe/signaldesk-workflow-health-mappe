# AI Use Note

I used Codex as a coding and analysis partner, but I directed the scope and decided what the final artifact needed to accomplish.

I chose to focus the work on a practical product decision: which workflow looks strongest, what looks suspicious, and what the team should investigate before expanding usage. I kept the project centered on one weekly health check instead of turning it into a large analytics system.

I challenged outputs that did not help answer that question. A daily bar chart showed movement but did not explain why the differences mattered, so I replaced it with a before-and-after prompt comparison that shows exact changes and limitations. I also decided that August 7 should not be included in that comparison because coverage is incomplete and the Reply draft review policy changed mid-day.

Codex helped inspect the data, draft cleaning logic, calculate metrics, build the interface, and identify test cases. I checked the suspicious records against the raw CSV and decided how to handle the duplicate row, demo-account spike, missing confidence value, and inconsistent team label. I also required acceptance and review rates to use completed outputs as their denominator.

I treated model confidence and estimated time saved cautiously rather than presenting them as ground truth. I kept the causal limitation visible because the window is short, traffic changed, and there is no control group.

AI accelerated the implementation, but I made the framing, metric, trust, and product decisions.
