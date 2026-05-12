from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────────
section = doc.sections[0]
section.top_margin    = Cm(2.0)
section.bottom_margin = Cm(2.0)
section.left_margin   = Cm(2.5)
section.right_margin  = Cm(2.5)

# ── Helpers ───────────────────────────────────────────────────────────────────
DARK   = RGBColor(0x1a, 0x1a, 0x2e)
ACCENT = RGBColor(0x1a, 0x6b, 0x4a)   # dark green
WARN   = RGBColor(0xb8, 0x5c, 0x00)   # amber
DANGER = RGBColor(0xaa, 0x22, 0x22)   # red
GREY   = RGBColor(0x55, 0x55, 0x55)

def add_para(doc, text="", size=11, bold=False, color=None,
             space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT,
             italic=False):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    if text:
        run = p.add_run(text)
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        if color:
            run.font.color.rgb = color
    return p

def add_rule(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "CCCCCC")
    pBdr.append(bottom)
    pPr.append(pBdr)

def add_bullet(doc, label, body, label_color=DARK):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Inches(0.25)
    if label:
        r = p.add_run(label + "  ")
        r.font.size  = Pt(10.5)
        r.font.bold  = True
        r.font.color.rgb = label_color
    r2 = p.add_run(body)
    r2.font.size = Pt(10.5)
    return p

# ── Header block ──────────────────────────────────────────────────────────────
add_para(doc, "MERIDIAN TECHNOLOGIES", size=9, color=GREY,
         space_before=0, space_after=2)
add_para(doc, "Board of Directors — Annual Strategic Review",
         size=9, color=GREY, space_before=0, space_after=2)
add_para(doc, "CEO Opening Remarks  |  May 2026  |  Catherine Park",
         size=9, color=GREY, space_before=0, space_after=10)

add_rule(doc)

# ── Headline ──────────────────────────────────────────────────────────────────
add_para(doc,
         "We have a healthy enterprise, a profitable company, and a two-year "
         "window to decide what Meridian is — before the market decides for us.",
         size=14, bold=True, color=DARK,
         space_before=14, space_after=14,
         align=WD_ALIGN_PARAGRAPH.LEFT)

add_rule(doc)

# ── Framing ───────────────────────────────────────────────────────────────────
add_para(doc, "Context  (spoken: ~45 seconds)", size=8, italic=True,
         color=GREY, space_before=8, space_after=4)

add_para(doc,
         "This is my first annual board review as your CEO. I want to use "
         "this time honestly — not to recap a year you already know, but to "
         "name three problems that require board-level decisions, and to make "
         "one specific ask before we close. I will take ten minutes of "
         "questions after.",
         size=10.5, space_before=0, space_after=10)

# ── The Chart ─────────────────────────────────────────────────────────────────
add_para(doc, "The Picture  (spoken: ~30 seconds)", size=8, italic=True,
         color=GREY, space_before=4, space_after=6)

try:
    doc.add_picture("meridian_strategic_chart.png", width=Inches(5.8))
    last_para = doc.paragraphs[-1]
    last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_para(doc,
             "Figure 1. ARR growth deceleration (top) and NRR by segment (bottom), "
             "Q1 2024–Q4 2025. Sources: meridian_financials_2022_2025.csv, "
             "meridian_kpis_2024.csv, meridian_segments_overview.md.",
             size=8, italic=True, color=GREY,
             space_before=2, space_after=10,
             align=WD_ALIGN_PARAGRAPH.CENTER)
except Exception as e:
    add_para(doc,
             f"[Chart: meridian_strategic_chart.png — {e}]",
             size=9, italic=True, color=GREY, space_before=2, space_after=10)

add_para(doc,
         "This chart is the whole story. Enterprise is healthy and growing. "
         "SMB is in managed decline. Mid-market — our largest segment at 47% "
         "of ARR — is compressing toward break-even NRR. And across all three, "
         "total growth has decelerated from 28% in 2022 to 10% last quarter. "
         "That deceleration is structural. It is the reason this board meeting matters.",
         size=10.5, space_before=0, space_after=10)

add_rule(doc)

# ── Issue 1 ───────────────────────────────────────────────────────────────────
add_para(doc, "Issue 1 of 3 — Growth deceleration is structural; AI is the only re-acceleration lever, and it is unproven  (spoken: ~75 seconds)",
         size=8, italic=True, color=GREY, space_before=8, space_after=4)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after  = Pt(6)
r = p.add_run("Full-year 2025 revenue was $400M, up 11% — the slowest growth "
              "this company has reported as a public. Our 2026 guide is 10–14%, "
              "below Street consensus at 15%. I said on our Q1 call that this "
              "deceleration is not transitory. I meant it.")
r.font.size = Pt(10.5)

add_para(doc, "The evidence:", size=10.5, bold=True, space_before=4, space_after=2)
add_bullet(doc, "Revenue growth:", "28% (2022) → 19% (2023) → 16% (2024) → 11% (2025). "
           "Four consecutive years of deceleration. (meridian_financials_2022_2025.csv)")
add_bullet(doc, "Sales efficiency:", "Magic number fell from 1.20 (Q1 2024) to 0.92 (Q4 2025) — "
           "we are spending more to acquire less ARR. (meridian_kpis_2024.csv)")
add_bullet(doc, "AI Copilot today:", "710 paying seats, $3.5M ARR contribution on a $413M base. "
           "That is 0.85% of ARR. It is a promising signal, not yet a growth driver. "
           "(meridian_earnings_call_q4_2025.txt)")

add_para(doc,
         "AI Copilot is real — 44% enterprise attach rate in Q4, ahead of our "
         "own target. But we cannot book re-acceleration on the basis of 710 seats. "
         "The board needs to pressure-test whether the Investor Day thesis on March 11 "
         "is credible, and what happens to our valuation if it is not.",
         size=10.5, space_before=6, space_after=10)

add_rule(doc)

# ── Issue 2 ───────────────────────────────────────────────────────────────────
add_para(doc, "Issue 2 of 3 — Mid-market is converging on break-even NRR; we do not control the competitive dynamic driving it  (spoken: ~75 seconds)",
         size=8, italic=True, color=GREY, space_before=8, space_after=4)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after  = Pt(6)
r = p.add_run("Mid-market is $194M ARR — 47% of the company. It gets less "
              "board attention than SMB because the decline is slower. That "
              "is precisely why it is dangerous.")
r.font.size = Pt(10.5)

add_para(doc, "The evidence:", size=10.5, bold=True, space_before=4, space_after=2)
add_bullet(doc, "NRR compression:", "Mid-market NRR fell from 115% (2022) to 102% (Q4 2025). "
           "Gross logo churn rose from 9.1% to 10.2% over the same period. "
           "(meridian_kpis_2024.csv)",
           label_color=WARN)
add_bullet(doc, "Competitive trigger:", "Asana bundled AI into its standard tier in Q4 2025. "
           "Every mid-market renewal now includes a demand for price holds, seat expansion "
           "at flat cost, or free AI Copilot. (meridian_earnings_call_q3_2025.txt)",
           label_color=WARN)
add_bullet(doc, "No checkbook fix:", "Unlike talent retention, this cannot be solved with "
           "capital. It requires a product response (AI parity) and/or a pricing model "
           "change — both of which take 12–18 months to show results.",
           label_color=WARN)

add_para(doc,
         "If mid-market NRR crosses below 100%, we will have two of three segments "
         "in net contraction simultaneously. The 2026 resource management module "
         "and pricing refresh on the roadmap are the right moves — but the board "
         "should understand the exposure in the gap before they ship.",
         size=10.5, space_before=6, space_after=10)

add_rule(doc)

# ── Issue 3 ───────────────────────────────────────────────────────────────────
add_para(doc, "Issue 3 of 3 — Engineering capacity and Helio retention are the binding constraint on every strategy we just discussed  (spoken: ~60 seconds)",
         size=8, italic=True, color=GREY, space_before=8, space_after=4)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after  = Pt(6)
r = p.add_run("We cannot execute the mid-market response, the Copilot roadmap, "
              "or the Investor Day commitments without the engineering team to "
              "build them. That team is under stress right now.")
r.font.size = Pt(10.5)

add_para(doc, "The evidence:", size=10.5, bold=True, space_before=4, space_after=2)
add_bullet(doc, "Roadmap delivery:", "8 of 12 product commitments in 2025 slipped or were "
           "deferred. CPO's own assessment: 'Engineering capacity is the binding constraint.' "
           "(meridian_product_roadmap_2025.md)",
           label_color=DANGER)
add_bullet(doc, "Senior engineering attrition risk:", "27% of senior engineers flagged "
           "below-market compensation in the October 2025 survey. People team estimates "
           "15–25 senior engineers are at immediate flight risk. "
           "(meridian_employee_survey_2025.md)",
           label_color=DANGER)
add_bullet(doc, "Helio cliff:", "The Helio retention agreements — the foundation of our "
           "agentic roadmap — carry a cash compensation cliff in 2026. CPO flagged this "
           "explicitly: 'If the team unwinds early… the roadmap is exposed.' "
           "(meridian_product_roadmap_2025.md)",
           label_color=DANGER)

add_para(doc,
         "This issue is solvable with capital. We have $463M in cash and no debt. "
         "A senior engineering compensation refresh costs $5–10M. The Helio cliff "
         "can be addressed proactively. What it requires is a board decision to act "
         "before the cliff, not after.",
         size=10.5, space_before=6, space_after=10)

add_rule(doc)

# ── The Ask ───────────────────────────────────────────────────────────────────
add_para(doc, "My One Ask  (spoken: ~30 seconds)", size=8, italic=True,
         color=GREY, space_before=8, space_after=6)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after  = Pt(8)
r1 = p.add_run("I am asking the board to authorize a senior engineering and "
               "Helio retention package — up to $12M in incremental equity "
               "and cash — before the end of Q1 2026.")
r1.font.size = Pt(11.5)
r1.font.bold = True
r1.font.color.rgb = DARK

add_para(doc,
         "Every other issue on this agenda — growth re-acceleration, mid-market "
         "defense, Investor Day credibility — depends on the engineering team "
         "staying intact. This is the one action the board can take today that "
         "reduces risk across all three problems simultaneously. I have the People "
         "& Compensation Committee's support. I need full board authorization to "
         "move before the cliff hits.",
         size=10.5, space_before=0, space_after=12)

add_rule(doc)

# ── Closing line ──────────────────────────────────────────────────────────────
add_para(doc,
         "The enterprise franchise Lenore built is the best asset in this category. "
         "Our job is to make sure we have the team to build the next chapter on top of it. "
         "I'll take questions.",
         size=10.5, italic=True, space_before=8, space_after=4)

add_rule(doc)

# ── Footer metadata ───────────────────────────────────────────────────────────
add_para(doc,
         "Confidential — Meridian Technologies Board of Directors only  |  "
         "Prepared by: Office of the CEO  |  May 2026",
         size=8, color=GREY, space_before=6, space_after=0,
         align=WD_ALIGN_PARAGRAPH.CENTER)

doc.save("board_opening_remarks.docx")
print("Saved: board_opening_remarks.docx")
