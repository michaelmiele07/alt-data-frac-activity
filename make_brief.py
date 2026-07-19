#!/usr/bin/env python3
"""Render the one-page investment brief PDF (plain-English companion to the
technical note): premise, mechanism, affected companies, use cases."""
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
    bull=ParagraphStyle("bl", fontName="Helvetica", fontSize=9, leading=11.8,
                        textColor=HexColor(INK2), spaceAfter=2.5,
                        leftIndent=12, bulletIndent=2),
    cell=ParagraphStyle("c", fontName="Helvetica", fontSize=8, leading=10,
                        textColor=HexColor(INK2)),
    cellb=ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=8, leading=10,
                         textColor=HexColor(INK)),
    foot=ParagraphStyle("f", fontName="Helvetica-Oblique", fontSize=7.5,
                        leading=9.5, textColor=HexColor(MUTED)),
)

def bullets(items):
    return [Paragraph(x, S["bull"], bulletText="•") for x in items]

def row(seg, names):
    return [Paragraph(seg, S["cellb"]), Paragraph(names, S["cell"])]

table = Table(
    [row("Majors (shale arms)", "XOM (incl. Pioneer), CVX (incl. Hess, PDC, Noble), COP (incl. Marathon, Concho), OXY (incl. CrownRock), BP"),
     row("Large independents", "EOG, FANG (incl. Endeavor), DVN, EQT, EXE (Chesapeake+Southwestern)"),
     row("Mid-cap E&amp;Ps", "MTDR, PR, SM, CTRA, OVV, CIVI, APA, MUR, HPK"),
     row("Gas-levered", "RRC, AR, CRK, EQT, EXE — completion momentum maps to gas macro"),
     row("Second-order reads", "Pressure pumpers &amp; sand: HAL, SLB, LBRT — aggregate completion count is their demand pool")],
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
        "or more before the production reaches a 10-Q. Counting disclosures per operator gives a field-level read on "
        "who is accelerating and who is quietly slowing, from a free public database refreshed continuously.", S["body"]),

    Paragraph("The mechanism — and what the test showed", S["h"]),
    *bullets([
        "Completions mechanically lead first production by roughly a quarter; water volume proxies job intensity "
        "(bigger fracks, longer laterals).",
        "The operator→ticker map uses <b>M&amp;A ownership windows</b> — Pioneer counts as XOM only after the deal "
        "closed, Marathon flips to COP in Nov 2024 — so activity is never miscredited.",
        "Measured limit: naive return ranking is a <b>null</b> (−0.66%/qtr, p=0.80), and the test is survivorship-"
        "biased <i>against</i> success — ten of twelve excluded tickers were taken out <i>after outperforming</i> "
        "(PXD, HES, MRO).",
        "Activity growth is not automatically value creation in shale; the natural product is production-surprise "
        "forecasting, not a long-short ranking.",
    ]),

    Paragraph("The investable universe", S["h"]),
    table,

    Paragraph("How an investor would use it", S["h"]),
    *bullets([
        "<b>Production-surprise watchlist:</b> operators whose completion count accelerates ahead of consensus. "
        "Current board (2026Q2 YoY, partial data): <b>RRC +67%, MTDR +20%, DVN +20%</b> — pre-registered September "
        "re-check, then against Q3 production prints.",
        "<b>Capex-discipline monitor:</b> for majors, the shale-arm completion count shows whether announced "
        "discipline is real in the field (XOM −63% and EOG −89% are partly filing lag; September resolves them).",
        "<b>Service-demand read-through:</b> the aggregate completion count is the quarterly demand pool for "
        "pressure pumpers (HAL, LBRT).",
        "<b>M&amp;A tell:</b> 2024's marquee take-outs hid in plain sight — in 2023 Endeavor was the <b>#10 "
        "completer of 496 operators</b> and CrownRock's CrownQuest <b>#18</b>, both private. Today's equivalents on "
        "that screen: Mewbourne (#8), BlackBeard (#9).",
    ]),

    Paragraph("What could mislead you", S["h"]),
    *bullets([
        "Filings lag job completion by 30–90 days — never trade the raw latest print.",
        "Gas-basin and oil-basin economics diverge; water volume is an intensity proxy, not EUR.",
        "The return null is real: this is an operational nowcast, not a priced anomaly.",
    ]),

    HRFlowable(width="100%", thickness=0.7, color=HexColor(RULE), spaceBefore=5, spaceAfter=4),
    Paragraph("Data: FracFocus Chemical Disclosure Registry bulk export, 248K disclosures 2012–July 2026. "
              "Methodology and validation: out/frac_activity_note.pdf. Research, not investment advice.", S["foot"]),
]
doc.build(story)
print("wrote", OUT / "frac_investment_brief.pdf")
