#!/usr/bin/env python3
"""Normalize FracFocus disclosures to monthly completion activity by ticker.

Input : data/DisclosureList_1.csv (one row per hydraulic-fracturing job
        disclosure; primary source: fracfocus.org bulk download)
        tickers.csv (operator-pattern -> ticker with ownership windows,
        so M&A-era activity is credited to the right public company)
Output: data/monthly_by_operator.csv  (month, operator, jobs, water_mgal)
        data/monthly_by_ticker.csv    (month, ticker, jobs, water_mgal)

Month = JobEndDate month (completion date). Disclosure filing lags job end
by ~30-90 days depending on state; the signal must only be "known" with
that lag - documented in README and respected by validate.py.
"""
import pandas as pd
import pathlib

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"

df = pd.read_csv(DATA / "DisclosureList_1.csv",
                 usecols=["JobEndDate", "OperatorName", "StateName",
                          "TotalBaseWaterVolume"])
df["end"] = pd.to_datetime(df["JobEndDate"], errors="coerce")
df = df[(df["end"] >= "2012-01-01") & (df["end"] <= "2026-07-18")]
df["month"] = df["end"].dt.to_period("M")
df["op"] = df["OperatorName"].str.upper().str.strip()
df["water_mgal"] = pd.to_numeric(df["TotalBaseWaterVolume"], errors="coerce") / 1e6

monthly_op = (df.groupby(["month", "op"])
                .agg(jobs=("op", "size"), water_mgal=("water_mgal", "sum"))
                .reset_index())
monthly_op.to_csv(DATA / "monthly_by_operator.csv", index=False)

tickers = pd.read_csv(ROOT / "tickers.csv")
tickers["valid_from"] = pd.PeriodIndex(tickers["valid_from"], freq="M")
tickers["valid_to"] = pd.PeriodIndex(
    tickers["valid_to"].fillna("2026-07"), freq="M")

rows = []
for _, t in tickers.iterrows():
    if not isinstance(t["ticker"], str) or not t["ticker"]:
        continue  # private-window rows
    hit = monthly_op[monthly_op["op"].str.contains(t["operator_pattern"],
                                                  regex=False)]
    hit = hit[(hit["month"] >= t["valid_from"]) & (hit["month"] <= t["valid_to"])]
    hit = hit.assign(ticker=t["ticker"])
    rows.append(hit)

by_ticker = (pd.concat(rows)
               .groupby(["month", "ticker"])
               .agg(jobs=("jobs", "sum"), water_mgal=("water_mgal", "sum"))
               .reset_index())
by_ticker.to_csv(DATA / "monthly_by_ticker.csv", index=False)

print("operators:", monthly_op["op"].nunique(),
      "| ticker rows:", len(by_ticker),
      "| tickers:", by_ticker["ticker"].nunique())
print(by_ticker.groupby("ticker")["jobs"].sum().sort_values(ascending=False)
      .head(15).to_string())
