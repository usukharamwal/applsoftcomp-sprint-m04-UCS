# Observations — S&P 500 Semantic Map

## Dataset & Axes

The analysis uses the S&P 500 sample (203 companies, 11 GICS sectors).
Two semantic axes were constructed using the SemAxis framework with the
`all-mpnet-base-v2` sentence transformer:

- **Axis 1 (X): Traditional/Legacy <--> Innovative/Digital**: captures how
  "new-economy" a company's core identity is in language space.
- **Axis 2 (Y): Enterprise/Industrial <--> Consumer-Facing**: captures
  whether a company sells to individual people or to other businesses and
  institutions.

---

## What separates along each axis?

**Axis 1 (Innovation)** cleanly separates the S&P 500 into two camps.
Information Technology companies (NVIDIA, Salesforce, Adobe) cluster
strongly toward the positive (innovative) end, joined by high-growth
Communication Services names (Meta, Netflix, Alphabet). At the negative
end sit Energy producers (ExxonMobil, Chevron), Utilities, and heavy
Industrials such as sectors whose identities in text are dominated by words
like "infrastructure", "commodity", and "established operations." Consumer
Discretionary is the most interesting sector on this axis: it straddles
both poles, with digital-native brands (Amazon, Airbnb, Booking Holdings)
sitting far right and traditional retailers (Best Buy, Dollar General) pulling
left. This split reflects a genuine structural divide within the sector that
the embedding captures from how these companies are discussed in text.

**Axis 2 (Consumer vs. Enterprise)** produces an almost orthogonal split.
Consumer Staples and Consumer Discretionary companies sit at the top, while
Energy, Materials, and Industrials anchor the bottom. Financials are
revealing: retail-banking brands (Visa, Mastercard, PayPal) score high on
the consumer axis because their products touch everyday people, whereas pure
institutional players (Moody's, S&P Global, CME Group) score low, sitting
closer to the enterprise/industrial pole. Health Care occupies a wide
vertical band from pharmaceutical brands pitched directly to patients score
higher than medical-device or life-sciences companies that sell
primarily to hospitals and research institutions.

---

## Most surprising point

The most surprising placement is **Utilities** on Axis 1. Intuitively,
utilities feel like the least innovative sector, yet several names score
near zero rather than at the extreme negative end. The likely explanation is
that the embedding has absorbed a wave of recent press around "smart grid,"
"clean energy transition," and "digital metering" — language that pulls
utility company representations closer to the innovation centroid than
their actual business models would warrant. This is a good reminder that
SemAxis scores reflect **how an entity is discussed in text**, not
its objective operational characteristics. The embedding is a mirror of
language, not of reality.

---

## What would a third axis capture?

A **Global/Multinational <--> Domestic/Regional** axis would add the most
explanatory power to this map. Many companies occupy similar positions on
the current two axes but differ dramatically in geographic footprint:
Procter & Gamble and Church & Dwight are both consumer staples scoring
similarly on Innovation and Consumer, yet one derives the majority of
revenue internationally while the other is predominantly North American.
Pole words for this axis could be:
- **+** (global): "multinational corporation worldwide markets", "international operations emerging economies", "global brand"
- **−** (domestic): "regional provider local market", "domestic operations United States only", "community bank"

This third axis would slice the Consumer Staples cluster and reveal
which financial and utility names have meaningful overseas exposure, a
distinction invisible in the current 2D view.
