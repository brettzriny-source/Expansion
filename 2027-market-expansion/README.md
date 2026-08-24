# 2027 Market Expansion Deck

A **standalone** pitch deck proposing Jetson's next-market recommendations for 2027.
This does **not** touch the master *Panorama Policy Overlay* deck — it is a new, separate output.

- **Deliverable:** `2027-expansion-deck.html` — a self-contained interactive HTML deck (open in any browser; also published as a private Claude Artifact).
- **Slide 1:** the policy-offset market map ("Out-of-pocket is the outcome, not the axis"), mimicking Slide 7 of the master deck, re-plotted on **live Panorama data**, with the 12 2027 candidates in **amber (`#F9A843`)**.
- **Slide 2:** the 12 recommended 2027 markets as a clean list.

The list is the 11 originally briefed markets plus **Minneapolis** (added at Z's request — a live Panorama market: Tier A, W-TAM 376k, rebate stack $400–$9,500, MN HEAR pending).

Status: **working draft — Slides 1 & 2 only.** Further slides pending sign-off from Z (VP New Market Expansion).

## Data provenance

| Field | Source | Notes |
|---|---|---|
| Rebate stack (Slide 1 **x-axis**) | **live** — Panorama `src/data/rebates.js` → `stackable[id].high` **minus the $8k HEAR line** | Plotted value = **market-rate stack** (utility + state, no income qualification). Panorama's `high` bakes in federal HEAR; we subtract the $8k HEAR component where the stack note carries it (`/HEAR \$8K/`), so income-qualified HEAR is excluded — it does not reach market-rate buyers (≤150% AMI cap). Basis April 2026; files synced **2026-08-24**. |
| W-TAM / tier / existing flag / HEAR status | **live** — Panorama `src/data/markets.js`, `rebates.js` | Panorama = source of truth (the proforma app syncs *from* it). |
| Install cost (Slide 1 **y-axis**) | ⚠ **MODELED — not a Panorama field** | Panorama stores no per-market install price. See formula below. Treat the vertical axis as directional, not quoted pricing. |
| 5 markets (Raleigh-Durham, Austin, Charlotte, Las Vegas, Richmond) | ⚠ **ESTIMATED — not in Panorama** | No Panorama record exists. Rebate figures inferred from each state's HEAR framework + nearest Panorama analog (see `scripts/build_dataset.mjs`). Rendered as amber **open dashed rings**. |

### Modeled install-cost formula (y-axis)
```
installCost = $19,000 base
            × regional factor   (Panorama warehouseCost: Low 0.78 / Medium 1.00 / High 1.22)
            + cold-climate adder (heating degree-days: ≥6500 → +$1,500 / ≥5000 → +$750 / else +$0)
```
Chosen so the plotted range (~$14.8k–$23.9k) sits inside Slide 7's $13k–$25.5k axis. It is a transparent proxy, **not** a Jetson pricebook figure.

### Known caveats (flagged, not silently estimated)
- **HEAR (HEEHRA) is excluded** from the plotted stack — it is income-qualified (≤150% AMI) and does not reach Jetson's market-rate buyers. Panorama *does* include HEAR (a `federal` block + $8k baked into every `stackable.high`); we strip it. Result: market-rate stacks are thin ($50–$6k) and net out-of-pocket runs **$12k–$23k** across the candidates.
- Federal **25C** market-rate credit expired Dec 31 2025 — excluded.
- Diagonal net-out-of-pocket bands set at **$12k / $16k / $20k** (adapted from Slide 7's $8/$12/$16k to bracket the ex-HEAR range).
- Markets whose market-rate stack exceeds **$12k** are clamped to the chart's right edge (`≥$12k`).
- **Vancouver** omitted from the map (no rebate record in Panorama).
- Panorama tracks **67** markets — the brief's "126 markets / 22 unverified" refers to the older source deck; this codebase has **no `unverified` flag**, so unverified markets cannot be machine-detected here.
- Per Panorama, **Portland & Dallas are modeled *expansion* markets** (in pipeline scenarios), **not** live "existing" markets; **Austin is not in Panorama at all**. This differs from the brief's assumption — confirm with Z.

## Open questions for Z
1. Confirm the accent color `#F9A843` against Jetson brand guidelines (the official palette has no approved warm accent).
2. Confirm the modeled install-cost approach for the y-axis, or supply real install pricing.
3. Confirm the pipeline-vs-new distinction for Portland / Dallas / Austin.
4. Confirm output format — currently interactive HTML / Artifact.

## Rebuild
Requires Node (ESM) + Python 3 and a local checkout of the `conductor-playground` monorepo.
```bash
export PANORAMA_SRC=/path/to/conductor-playground/project-panorama/src   # optional; has a default
node   scripts/compute.mjs         # sanity-print the live Panorama values
node   scripts/build_dataset.mjs   # regenerate dataset.json from live data
python3 scripts/build.py           # inline font + logo + data → 2027-expansion-deck.html
```

## Files
```
2027-expansion-deck.html   generated, self-contained deck (the deliverable)
deck.template.html         HTML/CSS/JS template with __FONT_B64__ / __LOGO_B64__ / __DATASET__ placeholders
dataset.json               computed plot data (live Panorama + 5 estimates)
assets/                    Jetson brand font (MNKY Jane) + green logo, inlined at build
scripts/                   compute.mjs · build_dataset.mjs · build.py
```
