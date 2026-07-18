#!/usr/bin/env python3
"""Validation: does quarterly completion-activity growth predict next-quarter
stock returns? Cross-sectional tertile spread + permutation test.

Design (pre-committed before looking at results):
- Signal: jobs YoY growth for quarter Q, per ticker (min 10 jobs).
- Return: ticker total return over the quarter Q+1 shifted one month late
  (i.e. months 2-4 after Q ends) so the signal was actually observable -
  FracFocus filings lag job end by 30-90 days.
- Spread: mean return of top tertile minus bottom tertile, averaged over
  all quarters 2015Q1-2026Q1.
- Test: 2000 permutations shuffling signal ranks within quarter.

Survivorship caveat (disclosed, not hidden): Yahoo Finance lacks history
for delisted tickers (PXD, MRO, CLR, SWN, XEC, CPE, CHK, HES, PDCE, CXO),
so those names drop out of the return test even where the signal exists.
"""
import numpy as np
import pandas as pd
import pathlib

import yfinance as yf

ROOT = pathlib.Path(__file__).parent
q = pd.read_csv(ROOT / "out" / "quarterly_signal.csv")
q["quarter"] = pd.PeriodIndex(q["quarter"], freq="Q")
q = q.dropna(subset=["jobs_yoy"])
q = q[(q["jobs"] >= 10) & (q["quarter"] >= "2015Q1") & (q["quarter"] <= "2026Q1")]

tickers = sorted(q["ticker"].unique())
px = yf.download(tickers, start="2014-06-01", end="2026-07-17",
                 progress=False, auto_adjust=True)["Close"]
got = [t for t in tickers if t in px.columns and px[t].notna().sum() > 100]
missing = sorted(set(tickers) - set(got))
print(f"prices for {len(got)}/{len(tickers)} tickers; missing (survivorship): {missing}")

monthly = px[got].resample("ME").last()

def fwd_return(ticker, quarter):
    """Total return over months 2-4 after quarter end (signal observable)."""
    end = quarter.end_time
    try:
        s = monthly[ticker]
    except KeyError:
        return np.nan
    window = s[s.index > end]
    if len(window) < 4 or pd.isna(window.iloc[0]) or pd.isna(window.iloc[3]):
        return np.nan
    return window.iloc[3] / window.iloc[0] - 1

q = q[q["ticker"].isin(got)].copy()
q["fwd_ret"] = [fwd_return(t, qu) for t, qu in zip(q["ticker"], q["quarter"])]
q = q.dropna(subset=["fwd_ret"])

spreads = []
rows = []
for qu, g in q.groupby("quarter"):
    if len(g) < 6:
        continue
    g = g.sort_values("jobs_yoy")
    k = len(g) // 3
    lo, hi = g.head(k), g.tail(k)
    spreads.append(hi["fwd_ret"].mean() - lo["fwd_ret"].mean())
    rows.append((str(qu), len(g), spreads[-1]))

obs = float(np.mean(spreads))
rng = np.random.default_rng(42)
perm = []
for _ in range(2000):
    ps = []
    for qu, g in q.groupby("quarter"):
        if len(g) < 6:
            continue
        r = g["fwd_ret"].to_numpy(copy=True)
        rng.shuffle(r)
        k = len(g) // 3
        ps.append(r[-k:].mean() - r[:k].mean())
    perm.append(np.mean(ps))
perm = np.asarray(perm)
p = float((np.abs(perm) >= abs(obs)).mean())

report = [
    f"quarters tested: {len(spreads)}  (2015Q1-2026Q1, >=6 names/quarter)",
    f"mean top-minus-bottom tertile fwd return (months 2-4): {obs:+.2%}/quarter",
    f"two-sided permutation p-value (2000 shuffles within quarter): {p:.3f}",
    f"survivorship: {len(missing)} delisted tickers excluded: {missing}",
]
print("\n".join(report))
pd.DataFrame(rows, columns=["quarter", "names", "spread"]) \
    .to_csv(ROOT / "out" / "validation_spreads.csv", index=False)
(ROOT / "out" / "validation_result.txt").write_text("\n".join(report) + "\n")
