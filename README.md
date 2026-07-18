# FracFocus Completion Activity → E&P Operator Signal

Quarterly hydraulic-fracturing completion activity per public E&P operator,
built from the FracFocus Chemical Disclosure Registry bulk export (248k
disclosures, 2012–present). Completions lead first production by roughly a
quarter, so operator-level completion acceleration is a candidate leading
indicator for reported production and capex.

## Pipeline

| step | script | output |
|---|---|---|
| fetch | `fetch.py` | `data/DisclosureList_1.csv` (61 MB, not committed) |
| normalize | `normalize.py` + `tickers.csv` | monthly jobs + base-water volume by operator and by ticker |
| signal | `build_signal.py` | quarterly YoY completion growth per ticker |
| validate | `validate.py` | cross-sectional forward-return test, permutation p-value |

## M&A handled with ownership windows

`tickers.csv` maps operator names to tickers **with validity windows**, so
Pioneer counts as PXD until Apr-2024 and as XOM after; Endeavor is private
until FANG closes Sep-2024; Marathon → COP Nov-2024; Hess/PDC/Noble → CVX;
Chesapeake + Southwestern → EXE; CrownRock → OXY. Activity is never credited
to an owner before the deal closed.

## Honest null on returns

Pre-committed test (45 quarters 2015Q1–2026Q1, ≥6 names/quarter): tertile
spread on quarterly jobs YoY growth vs forward-quarter return taken at
months 2–4 after quarter end (respecting the 30–90 day disclosure filing
lag): **−0.66%/quarter, permutation p = 0.80 — no return predictability.**

Two disclosed limitations that could mask a real effect:

- **Survivorship:** Yahoo lacks history for 12 tickers (10 delisted via
  M&A — often *after outperformance*, e.g. PXD, HES, MRO — plus CTRA/CIVI
  query failures). Winners exiting the sample biases the test toward null.
- **Completion growth ≠ value creation:** in shale, activity growth can be
  capital-destructive; the signal may be better used for production-surprise
  forecasting than raw return ranking.

## What the signal is still good for

`out/latest_signal.txt` ranks 2026Q2 completion momentum (RRC +67%, MTDR
+20%, DVN +20% YoY vs EOG −89%, XOM −63% — the latter partly filing lag).
The defensible product is a **production-surprise watchlist**: completion
acceleration that consensus hasn't picked up. Testing signal vs reported
quarterly production (from 10-Qs) is the natural next step and is listed as
future work rather than claimed.

## Pre-registered check (September 2026)

FracFocus filings for 2026Q2 finish arriving by ~September. Re-run
`build_signal.py` then and check: (1) does the RRC/MTDR/DVN acceleration
survive complete data? (2) do their Q3 production prints beat consensus?

Data: FracFocus bulk download is public. This is research, not investment
advice.
