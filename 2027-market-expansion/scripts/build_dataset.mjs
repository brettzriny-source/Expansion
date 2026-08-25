// Build the plot dataset from the LIVE Panorama tool (rebate-recast / JEV model).
// x = m.jevDollars  — Panorama's risk-adjusted rebate value a Jetson customer
//     actually captures. Federal HEAR = $0 for every status (DOE made HEAR
//     electric-to-electric; Jetson does gas-to-electric), so this is HEAR-free
//     by construction — no manual subtraction.
// y = MODELED install cost (Panorama still stores no per-market install price).
import { writeFileSync, readFileSync, unlinkSync } from "fs";
import { fileURLToPath, pathToFileURL } from "url";
import { dirname, resolve } from "path";

const SRC = process.env.PANORAMA_SRC
  || "/home/user/conductor-playground/project-panorama/src";
const { ALL_MARKETS } = await import(resolve(SRC, "data/markets.js"));
const { REBATE_DATA } = await import(resolve(SRC, "data/rebates.js"));
const { GENERATED_REBATES } = await import(resolve(SRC, "data/notion-rebates.generated.js"));
const OUT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "dataset.json");

// ── Resolve JEV exactly as the Panorama app does ─────────────────────────────
// The app overrides m.jevDollars before render (src/data/useNotionRebates.js):
//   effective = { ...RESEARCHED_OVERRIDES, ...GENERATED_REBATES.markets }
//   (CORRECTED_OVERRIDES intentionally NOT applied — awaiting rebates-team sign-off)
// then floor-merges: an override BELOW the legacy jev.js value is floored back to
// legacy unless the reduction is trusted. Without this the deck would plot the
// legacy fallback, not what the tool actually shows.
// useNotionRebates.js imports React, so load it with that import stripped.
const hookSrc = readFileSync(resolve(SRC, "data/useNotionRebates.js"), "utf8")
  .replace(/^\s*import\s+\{[^}]*\}\s+from\s+["']react["'];?\s*$/m, "");
// written beside the originals so its relative imports (./markets.js …) resolve
const shim = resolve(SRC, "data/__jev_shim.mjs");
writeFileSync(shim, hookSrc);
let RESEARCHED_OVERRIDES;
try {
  ({ RESEARCHED_OVERRIDES } = await import(pathToFileURL(shim).href));
} finally {
  try { unlinkSync(shim); } catch {}
}

const CONFIRMED_ZERO = new Set(["MKE"]);   // mirrors useNotionRebates.js
const isTrustedReduction = (m, r) =>
  r._source === "research" || r._source === "corrected" ||
  CONFIRMED_ZERO.has(m.id) ||
  (r.programs || []).some(p => (Number(p.jev) || 0) > 0);

const effective = { ...RESEARCHED_OVERRIDES, ...(GENERATED_REBATES?.markets || {}) };
let covered = 0, floored = 0;
for (const m of ALL_MARKETS) {
  const r = effective[m.id];
  if (!r) { m._rebateSource = "legacy"; continue; }
  const legacy = m.jevDollars;
  const override = r.jevDollars ?? 0;
  if (override < legacy && !isTrustedReduction(m, r)) { m.jevDollars = legacy; m._rebateFloored = true; floored++; }
  else { m.jevDollars = override; m._rebateFloored = false; }
  m._rebateSource = r._source || "notion";
  covered++;
}
console.log(`JEV resolution: ${covered} markets overridden (${floored} floored to legacy), ${ALL_MARKETS.length - covered} on legacy fallback`);

// ── Modeled install cost (NOT a Panorama field) ──
const BASE = 19000;
const COST_FACTOR = { Low: 0.78, Medium: 1.0, High: 1.22 };
const climateAdder = dd => (dd >= 6500 ? 1500 : dd >= 5000 ? 750 : 0);
const modeledInstall = (cost, dd) =>
  Math.round((BASE * (COST_FACTOR[cost] ?? 1.0) + climateAdder(dd)) / 100) * 100;

// 14 candidate markets → current Panorama id (all live now; no estimates)
const CAND = {
  "Raleigh-Durham": "RDU", "Salt Lake City": "SLC", "Portland": "POR",
  "Dallas": "DAL", "Austin": "AUS", "Charlotte": "CLT", "Seattle": "SEA",
  "Las Vegas": "LV", "Richmond": "RIC", "Westfield (NJ)": "WNJ",
  "Chicago North": "CHI_N", "Minneapolis": "MSP", "Philadelphia": "PHI",
  "Royal Oak Metro": "ROY",
};
const CAND_ID = new Set(Object.values(CAND));

// Licensed-model markets (shown as a distinct category, not amber candidates)
const LICENSED = { "Phoenix": "PHX", "Memphis": "MEM", "Providence": "PVD", "Hartford": "HARTFORD" };
const LIC_ID = new Set(Object.values(LICENSED));

const all = ALL_MARKETS.map(m => {
  const s = REBATE_DATA.stackable?.[m.id];
  const note = s?.note ?? null;
  return {
    id: m.id, name: m.name, state: m.state,
    x: m.jevDollars,                    // Panorama JEV $ (HEAR-free, risk-adjusted)
    y: modeledInstall(m.warehouseCost, m.degreeDays),
    tam: m.warehouseTam, tier: m.tier,
    kind: m.isExisting ? "existing" : "modeled",
    candidate: CAND_ID.has(m.id),
    licensed: LIC_ID.has(m.id),
    source: "panorama",
    rebateSource: m._rebateSource,       // notion | research | legacy
    floored: !!m._rebateFloored,
    riskFlag: !!(note && note.includes("⚠")),
    note,
  };
});

// Missing IDs (should be none)
const missingIds = [...Object.entries(CAND), ...Object.entries(LICENSED)]
  .filter(([,id]) => !all.some(a => a.id === id)).map(([n]) => n);

const roster = [
  ...Object.entries(CAND).map(([name, id]) => {
    const r = all.find(a => a.id === id);
    return { name, id, group: "candidate", x: r.x, y: r.y, tam: r.tam, tier: r.tier,
             kind: r.kind, riskFlag: r.riskFlag, note: r.note,
             rebateSource: r.rebateSource, floored: r.floored,
             pipeline: ["Portland", "Dallas"].includes(name) };
  }),
  ...Object.entries(LICENSED).map(([name, id]) => {
    const r = all.find(a => a.id === id);
    return { name, id, group: "licensed", x: r.x, y: r.y, tam: r.tam, tier: r.tier,
             kind: r.kind, riskFlag: r.riskFlag, note: r.note,
             rebateSource: r.rebateSource, floored: r.floored, pipeline: false };
  }),
];

writeFileSync(OUT, JSON.stringify({ all, roster, missing: missingIds }, null, 2));
console.log("wrote", OUT, "| markets:", all.length, "| candidates found:", roster.length,
            "| missing ids:", missingIds.join(", ") || "none");
console.log("candidate JEV$:", roster.map(r => `${r.name}=$${r.x}`).join("  "));
