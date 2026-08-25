# 2027 Market Expansion Deck

A **standalone** pitch deck proposing Jetson's next-market recommendations for 2027.
This does **not** touch the master *Panorama Policy Overlay* deck — it is a new, separate output.

- **Deliverable:** `2027-expansion-deck.html` — a self-contained interactive HTML deck (open in any browser; also published as a private Claude Artifact).
- **Slide 1:** the policy-offset market map ("Out-of-pocket is the outcome, not the axis"), mimicking Slide 7 of the master deck, re-plotted on **live Panorama data**, with the 14 2027 candidates in **amber (`#F9A843`)** and 4 licensed-model markets as **green diamonds**.
- **Slide 2:** the recommended 2027 markets as a clean list — 14 direct-entry candidates (amber, numbered) + 4 licensed-model markets (green "L").

**Roster (18 markets, all live Panorama):** 14 direct-entry candidates (the 11 briefed + Minneapolis, Philadelphia, Royal Oak Metro) and 4 licensed-model markets tagged "licensed" at Z's request — **Phoenix, Memphis, Providence, Hartford** (green diamonds / green "L").

Status: **working draft — Slides 1 & 2 only.** Further slides pending sign-off from Z (VP New Market Expansion).

## Data source — the current Panorama tool (JEV, Notion-resolved)

The JEV work has been **merged to `main`** (PR #144, "Panorama: sync to rebate-recast for git-based deploys"), so `main` is now canonical — this deck syncs from `main` (`2026-08-25`, 126 markets).

- **126 markets.** All 18 roster markets are live Panorama markets — none are estimated.
- **JEV $ (`jevDollars`)** is the headline rebate metric: the **risk-adjusted** rebate a mid-AMI Jetson customer actually captures, discounted for program status, funding risk and friction.
- **Federal contribution = $0.** Per `jev.js`, DOE scoped HEAR to *electric-to-electric* and Jetson does *gas-to-electric*, so federal funds nothing; the 25C credit expired Dec 31 2025. The x-axis is therefore HEAR-free by construction (no manual subtraction).

### ⚠ JEV must be resolved the way the app resolves it
`m.jevDollars` as exported by `markets.js` is only the **legacy fallback**. Before render, the app (`data/useNotionRebates.js`) overrides it from the validated **Notion "Heat Pump Rebate Programs"** pull:

```
effective = { ...RESEARCHED_OVERRIDES, ...GENERATED_REBATES.markets }   // CORRECTED_OVERRIDES deliberately NOT applied
floor-merge: an override BELOW the legacy value is floored back to legacy
             unless the reduction is trusted (research/corrected source,
             CONFIRMED_ZERO market, or any program row with jev > 0)
```
`build_dataset.mjs` replicates this exactly (74 of 126 markets are Notion-covered, 8 floored). **Reading `jevDollars` raw understates/overstates most markets** — it previously put Phoenix at $5,400 when the tool shows $455, and Hartford at $3,600 when the tool shows $6,832.

| Field | Source | Notes |
|---|---|---|
| Rebate value (Slide 1 **x-axis**) | **live** — Notion-resolved `jevDollars` (see above) | Risk-adjusted, federal-free. Roster range $230–$6,832; all markets $0–$16,088. |
| W-TAM / tier / existing flag | **live** — Panorama `markets.js` | Panorama = source of truth. 7 existing markets (Denver, Loveland, Colorado Springs, Vancouver, White Plains, Marlborough, …). |
| Install cost (Slide 1 **y-axis**) | ⚠ **MODELED — not a Panorama field** | Panorama still stores no per-market install price. See formula below. Treat the vertical axis as directional, not quoted pricing. |
| Funding/timing risk (⚠) | **live** — Panorama rebate notes (`stackable[id].note`) | Markets whose rebate note carries a ⚠ (waitlist / program ending / funding risk) are flagged. |

### Modeled install-cost formula (y-axis) — the one remaining estimate
```
installCost = $19,000 base
            × regional factor   (Panorama warehouseCost: Low 0.78 / Medium 1.00 / High 1.22)
            + cold-climate adder (heating degree-days: ≥6500 → +$1,500 / ≥5000 → +$750 / else +$0)
```
A transparent proxy, **not** a Jetson pricebook figure. **Open ask to Z:** supply real installed cost per market (pricebook / proforma) to make the y-axis authoritative.

### Chart conventions
- Diagonal bands = net out-of-pocket (install − JEV) at **$14k / $18k / $22k**, chosen to bracket the candidate cloud.
- Markers: amber circle = 2027 candidate · green diamond = licensed market · hollow = other tracked Panorama market. Jetson's **existing markets are excluded** from the plot (Z: too busy) — the map is scoped to where we go next.
- Markets with JEV > $8k clamp to the right edge.

## Open questions for Z
1. Confirm the accent color `#F9A843` against Jetson brand guidelines.
2. Supply real per-market install cost to replace the modeled y-axis.
3. Confirm the pipeline flags for Portland / Dallas.
4. Phoenix and Memphis are tagged "licensed" per Z, though Panorama classifies them as gravity (owned-footprint); only Providence and Hartford are relay/licensed in the tool.

## Rebuild
Requires Node (ESM) + Python 3 and a checkout of `conductor-playground` on **`main`**.
```bash
export PANORAMA_SRC=/path/to/conductor-playground/project-panorama/src   # optional; has a default
node   scripts/compute.mjs         # sanity-print candidate JEV $
node   scripts/build_dataset.mjs   # regenerate dataset.json from live data
python3 scripts/build.py           # inline font + logo + data → 2027-expansion-deck.html
```

## Files
```
2027-expansion-deck.html   generated, self-contained deck (the deliverable)
deck.template.html         HTML/CSS/JS template with __FONT_B64__ / __LOGO_B64__ / __DATASET__ placeholders
dataset.json               computed plot data (126 Panorama markets + 18-market roster)
assets/                    Jetson brand font (MNKY Jane) + green logo, inlined at build
scripts/                   compute.mjs · build_dataset.mjs · build.py
```
