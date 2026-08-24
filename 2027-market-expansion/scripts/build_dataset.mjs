// Build the plot dataset from the LIVE Panorama tool (rebate-recast / JEV model).
// x = m.jevDollars  — Panorama's risk-adjusted rebate value a Jetson customer
//     actually captures. Federal HEAR = $0 for every status (DOE made HEAR
//     electric-to-electric; Jetson does gas-to-electric), so this is HEAR-free
//     by construction — no manual subtraction.
// y = MODELED install cost (Panorama still stores no per-market install price).
import { writeFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, resolve } from "path";

const SRC = process.env.PANORAMA_SRC
  || "/home/user/conductor-playground/project-panorama/src";
const { ALL_MARKETS } = await import(resolve(SRC, "data/markets.js"));
const { REBATE_DATA } = await import(resolve(SRC, "data/rebates.js"));
const OUT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "dataset.json");

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
    source: "panorama",
    riskFlag: !!(note && note.includes("⚠")),
    note,
  };
});

// Missing IDs (should be none)
const missingIds = Object.entries(CAND).filter(([,id]) => !all.some(a => a.id === id)).map(([n]) => n);

const roster = Object.entries(CAND).map(([name, id]) => {
  const r = all.find(a => a.id === id);
  return { name, id, source: "panorama", x: r.x, y: r.y, tam: r.tam, tier: r.tier,
           kind: r.kind, riskFlag: r.riskFlag, note: r.note,
           pipeline: ["Portland", "Dallas"].includes(name) };
});

writeFileSync(OUT, JSON.stringify({ all, roster, missing: missingIds }, null, 2));
console.log("wrote", OUT, "| markets:", all.length, "| candidates found:", roster.length,
            "| missing ids:", missingIds.join(", ") || "none");
console.log("candidate JEV$:", roster.map(r => `${r.name}=$${r.x}`).join("  "));
