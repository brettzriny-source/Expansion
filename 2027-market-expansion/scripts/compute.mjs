// Sanity-print the live Panorama JEV values behind Slide 1 for the 14 candidates.
// Read-only. Set PANORAMA_SRC or default to the monorepo clone (rebate-recast/JEV build).
import { resolve } from "path";
const SRC = process.env.PANORAMA_SRC || "/home/user/conductor-playground/project-panorama/src";
const { ALL_MARKETS } = await import(resolve(SRC, "data/markets.js"));

const CAND = { RDU:"Raleigh-Durham", SLC:"Salt Lake City", POR:"Portland", DAL:"Dallas",
  AUS:"Austin", CLT:"Charlotte", SEA:"Seattle", LV:"Las Vegas", RIC:"Richmond",
  WNJ:"Westfield (NJ)", CHI_N:"Chicago North", MSP:"Minneapolis", PHI:"Philadelphia", ROY:"Royal Oak Metro" };

console.log(`Panorama markets loaded: ${ALL_MARKETS.length}. JEV $ (jevDollars) for the 14 candidates:\n`);
for (const [id, label] of Object.entries(CAND)) {
  const m = ALL_MARKETS.find(x => x.id === id);
  if (!m) { console.log(`${label.padEnd(16)} — id ${id} NOT FOUND`); continue; }
  console.log(`${label.padEnd(16)} [${id}] JEV $${String(m.jevDollars).padStart(5)}  W-TAM ${m.warehouseTam}  Tier ${m.tier}${m.isExisting ? "  (existing)" : ""}`);
}
