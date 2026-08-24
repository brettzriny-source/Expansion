# 2027 Market Expansion Deck

A **standalone** pitch deck proposing Jetson's next-market recommendations for 2027.
This does **not** touch the master *Panorama Policy Overlay* deck — it is a new, separate output.

- **Deliverable:** `2027-expansion-deck.html` — a self-contained interactive HTML deck (open in any browser; also published as a private Claude Artifact).
- **Slide 1:** the policy-offset market map ("Out-of-pocket is the outcome, not the axis"), mimicking Slide 7 of the master deck, re-plotted on **live Panorama data**, with the 14 2027 candidates in **amber (`#F9A843`)** and 4 licensed-model markets as **green diamonds**.
- **Slide 2:** the recommended 2027 markets as a clean list — 14 direct-entry candidates (amber, numbered) + 4 licensed-model markets (green "L").

**Roster (18 markets, all live Panorama):** 14 direct-entry candidates (the 11 briefed + Minneapolis, Philadelphia, Royal Oak Metro) and 4 licensed-model markets tagged "licensed" at Z's request — **Phoenix, Memphis, Providence, Hartford** (green diamonds / green "L").

Status: **working draft — Slides 1 & 2 only.** Further slides pending sign-off from Z (VP New Market Expansion).

## Data source — the current Panorama tool (JEV build)

Panorama received a comprehensive overhaul (branch **`rebate-recast`** in the monorepo `conductor-playground`; commit *"Panorama: comprehensive update — DOE e2e HEAR exclusion…"*, rebate data last reviewed **May 2026**). This deck sources from that build, **not** `main` (which still holds the older 67-market, HEAR-inclusive dataset). Key differences:

- **113 markets** (was 67). All 14 candidates are now live Panorama markets — none are estimated.
- **JEV $ (`jevDollars`)** is the new headline rebate metric: the tool's **risk-adjusted** rebate a mid-AMI Jetson customer actually captures (utility + state `captureDollars`, discounted for program status, funding risk, and friction — see `data/jev.js`).
- **Federal HEAR = $0** for every market. Per `jev.js`: DOE scoped HEAR to *electric-to-electric*, and Jetson does *gas-to-electric* conversions, so federal contributes nothing. The 25C credit expired Dec 31 2025. This is why the map's x-axis is HEAR-free by construction (no manual subtraction).

| Field | Source | Notes |
|---|---|---|
| Rebate value (Slide 1 **x-axis**) | **live** — `m.jevDollars` from Panorama `markets.js` (rebate-recast) | Risk-adjusted, HEAR-free. Candidate range $230–$5,355; all markets $0–$10,800. |
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
- Markers: amber = 2027 candidate · solid fern = existing market · hollow = other tracked Panorama market.
- Markets with JEV > $8k clamp to the right edge.

## Open questions for Z
1. Confirm `rebate-recast` (JEV build) is the correct/live Panorama source (it's an unmerged branch; `main` differs).
2. Confirm the accent color `#F9A843` against Jetson brand guidelines.
3. Supply real per-market install cost to replace the modeled y-axis.
4. Confirm the pipeline flags for Portland / Dallas.

## Rebuild
Requires Node (ESM) + Python 3 and a checkout of `conductor-playground` on the **`rebate-recast`** branch.
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
dataset.json               computed plot data (113 Panorama markets + 14-candidate roster)
assets/                    Jetson brand font (MNKY Jane) + green logo, inlined at build
scripts/                   compute.mjs · build_dataset.mjs · build.py
```
