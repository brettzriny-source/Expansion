// Build the combined plot dataset: live Panorama rows + 5 estimated markets.
// Reads Panorama source (set PANORAMA_SRC env, or defaults to the monorepo clone).
// Writes ../dataset.json.
import { writeFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, resolve } from "path";

const SRC = process.env.PANORAMA_SRC
  || "/home/user/conductor-playground/project-panorama/src";
const { ALL_MARKETS } = await import(resolve(SRC, "data/markets.js"));
const { REBATE_DATA } = await import(resolve(SRC, "data/rebates.js"));
const OUT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "dataset.json");

// ── Modeled install cost (NOT a Panorama field — clearly labeled MODELED) ──
// national base × regional cost factor (Panorama warehouseCost proxy) + cold-climate adder (degree-days)
const BASE = 19000;
const COST_FACTOR = { Low: 0.78, Medium: 1.0, High: 1.22 };
const climateAdder = dd => (dd >= 6500 ? 1500 : dd >= 5000 ? 750 : 0);
const modeledInstall = (cost, dd) =>
  Math.round((BASE * (COST_FACTOR[cost] ?? 1.0) + climateAdder(dd)) / 100) * 100;

// candidate name -> panorama id (null = not in Panorama)
const CAND = {
  "Raleigh-Durham": null, "Salt Lake City": "SLC", "Portland": "POR",
  "Dallas": "DAL", "Austin": null, "Charlotte": null, "Seattle": "SEA",
  "Las Vegas": null, "Richmond": null, "Westfield (NJ)": "WNJ", "Chicago North": "CHI_N",
  "Minneapolis": "MSP",
};
const CAND_ID = new Set(Object.values(CAND).filter(Boolean));

// ── Market-rate stack: strip the income-qualified $8k HEAR (HEEHRA, ≤150% AMI) ──
// HEAR does not reach Jetson's market-rate customers, so it's excluded from the
// plotted rebate stack. Panorama bakes HEAR into stackable.high; we subtract the
// $8k HEAR line ONLY where the stack note actually carries it (regex guards against
// docking e.g. MA's Mass Save, whose note reads "HEAR not separately launched").
const HEAR8 = /HEAR \$8K/i;
const marketRate = (high, note) =>
  high == null ? null : (note && HEAR8.test(note) ? Math.max(0, high - 8000) : high);

const base = ALL_MARKETS.map(m => {
  const s = REBATE_DATA.stackable[m.id];
  const fed = REBATE_DATA.federal[m.state];
  return {
    id: m.id, name: m.name, state: m.state,
    x: marketRate(s?.high, s?.note),          // market-rate stack, HEAR excluded
    xFull: s?.high ?? null,                    // Panorama's full stack incl. HEAR (reference only)
    hearInStack: !!(s?.note && HEAR8.test(s.note)),
    rebateLow: s?.low ?? null, rebateNote: s?.note ?? null,
    y: modeledInstall(m.warehouseCost, m.degreeDays),
    tam: m.warehouseTam, tier: m.tier,
    kind: m.isExisting ? "existing" : "modeled",
    hear: fed?.status ?? "none",
    candidate: CAND_ID.has(m.id), source: "panorama",
  };
});

const missing = base.filter(b => b.x == null).map(b => `${b.name} (${b.id})`);

// 5 estimated markets — grounded in each state's HEAR framework + nearest Panorama analog
const estimated = [
  { name:"Raleigh-Durham", state:"NC", x:9000,  rebateLow:500,  y:modeledInstall("Medium",3400), hear:"live",    analog:"Asheville/Greenville (Duke Carolinas $1K + NC HEAR $8K, live)" },
  { name:"Austin",         state:"TX", x:2500,  rebateLow:500,  y:modeledInstall("Low",2600),    hear:"none",    analog:"Dallas (Austin Energy muni ~$2.5K; no HEAR in TX)" },
  { name:"Charlotte",      state:"NC", x:9000,  rebateLow:500,  y:modeledInstall("Medium",3200), hear:"live",    analog:"Asheville (Duke Carolinas $1K + NC HEAR $8K, live)" },
  { name:"Las Vegas",      state:"NV", x:11200, rebateLow:1000, y:modeledInstall("Low",2700),    hear:"pending", analog:"Reno (NV Energy PowerShift $3.2K + NV HEAR $8K, pending)" },
  { name:"Richmond",       state:"VA", x:8050,  rebateLow:50,   y:modeledInstall("Medium",3900), hear:"pending", analog:"Fairfax (Dominion $50 + VA HEAR $8K, pending)" },
].map(e => ({ id:"EST_"+e.name.replace(/\W/g,"").toUpperCase(), ...e, kind:"candidate",
             candidate:true, source:"estimated", tam:null, tier:null, rebateNote:e.analog,
             xFull:e.x, hearInStack:HEAR8.test(e.analog),
             x:marketRate(e.x, e.analog) }));   // market-rate: HEAR stripped from estimates too

const all = [...base, ...estimated];

const roster = Object.entries(CAND).map(([name,id]) => {
  const rec = id ? base.find(b=>b.id===id) : estimated.find(e=>e.name===name);
  return { name, id, source: rec.source, x: rec.x, xFull: rec.xFull, hearInStack: rec.hearInStack,
           y: rec.y, hear: rec.hear, tam: rec.tam ?? null, tier: rec.tier ?? null,
           pipeline: ["Portland","Dallas"].includes(name), note: rec.rebateNote };
});

writeFileSync(OUT, JSON.stringify({ all, roster, missing }, null, 2));
console.log("wrote", OUT);
console.log("plotted rows:", all.filter(a=>a.x!=null).length, "| missing rebate data:", missing.join(", ")||"none");
