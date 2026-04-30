# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "sentence-transformers>=2.7.0",
#     "numpy>=1.24",
#     "pandas>=2.0",
#     "matplotlib>=3.7",
# ]
# ///
"""
Sprint M04 — Semantic Axes
Dataset  : S&P 500 sample (data/sp500.csv, 203 companies)
Axis 1 X : Traditional / Legacy  ←→  Innovative / Digital
Axis 2 Y : Enterprise / Industrial  ←→  Consumer-Facing
Output   : figs/semantic_map.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from pathlib import Path
from sentence_transformers import SentenceTransformer

# ── 0. Output directory ───────────────────────────────────────────────────────
FIGS_DIR = Path("figs")
FIGS_DIR.mkdir(exist_ok=True)

# ── 1. Load embedding model ───────────────────────────────────────────────────
print("Loading model …")
model = SentenceTransformer("all-mpnet-base-v2")


# ── 2. SemAxis helpers ────────────────────────────────────────────────────────
def make_axis(positive_words, negative_words, embedding_model):
    """Return a unit-length semantic axis from two opposing word sets."""
    pos_emb = embedding_model.encode(positive_words, normalize_embeddings=True)
    neg_emb = embedding_model.encode(negative_words, normalize_embeddings=True)
    v = pos_emb.mean(axis=0) - neg_emb.mean(axis=0)
    return v / (np.linalg.norm(v) + 1e-10)


def score_words(words, axis, embedding_model):
    """Project each word onto the axis; returns one score per word."""
    emb = embedding_model.encode(list(words), normalize_embeddings=True)
    return emb @ axis


# ── 3. Define two semantic axes ───────────────────────────────────────────────
print("Building axes …")

# Axis 1 (X) — Traditional / Legacy  ←→  Innovative / Digital
# Captures how "new-economy" a company is in its core identity.
axis_innovation = make_axis(
    positive_words=[
        "disruptive innovation",
        "cutting-edge technology",
        "artificial intelligence platform",
        "digital transformation software",
        "startup tech unicorn",
    ],
    negative_words=[
        "legacy industry established institution",
        "century-old conventional business model",
        "old economy traditional manufacturing",
        "brick and mortar retail store",
        "industrial commodity supplier",
    ],
    embedding_model=model,
)

# Axis 2 (Y) — Enterprise / Industrial  ←→  Consumer-Facing
# Captures whether a company sells to individual people or to other businesses.
axis_consumer = make_axis(
    positive_words=[
        "consumer products everyday household brand",
        "retail shopping personal lifestyle",
        "mass market direct to consumer",
        "entertainment streaming for individuals",
        "personal device people use daily",
    ],
    negative_words=[
        "business to business enterprise infrastructure",
        "industrial machinery heavy manufacturing",
        "institutional financial services corporate",
        "raw materials wholesale supplier",
        "utilities power grid operator",
    ],
    embedding_model=model,
)

# Pole separation check (rule-of-thumb: distance ≥ 0.3)
for name, axis, pos, neg in [
    (
        "Innovation",
        axis_innovation,
        ["disruptive innovation", "cutting-edge technology", "artificial intelligence platform",
         "digital transformation software", "startup tech unicorn"],
        ["legacy industry established institution", "century-old conventional business model",
         "old economy traditional manufacturing", "brick and mortar retail store",
         "industrial commodity supplier"],
    ),
    (
        "Consumer",
        axis_consumer,
        ["consumer products everyday household brand", "retail shopping personal lifestyle",
         "mass market direct to consumer", "entertainment streaming for individuals",
         "personal device people use daily"],
        ["business to business enterprise infrastructure", "industrial machinery heavy manufacturing",
         "institutional financial services corporate", "raw materials wholesale supplier",
         "utilities power grid operator"],
    ),
]:
    pos_c = model.encode(pos, normalize_embeddings=True).mean(axis=0)
    neg_c = model.encode(neg, normalize_embeddings=True).mean(axis=0)
    dist = float(np.linalg.norm(pos_c - neg_c))
    print(f"  Axis '{name}' pole distance: {dist:.3f}  {'✓' if dist >= 0.3 else '✗ (< 0.3)'}")


# ── 4. Load dataset & score companies ─────────────────────────────────────────
print("Scoring companies …")
df = pd.read_csv("data/sp500.csv", dtype={"name": "string", "sector": "category"})

df = df.assign(
    x=score_words(df["name"].tolist(), axis_innovation, model),
    y=score_words(df["name"].tolist(), axis_consumer, model),
)

print(f"  {len(df)} companies across {df['sector'].nunique()} sectors.")


# ── 5. Plot ───────────────────────────────────────────────────────────────────
print("Plotting …")

# ---- visual encoding --------------------------------------------------------
SECTORS = sorted(df["sector"].cat.categories.tolist())

# Colorblind-friendly palette (Okabe–Ito extended; no red/green clash)
PALETTE = {
    "Communication Services":  "#0072B2",   # blue
    "Consumer Discretionary":  "#E69F00",   # orange
    "Consumer Staples":        "#D55E00",   # vermilion
    "Energy":                  "#009E73",   # bluish-green
    "Financials":              "#56B4E9",   # sky blue
    "Health Care":             "#CC79A7",   # reddish-purple
    "Industrials":             "#F0E442",   # yellow
    "Information Technology":  "#999999",   # grey
    "Materials":               "#882255",   # wine
    "Real Estate":             "#44AA99",   # teal
    "Utilities":               "#117733",   # dark green
}

# Shape: redundant encoding for colorblind viewers
MARKER = {
    "Communication Services":  "o",   # circle
    "Consumer Discretionary":  "^",   # triangle up
    "Consumer Staples":        "^",
    "Energy":                  "P",   # filled plus
    "Financials":              "s",   # square
    "Health Care":             "D",   # diamond
    "Industrials":             "X",   # filled x
    "Information Technology":  "o",
    "Materials":               "P",
    "Real Estate":             "s",
    "Utilities":               "X",
}

# ---- draw -------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 9))

for sector in SECTORS:
    mask = df["sector"] == sector
    ax.scatter(
        df.loc[mask, "x"],
        df.loc[mask, "y"],
        c=PALETTE.get(sector, "#444444"),
        marker=MARKER.get(sector, "o"),
        s=65,
        alpha=0.85,
        edgecolors="white",
        linewidths=0.6,
        zorder=3,
    )

# Zero lines
ax.axhline(0, color="#bbbbbb", linewidth=0.9, linestyle="--", zorder=1)
ax.axvline(0, color="#bbbbbb", linewidth=0.9, linestyle="--", zorder=1)

# Quadrant annotations (positioned in axes-fraction coords to stay inside plot)
q_kw = dict(fontsize=8.5, color="#aaaaaa", style="italic",
            transform=ax.transAxes, zorder=2)
ax.text(0.97, 0.97, "Innovative & Consumer",  ha="right", va="top",    **q_kw)
ax.text(0.03, 0.97, "Traditional & Consumer", ha="left",  va="top",    **q_kw)
ax.text(0.97, 0.03, "Innovative & Industrial", ha="right", va="bottom", **q_kw)
ax.text(0.03, 0.03, "Traditional & Industrial", ha="left", va="bottom", **q_kw)

# Label the most extreme companies (top N per axis extreme)
N = 7
extremes = pd.concat([
    df.nlargest(N, "x"),
    df.nsmallest(N, "x"),
    df.nlargest(N, "y"),
    df.nsmallest(N, "y"),
]).drop_duplicates(subset="name")

for _, row in extremes.iterrows():
    ax.annotate(
        row["name"],
        xy=(row["x"], row["y"]),
        xytext=(5, 4),
        textcoords="offset points",
        fontsize=6.2,
        color="#333333",
        alpha=0.88,
    )

# ---- axes & title -----------------------------------------------------------
ax.set_xlabel("← Traditional / Legacy                 Innovative / Digital →", fontsize=11)
ax.set_ylabel("← Enterprise / Industrial                 Consumer-Facing →",   fontsize=11)
ax.set_title(
    "S&P 500 Companies in 2D Semantic Space\n"
    "Axis 1: Traditional ↔ Innovative   ·   Axis 2: Enterprise ↔ Consumer",
    fontsize=13, fontweight="bold", pad=14,
)

# ---- legend (color + shape combined) ----------------------------------------
legend_handles = [
    mlines.Line2D(
        [], [],
        color=PALETTE.get(s, "#444444"),
        marker=MARKER.get(s, "o"),
        linestyle="None",
        markersize=7,
        label=s,
        markeredgecolor="white",
        markeredgewidth=0.5,
    )
    for s in SECTORS
]
ax.legend(
    handles=legend_handles,
    title="GICS Sector",
    loc="upper left",
    fontsize=8,
    title_fontsize=9,
    framealpha=0.9,
    edgecolor="#cccccc",
)

ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()

# ── 6. Save ───────────────────────────────────────────────────────────────────
out = FIGS_DIR / "semantic_map.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"Saved → {out}")
