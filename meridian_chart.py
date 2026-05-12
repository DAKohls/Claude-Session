import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

# --- Data ---
quarters = ["Q1\n2024","Q2\n2024","Q3\n2024","Q4\n2024",
            "Q1\n2025","Q2\n2025","Q3\n2025","Q4\n2025"]

# ARR YoY growth by segment (derived from segment overview + financials)
# Enterprise ARR: 2022Q4=$74M, 2024Q4=$138M, 2025Q4=$167M
# Mid-market ARR: 2025Q4=$194M, YoY+6%; so 2024Q4~$183M
# SMB ARR: 2025Q4=$52M, YoY-23%; so 2024Q4~$68M
# Total ARR per financials CSV
total_arr = [357.5, 367.6, 374.1, 374.8, 398.9, 408.5, 419.6, 412.8]

# NRR by segment from kpis CSV
nrr_enterprise  = [127, 127, 126, 126, 125, 125, 125, 125]
nrr_midmarket   = [108, 107, 106, 105, 104, 103, 103, 102]
nrr_smb         = [98,  96,  93,  91,  89,  88,  86,  84]

# YoY total ARR growth (Q1 2023 ARR = 302.5 as base)
prior_arr =      [302.5, 316.1, 329.8, 328.0,  # 2023
                  357.5, 367.6, 374.1, 374.8]   # 2024
arr_growth_yoy = [(c/p - 1)*100 for c, p in zip(total_arr, prior_arr)]

# --- Layout ---
fig = plt.figure(figsize=(13, 9), facecolor="#0f1117")
fig.suptitle(
    "Meridian Technologies — The Core Strategic Problem",
    color="white", fontsize=16, fontweight="bold", y=0.97
)

ax1 = fig.add_axes([0.07, 0.54, 0.56, 0.36])   # top-left: ARR growth
ax2 = fig.add_axes([0.07, 0.10, 0.56, 0.36])   # bottom-left: NRR by segment
ax3 = fig.add_axes([0.70, 0.10, 0.27, 0.80])   # right: annotation panel

for ax in [ax1, ax2]:
    ax.set_facecolor("#0f1117")
    ax.tick_params(colors="white", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#444")
    ax.yaxis.label.set_color("white")
    ax.xaxis.label.set_color("white")
    ax.grid(axis="y", color="#2a2a2a", linewidth=0.7)

x = np.arange(len(quarters))

# --- Top chart: total ARR YoY growth as bars ---
colors_growth = ["#e05252" if g < 12 else "#f0a500" if g < 16 else "#4caf7d"
                 for g in arr_growth_yoy]
bars = ax1.bar(x, arr_growth_yoy, color=colors_growth, width=0.55, zorder=3)
ax1.axhline(10, color="#888", linewidth=0.8, linestyle="--")
ax1.set_xticks(x)
ax1.set_xticklabels(quarters, color="white", fontsize=8)
ax1.set_ylabel("ARR YoY Growth (%)", color="white", fontsize=9)
ax1.set_ylim(0, 28)
ax1.set_title("Total ARR Growth — Structural Deceleration",
              color="#aaa", fontsize=10, pad=6)
for bar, val in zip(bars, arr_growth_yoy):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
             f"{val:.0f}%", ha="center", va="bottom", color="white", fontsize=8)

# shade 2025
ax1.axvspan(3.72, 7.28, color="#ffffff", alpha=0.04, zorder=0)
ax1.text(5.5, 25.5, "2025", color="#777", fontsize=8, ha="center")

# --- Bottom chart: NRR by segment ---
ax2.plot(x, nrr_enterprise, color="#4caf7d", linewidth=2.2, marker="o",
         markersize=5, label="Enterprise", zorder=3)
ax2.plot(x, nrr_midmarket,  color="#f0a500", linewidth=2.2, marker="s",
         markersize=5, label="Mid-market", zorder=3)
ax2.plot(x, nrr_smb,        color="#e05252", linewidth=2.2, marker="^",
         markersize=5, label="SMB",        zorder=3)
ax2.axhline(100, color="white", linewidth=1.1, linestyle="--", alpha=0.6)
ax2.text(7.1, 100.4, "100% =\nbreak-even", color="#aaa", fontsize=7, va="bottom")
ax2.set_xticks(x)
ax2.set_xticklabels(quarters, color="white", fontsize=8)
ax2.set_ylabel("Net Revenue Retention (%)", color="white", fontsize=9)
ax2.set_ylim(78, 134)
ax2.set_title("NRR by Segment — Mid-market Converging on Break-even",
              color="#aaa", fontsize=10, pad=6)
ax2.legend(facecolor="#1a1a2e", edgecolor="#444", labelcolor="white",
           fontsize=8, loc="lower left")
ax2.axvspan(3.72, 7.28, color="#ffffff", alpha=0.04, zorder=0)

# end-of-line labels
for series, label, color in [
    (nrr_enterprise, "125%", "#4caf7d"),
    (nrr_midmarket,  "102%", "#f0a500"),
    (nrr_smb,        " 84%", "#e05252"),
]:
    ax2.annotate(label, xy=(7, series[-1]),
                 xytext=(7.15, series[-1]),
                 color=color, fontsize=8, va="center",
                 fontweight="bold")

# --- Right panel: annotation ---
ax3.set_facecolor("#111827")
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis("off")
for spine in ax3.spines.values():
    spine.set_color("#333")

def anno(ax, y, dot_color, headline, body, size_h=9.5, size_b=8):
    ax.plot(0.07, y + 0.015, "o", color=dot_color, markersize=7,
            transform=ax.transAxes, clip_on=False)
    ax.text(0.17, y + 0.015, headline, color="white", fontsize=size_h,
            fontweight="bold", va="center", transform=ax.transAxes)
    ax.text(0.07, y - 0.065, body, color="#aaaaaa", fontsize=size_b,
            va="top", transform=ax.transAxes, wrap=True,
            multialignment="left")

ax3.text(0.07, 0.96, "Key Takeaways", color="white", fontsize=11,
         fontweight="bold", transform=ax3.transAxes)
ax3.axhline(0, color="#333")  # dummy

anno(ax3, 0.83,
     "#4caf7d", "Enterprise: healthy",
     "NRR 125%, growing 21%\nYoY. The asset. $167M ARR.")

anno(ax3, 0.60,
     "#f0a500", "Mid-market: warning",
     "NRR 102% and falling.\nAsana bundled AI in Q4 2025.\nRenewals under pressure.\n$194M ARR — the largest\nsegment.")

anno(ax3, 0.37,
     "#e05252", "SMB: managed decline",
     "NRR 84%, logo churn 22%.\nDown 23% YoY. No longer\nsubsidized; run for cash.")

anno(ax3, 0.14,
     "#888888", "Overall growth: structural",
     "28% (2022) → 11% (2025).\nCopilot at $3.5M ARR —\ntoo small to move the dial\nyet. 2026 guide: 10–14%.")

ax3.text(0.07, 0.02, "Source: meridian_financials_2022_2025.csv,\nmeridian_kpis_2024.csv, meridian_segments_overview.md",
         color="#555", fontsize=6.5, transform=ax3.transAxes)

plt.savefig("meridian_strategic_chart.png", dpi=150, bbox_inches="tight",
            facecolor="#0f1117")
print("Saved: meridian_strategic_chart.png")
