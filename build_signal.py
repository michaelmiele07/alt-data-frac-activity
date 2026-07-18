#!/usr/bin/env python3
"""Completion-activity signal: quarterly YoY change in frack jobs by ticker.

Output: out/quarterly_signal.csv (ticker, quarter, jobs, jobs_yoy, water_yoy)
        out/latest_signal.txt    (current-quarter ranking, human-readable)

Interpretation: completions lead first production by roughly one quarter
(well is turned in line weeks-to-months after frack job ends), so completion
acceleration should show up in reported production/capex next quarter.
"""
import pandas as pd
import pathlib

ROOT = pathlib.Path(__file__).parent
by_ticker = pd.read_csv(ROOT / "data" / "monthly_by_ticker.csv")
by_ticker["month"] = pd.PeriodIndex(by_ticker["month"], freq="M")
by_ticker["quarter"] = by_ticker["month"].dt.asfreq("Q")

q = (by_ticker.groupby(["ticker", "quarter"])
       .agg(jobs=("jobs", "sum"), water_mgal=("water_mgal", "sum"))
       .reset_index()
       .sort_values(["ticker", "quarter"]))

q["jobs_yoy"] = q.groupby("ticker")["jobs"].pct_change(4)
q["water_yoy"] = q.groupby("ticker")["water_mgal"].pct_change(4)

out = ROOT / "out"
out.mkdir(exist_ok=True)
q.to_csv(out / "quarterly_signal.csv", index=False)

# Latest complete quarter: 2026Q2 (Q3 is 18 days old and disclosure-lagged).
latest = q[q["quarter"] == "2026Q2"].dropna(subset=["jobs_yoy"])
latest = latest[latest["jobs"] >= 10]  # min activity to rank
lines = ["Completion activity, 2026Q2 vs 2025Q2 (min 10 jobs/quarter)",
         "NOTE: FracFocus filings lag job end by 30-90 days; 2026Q2 may still",
         "be incomplete for slow-filing states. Re-run in September for final.",
         ""]
for _, r in latest.sort_values("jobs_yoy", ascending=False).iterrows():
    lines.append(f"{r['ticker']:>5}  jobs {r['jobs']:>4.0f}  "
                 f"YoY {r['jobs_yoy']:+7.1%}  water YoY "
                 f"{r['water_yoy']:+7.1%}" if pd.notna(r['water_yoy'])
                 else f"{r['ticker']:>5}  jobs {r['jobs']:>4.0f}  YoY {r['jobs_yoy']:+7.1%}")
(out / "latest_signal.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
