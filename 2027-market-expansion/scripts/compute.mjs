// Sanity-print the live Panorama values behind Slide 1 (the 6 candidates that
// exist in Panorama). Read-only. Set PANORAMA_SRC or default to the monorepo clone.
import { resolve } from "path";
const SRC = process.env.PANORAMA_SRC || "/home/user/conductor-playground/project-panorama/src";
const { ALL_MARKETS } = await import(resolve(SRC, "data/markets.js"));
const { REBATE_DATA } = await import(resolve(SRC, "data/rebates.js"));

const CAND = { "Salt Lake City":"SLC","Portland":"POR","Dallas":"DAL",
  "Seattle":"SEA","Westfield (NJ)":"WNJ","Chicago North":"CHI_N" };

console.log("Live Panorama values (rebates.js stackable + federal HEAR status):\n");
for (const [name,id] of Object.entries(CAND)) {
  const m = ALL_MARKETS.find(x=>x.id===id);
  const s = REBATE_DATA.stackable[id];
  const fed = REBATE_DATA.federal[m.state];
  console.log(`${name.padEnd(16)} rebate $${s.low}–$${s.high}  W-TAM ${m.warehouseTam}  Tier ${m.tier}  HEAR=${fed?.status}  | ${s.note}`);
}
