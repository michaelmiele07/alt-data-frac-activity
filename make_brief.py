#!/usr/bin/env python3
"""Render the one-page investment brief PDF (plain-English companion to the
technical note): idea, theory, affected companies, investment angle."""
import pathlib

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, HRFlowable,
                                Table, TableStyle)

OUT = pathlib.Path(__file__).parent / "out"
INK, INK2, MUTED, RULE = "#0b0b0b", "#3d3c39", "#6b6a66", "#c3c2b7"

S = dict(
    title=ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=14.5, leading=17,
                         textColor=HexColor(INK), spaceAfter=2),
    sub=ParagraphStyle("s", fontName="Helvetica", fontSize=8.5, leading=11,
                       textColor=HexColor(MUTED), spaceAfter=7),
    h=ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10, leading=13,
                     textColor=HexColor(INK), spaceBefore=8, spaceAfter=3),
    body=ParagraphStyle("b", fontName="Helvetica", fontSize=9, leading=12.1,
                        textColor=HexColor(INK2), spaceAfter=4),
    cell=ParagraphStyle("c", fontName="Helvetica", fontSize=8, leading=10,
                        textColor=HexColor(INK2)),
    cellb=ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=8, leading=10,
                         textColor=HexColor(INK)),
    foot=ParagraphStyle("f", fontName="Helvetica-Oblique", fontSize=7.5,
                        leading=9.5, textColor=HexColor(MUTED)),
)

def row(seg, names):
    return [Paragraph(seg, S["cellb"]), Paragraph(names, S["cell"])]

table = Table(
    [row("Majors (shale arms)", "XOM (incl. Pioneer), CVX (incl. Hess, PDC, Noble), COP (incl. Marathon, Concho), OXY (incl. CrownRock), BP"),
     row("Large independents", "EOG, FANG (incl. Endeavor), DVN, EQT, EXE (Chesapeake+Southwestern)"),
     row("Mid-cap E&amp;Ps", "MTDR, PR, SM, CTRA, OVV, CIVI, APA, MUR, HPK"),
     row("Gas-levered", "RRC, AR, CRK, EQT, EXE — completion momentum maps to gas macro"),
     row("Second-order reads", "Pressure pumpers &amp; sand: HAL, SLB, LBRT — aggregate completion count is their demand; midstream volumes follow completions by basin")],
    colWidths=[1.35 * inch, 5.25 * inch])
table.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LINEBELOW", (0, 0), (-1, -2), 0.4, HexColor("#e2e1d8")),
    ("TOPPADDING", (0, 0), (-1, -1), 2.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
]))

doc = SimpleDocTemplate(str(OUT / "frac_investment_brief.pdf"),
                        pagesize=letter, leftMargin=0.85 * inch,
                        rightMargin=0.85 * inch, topMargin=0.7 * inch,
                        bottomMargin=0.65 * inch)
story = [
    Paragraph("Reading the Field: Fracturing Disclosures as a Leading Indicator for Shale Producers", S["title"]),
    Paragraph("Investment brief &nbsp;·&nbsp; Michael Miele &nbsp;·&nbsp; July 18, 2026 &nbsp;·&nbsp; "
              "companion to the technical note &nbsp;·&nbsp; github.com/michaelmiele07/alt-data-frac-activity", S["sub"]),
    HRFlowable(width="100%", thickness=0.7, color=HexColor(RULE), spaceAfter=7),

    Paragraph("The premise", S["h"]),
    Paragraph(
        "US law requires every hydraulic-fracturing job to be disclosed to the FracFocus registry — operator, well, "
        "dates, water volume. A frack job is the last capital step before a well produces, and it happens a quarter "
        "or more before the production shows up in a 10-Q. Counting disclosures per operator therefore gives a "
        "field-level read on who is accelerating and who is quietly slowing, weeks-to-months before guidance "
        "updates, from a free public database refreshed continuously.", S["body"]),

    Paragraph("The mechanism — and what the test showed", S["h"]),
    Paragraph(
        "Completions mechanically lead first production; water volume proxies job intensity (bigger fracks, longer "
        "laterals). The map to tickers uses <b>M&amp;A ownership windows</b> so Pioneer's activity counts as XOM only "
        "after the deal closed, Marathon flips to COP in Nov 2024, and so on — activity is never miscredited. Honest "
        "boundary: the pre-committed test of naive return ranking is a <b>null</b> (−0.66%/qtr, p=0.80), and it is "
        "survivorship-biased against success — ten of the twelve excluded tickers were taken out <i>after "
        "outperforming</i> (PXD, HES, MRO). Activity growth also isn't automatically value creation in shale; the "
        "signal's natural product is production-surprise forecasting, not a long-short ranking.", S["body"]),

    Paragraph("The investable universe", S["h"]),
    table,

    Paragraph("How an investor would use it", S["h"]),
    Paragraph(
        "(1) <b>Production-surprise watchlist:</b> operators whose completion count accelerates ahead of consensus "
        "models. Current board (2026Q2 vs 2025Q2, partial data): <b>RRC +67%, MTDR +20%, DVN +20%</b> against broad "
        "declines — pre-registered check in September when filings complete, then against Q3 production prints. "
        "(2) <b>Capex discipline monitor:</b> for majors, the shale-arm completion count is a direct read on whether "
        "announced discipline is real in the field (XOM −63% and EOG −89% YoY are partly filing lag — the September "
        "re-run resolves them). (3) <b>Service-demand read-through:</b> the aggregate completion count is the "
        "addressable market for pressure pumpers (HAL, LBRT) each quarter. (4) <b>M&amp;A tell:</b> the same data ranks private operators, and 2024's "
        "two marquee take-outs were hiding in plain sight: in 2023 Endeavor was the <b>#10 completer in the country</b> "
        "and CrownRock's CrownQuest operator <b>#18 of 496</b> — both private. Today's equivalents on that screen: "
        "Mewbourne (#8 in 2023) and BlackBeard (#9).", S["body"]),

    Paragraph("What could mislead you", S["h"]),
    Paragraph(
        "Filings lag job completion by 30–90 days, so the newest quarter is always partial — never trade the raw "
        "latest print. Gas-basin and oil-basin economics diverge; water volume is an intensity proxy, not EUR. The "
        "return null is real: this is an operational nowcast, not a priced anomaly. Not investment advice.", S["body"]),

    HRFlowable(width="100%", thickness=0.7, color=HexColor(RULE), spaceBefore=5, spaceAfter=4),
    Paragraph("Data: FracFocus Chemical Disclosure Registry bulk export, 248K disclosures 2012–July 2026. "
              "Methodology and validation in the technical note (out/frac_activity_note.pdf).", S["foot"]),
]
doc.build(story)
print("wrote", OUT / "frac_investment_brief.pdf")
