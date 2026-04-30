#!/usr/bin/env bash
# Reproducible pipeline template.
#
# Put ANYTHING you want here — this file is yours. The only requirement is
# that a grader can clone your repo and run `bash run.sh` to regenerate
# your final figure from scratch, with no manual steps.
#
# The `uvx ...` commands below are just one convenient way to get
# reproducibility: `uvx` spins up an isolated environment with the exact
# packages you ask for, so the grader doesn't need to install anything
# beyond `uv` itself. You're free to use plain `python`, a Makefile, a
# conda env, Docker, or whatever you prefer — as long as `bash run.sh`
# Just Works on a fresh clone.
#
# Conventions to keep:
#   - No manual steps.
#   - Data goes in `data/`, figures go in `figures/`.
#   - If you download/scrape data, do it here too (see the S&P 500
#     example below for a starting pattern).

set -euo pipefail

mkdir -p data figs

# ---------------------------------------------------------------------------
# Step 1 — raw data
# data/sp500.csv is already committed; nothing to download.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Step 2 — run the analysis and save the figure to figs/semantic_map.png
#
# submission.py carries PEP 723 inline metadata, so `uv run` installs its
# own isolated environment automatically — no manual pip install needed.
# If `uv` is not available, fall back to plain python (assumes deps are
# already installed in the active environment).
# ---------------------------------------------------------------------------
if command -v uv &>/dev/null; then
    uv run --script assignment2.py
else
    python assignment2.py
fi

echo "Done. See figs/semantic_map.png"
