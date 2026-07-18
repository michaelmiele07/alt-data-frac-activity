#!/usr/bin/env python3
"""Render the ~1.5 page research note PDF (house style of prior notes)."""
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Image,
                                HRFlowable)

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out"
INK, INK2, MUTED, RULE = "#0b0b0b", "#3d3c39", "#6b6a66", "#c3c2b7"

# ---- figure: 2026Q2 YoY completion growth ranking
q = pd.read_csv(OUT / "quarterly_signal.csv")
latest = q[(q["quarter"] == "2026Q2") & (q["jobs"] >= 10)].dropna(subset=["jobs_yoy"])
latest = latest.sort_values("jobs_yoy")
fig, ax = plt.subplots(figsize=(6.6, 2.6), dpi=200)
colors = ["#a03828" if v < 0 else "#2d5f3e" for v in latest["jobs_yoy"]]
ax.barh(latest["ticker"], latest["jobs_yoy"] * 100, color=colors, height=0.65)
ax.axvline(0, color="#0b0b0b", lw=0.7)
ax.set_xlabel("frack jobs completed, 2026Q2 vs 2025Q2 (% YoY)", fontsize=7)
ax.tick_params(labelsize=6.5)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(OUT / "figure1.png", bbox_inches="tight")

S = dict(
    title=ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=15, leading=18,
                         textColor=HexColor(INK), spaceAfter=2),
    sub=ParagraphStyle("s", fontName="Helvetica", fontSize=8.5, leading=11,
                       textColor=HexColor(MUTED), spaceAfter=8),
    h=ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10, leading=13,
                     textColor=HexColor(INK), spaceBefore=9, spaceAfter=3),
    body=ParagraphStyle("b", fontName="Helvetica", fontSize=9, leading=12.3,
                        textColor=HexColor(INK2), spaceAfter=5),
    foot=ParagraphStyle("f", fontName="Helvetica-Oblique", fontSize=7.5,
                        leading=9.5, textColor=HexColor(MUTED)),
)

doc = SimpleDocTemplate(str(OUT / "frac_activity_note.pdf"),
                        pagesize=letter, leftMargin=0.85 * inch,
                        rightMargin=0.85 * inch, topMargin=0.7 * inch,
                        bottomMargin=0.65 * inch)
story = [
    Paragraph("Completion Velocity: FracFocus Disclosures as an Operator-Level "
              "Activity Signal for Shale E&amp;Ps", S["title"]),
    Paragraph("Alt-data research note &nbsp;·&nbsp; Michael Miele &nbsp;·&nbsp; "
              "July 18, 2026 &nbsp;·&nbsp; FracFocus registry through July 13, "
              "2026 (248K disclosures)", S["sub"]),
    HRFlowable(width="100%", thickness=0.7, color=HexColor(RULE), spaceAfter=8),

    Paragraph("Data and signal construction", S["h"]),
    Paragraph(
        "Every hydraulic-fracturing job in the US must be disclosed to the FracFocus registry with operator, well, "
        "job dates, and base-water volume. I normalized the full bulk export — <b>248K disclosures, 2012–present, "
        "2,035 operators</b> — to monthly completion counts and water volumes per operator, then mapped operators to "
        "32 listed tickers using <b>ownership windows</b> so M&amp;A never miscredits activity: Pioneer counts as PXD "
        "until April 2024 and as XOM after; Endeavor is private until Diamondback closes; Marathon→COP, Hess/PDC/"
        "Noble→CVX, Chesapeake+Southwestern→EXE, CrownRock→OXY each switch at deal close. The signal is quarterly "
        "YoY growth in completed jobs per ticker. Completions lead first production by roughly a quarter, so "
        "operator-level completion acceleration is a candidate leading indicator for reported production and capex. "
        "Key friction, respected throughout: disclosures are <i>filed</i> 30–90 days after job end, so the most "
        "recent quarter is always partially visible.", S["body"]),
    Image(str(OUT / "figure1.png"), width=6.4 * inch, height=2.52 * inch),

    Paragraph("Pre-committed return test: an honest null, with a named bias", S["h"]),
    Paragraph(
        "Cross-sectional tertile test over 45 quarters (2015Q1–2026Q1, ≥6 names/quarter): rank by jobs YoY growth, "
        "hold months 2–4 after quarter end (when filings are complete). Result: <b>−0.66%/quarter top-minus-bottom, "
        "permutation p = 0.80</b> — no return predictability. Two disclosed limitations: (1) <b>survivorship</b> — "
        "Yahoo lacks history for 12 tickers, ten of them delisted via takeover <i>after outperforming</i> (PXD, HES, "
        "MRO…), which biases the test toward null; (2) in shale, activity growth is not value creation — completion "
        "acceleration can be capital-destructive, so the natural use is production-surprise forecasting, not raw "
        "return ranking.", S["body"]),

    Paragraph("Current board and pre-registered check", S["h"]),
    Paragraph(
        "2026Q2 completion momentum (partial data): <b>Range Resources +67%, Matador +20%, Devon +20% YoY</b> against "
        "broad declines elsewhere (EOG −89% and XOM −63% are partly filing-lag artifacts). <b>Check in September "
        "2026</b>, when Q2 filings are complete: (1) does the RRC/MTDR/DVN acceleration survive final data? "
        "(2) do their Q3 production prints beat consensus? Logged before either is knowable.", S["body"]),

    HRFlowable(width="100%", thickness=0.7, color=HexColor(RULE),
               spaceBefore=6, spaceAfter=4),
    Paragraph("Pipeline: github.com/michaelmiele07/alt-data-frac-activity — fetch → normalize (ownership windows) → "
              "quarterly signal → permutation validation. FracFocus data is public. Research, not investment advice. "
              "Third entry in a regulatory-exhaust series (NHTSA complaints, CFPB complaints, FracFocus "
              "disclosures).", S["foot"]),
]
doc.build(story)
print("wrote", OUT / "frac_activity_note.pdf")
