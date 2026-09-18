# Heat Pump Permit Volume per Capita: Newark, Minneapolis, Charlotte, Phoenix

**Status (2026-09-18):** source map complete, pipeline built and tested on synthetic data,
**no live permit numbers yet.** The Claude Code session that built this had a network
policy that blocked every government open-data host (Census API, ArcGIS, Socrata,
CKAN, state portals). See "Unblocking" below. Nothing in this folder should be read as
a measured rate until `output/market_summary.csv` exists.

---

## 1. Answer to the original question

> Can heat pump permits per capita be pulled for these markets at 90% accuracy, and
> can permit type (mini-split vs. dual fuel vs. full heat pump) be identified?

| Market | Permit volume feasibility | Type feasibility | Why |
|---|---|---|---|
| **Minneapolis-St. Paul** | **Good** for the two core cities (about 730k people). Poor for suburbs. | Partial. Free-text scope field; expect 50-70% of heat pump permits to state ductless vs. ducted, far fewer to state dual fuel. | Minneapolis publishes every permit weekly as an ArcGIS layer with permit type, work type and a free-text scope. St. Paul has a Socrata feed that reportedly includes mechanical permits. About 70% of the metro lives in suburbs on the LOGIS ePermits system, which has no export. |
| **Charlotte** | **Good structurally, blocked practically.** One authority (Mecklenburg County) permits 1.2M people, and NC law requires a permit for every HVAC changeout. But the published open-data layer covers permits needing a certificate of occupancy and appears to exclude stand-alone trade changeouts. | **Best potential of the four**, via a data extract rather than open data. Mecklenburg attaches the NC Energy Code Appendix 5 HVAC compliance form to changeout permits, which records equipment type and capacity. | Changeout permits live in Accela as Mechanical Permit records, searchable with CSV export of a few hundred rows per query, or obtainable as an extract from LUESA Code Enforcement. Surrounding counties are portal-by-portal only. |
| **Phoenix** | **Good for Mesa, Tempe, Scottsdale, Gilbert** (about 1.2M people). **Bad for Phoenix city** (1.65M), which has no exportable permit feed. | Weak. Free-text descriptions only where present. | Phoenix's open-data "permits" dataset is HUD new-construction aggregates. Its current SHAPE PHX system has per-record search only. A legacy PDD export may still work. Bigger issue: heat pumps are already the default system in about a quarter of Arizona homes, so this metric measures HVAC replacement volume, not adoption. Compliance for like-kind changeouts is believed to be very low. |
| **Newark** | **Poor.** No city permit dataset. State reporting is municipality-month aggregates with no equipment detail. | **Not feasible** from public data. | NJ treats like-capacity HVAC replacement as "minor work" (N.J.A.C. 5:23-2.17A): notice, start work, permit issued after the fact. These become thin subcode tickets in each town's Spatial Data Logic or GovPilot system. One unknown: the statewide `NJ Construction Permit Data` Socrata dataset on data.nj.gov, whose schema could not be inspected. |

**Decision (2026-09-18).** The target is heat pump permit activity as a whole, not full
system installs, used as one of several demand signals. Type breakdown is a nice-to-have
reported as a range where text supports it. Coverage is the priority, which points to
Shovels for the raw permit feed (with this classifier run on their description text,
not their pre-built heat pump tag, which validated at roughly 5% recall in Philadelphia).

**Accuracy verdict.** Permit *volume* in covered jurisdictions: 80-90% achievable for
Minneapolis, St. Paul, Mesa, Tempe, Scottsdale, Gilbert, and Mecklenburg once the
extract is obtained. Below that for any metro-wide figure because of coverage gaps.
Permit *type*: not achievable at 90% anywhere from permit text. Ranges, not points.
Permits as a proxy for *installs*: never at 90%. No state here has a compliance study,
and the California literature puts residential HVAC changeout permitting between 8%
and 35%.

**Cross-market comparability warning.** The four markets have four different permit
regimes. Minnesota and North Carolina require a full permit for every changeout.
Arizona requires one but enforcement is weak. New Jersey does not require one before
work starts. A raw per-capita comparison would rank permit culture, not heat pump
demand. Report each market against its own trend and against utility rebate counts.

---

## 2. Source map (from `pipeline/sources.yaml`)

Verified means the endpoint and field names were confirmed against the live API.
Nothing is verified yet. Endpoints were located from search results only.

### Minneapolis-St. Paul
- **Minneapolis CCS Permits**, ArcGIS FeatureServer, weekly. Fields confirmed by the
  portal's own description: `PermitType`, `WorkType`, `Comments` (free-text scope).
  `https://services.arcgis.com/afSMGVsC7QlRK1kZ/arcgis/rest/services/CCS_Permits/FeatureServer/0`
- **St. Paul Approved Building Permits**, Socrata `j8ip-eytd` on information.stpaul.gov.
  Reportedly includes mechanical permits, 2013 or 2015 to present. Fields unconfirmed.
- **Suburbs**: LOGIS ePermits (Edina, Eden Prairie, Minnetonka, Maple Grove, Eagan,
  Bloomington, Burnsville, Woodbury and others). Per-address search only. Needs a
  Data Practices Act request per city.
- **Calibration**: MN ASHP Collaborative "State of the Market" (HARDI shipment data:
  ducted heat pumps went from 6% of Minnesota cooling sales in 2023 to 17% in 2025;
  ducted passed ductless in 2024). CenterPoint's only heat pump rebate is for a ducted
  heat pump paired with a gas furnace, so its participation count is a direct
  dual-fuel proxy. Xcel and CenterPoint annual ECO status reports on MN PUC eDockets.

### Charlotte
- **Mecklenburg County** issues all building and trade permits for Charlotte and six
  towns. Changeouts go through Trade Internet Permitting (TIP) at a flat fee.
  - Accela public search: `https://aca-prod.accela.com/Mecklenburg/`
  - Open Mapping "Building Permits" layer: CO-requiring permits, likely no changeouts.
  - Forms attached to changeouts: NC Appendix 5 Statement of Compliance for HVAC
    System Installation, and an HVAC Change-out Compliance Form. These carry equipment
    type. Ask Code Enforcement whether the fields are captured in Accela, not just PDFs.
- **Cabarrus County**: Accela plus ArcGIS Hub with annual permit layers. Worth checking.
- **Union, Gaston, Iredell, York SC**: Evolve, EnerGov, BS&A portals. No export.
- **Calibration**: Duke Energy Smart $aver HVAC filings (NCUC docket E-7), program-year
  participant counts, possibly ductless as a separate measure. No county breakdown.

### Phoenix
- **Mesa**: Socrata `m2kk-w2hz` on data.mesaaz.gov, "Building Permits (Commercial,
  Residential and Signs)", has a "Description of work" column, updated Sept 2026.
  First check: are stand-alone mechanical permits in the extract at all.
- **Tempe**: ArcGIS Hub item `55b38626464d48cb94e81cb8227d6fde_0`, extracted from Accela.
- **Scottsdale**: ArcGIS Hub item `68ba7b38073f4cd4aee38d2b59afcaf4_12`. Changeouts appear
  to be filed under "MINIMUM (…)" permit types.
- **Gilbert**: ArcGIS Hub item `cba4345453f94ca5881b7727f069a431_3`, all permits since 2003.
- **Phoenix city**: no export. Try legacy PDD "Issued Permits" CSV export at
  `apps-secure.phoenix.gov/PDD/Search/IssuedPermit`; otherwise records request.
- **Chandler, Glendale, Peoria, Surprise, Goodyear, Buckeye, Queen Creek, County**:
  record-lookup portals only.
- **Calibration**: APS ended residential efficiency rebates 1 Jan 2026, so its DSM
  filings stop being useful after 2025. SRP Cool Cash publishes no unit counts.
  EIA RECS 2020: 25% of Arizona homes heat with a central heat pump, 51% electric.

### Newark
- **NJ Construction Permit Data**, Socrata `w9se-dmra` on data.nj.gov. Schema unknown.
  Probe this first; it decides whether the market has any free source.
- **NJ DCA Construction Reporter / Permit Activity Dashboard**: municipality-month
  counts and dollars by new / addition / alteration. No subcode, no equipment.
- **Newark city**: CO datasets only on data.ci.newark.nj.us. OPRA request needed.
- **Suburbs**: Bloomfield and Montclair on Spatial Data Logic (per-address lookup).
  Jersey City, Elizabeth on GovPilot (intake only). Others unknown.
- **Calibration**: NJ Clean Energy Program and PSE&G quarterly reports, by utility
  territory. No municipality breakdown found.

---

## 3. How the pipeline works

```
pipeline/
  sources.yaml     one entry per jurisdiction: endpoint, field mapping, notes, fallback population
  fetch.py         Socrata / ArcGIS FeatureServer / CSV fetchers, paginated, cached, probe helpers
  classify.py      rules-based classifier: is_heat_pump (True/False/None) and system_type
  population.py    Census ACS 1-year denominators (population, housing units, single-family units)
  run.py           orchestrates fetch -> normalise -> classify -> trailing 12/36 month rates
tests/
  test_classify.py 45 description cases modelled on real permit text
  test_run.py      end-to-end run on tests/fixtures/sample_permits.csv
```

```bash
cd analysis/heat-pump-permits
pip install -r requirements.txt
python -m pytest tests -q            # 46 tests, all offline
python -m pipeline.run --probe       # print every endpoint's real field names; fix sources.yaml
python -m pipeline.run               # full run -> output/market_summary.csv, .md, permits_classified.csv
```

**Signal definition.** Any permit whose text mentions heat pump work counts, whatever
the permit type. An electrical service upgrade with a "heat pump" note is a signal. The
summary breaks confirmed signals out by the permit type that carried them (mechanical,
electrical, other) so the electrical share can be read as a rough proxy for
electrification-driven work versus like-kind changeouts. This is a demand indicator,
not an install count, and sits alongside the other demand signals in the market model.

**Classifier behaviour that drives the numbers.** Each permit with a description gets
one of three verdicts. *Heat pump* when the text says heat pump, HSPF, mini-split, ductless,
geothermal, a ductless brand, or "HP" alongside HVAC context. *Not heat pump* when it
names a gas furnace, boiler, straight-cool AC, water heater, pool, or ductwork only.
*Ambiguous* when it is clearly HVAC ("replace 3 ton condenser and coil") but names no
equipment type. Heat pump water heaters and pool heat pumps are excluded. The summary
reports a low bound (confirmed) and a high bound (confirmed plus ambiguous). System type
is ductless, dual fuel (furnace mentioned), ducted (air handler, split system, package,
tonnage), or unknown.

**Denominators.** Population, total housing units, and single-family units (ACS
B25024 1-unit detached plus attached). Single-family units is the recommended
comparator because Newark's 2-4 family stock and Phoenix's detached stock differ so
much. Fallback populations in `sources.yaml` are approximate 2023 estimates written
from memory and are replaced by the Census API on any networked run.

---

## 4. Unblocking

The session's network egress policy denied every one of these hosts. To run the
pipeline from Claude Code on the web, add them to the environment's allowed domains
(see https://code.claude.com/docs/en/claude-code-on-the-web), or run it from a laptop.

```
api.census.gov
services.arcgis.com  services1.arcgis.com  hub.arcgis.com
information.stpaul.gov  data.mesaaz.gov  data.nj.gov
data.tempe.gov  data.scottsdaleaz.gov  data-tog.opendata.arcgis.com
opendata.minneapolismn.gov  maps.mecknc.gov  gis-cabarrus.opendata.arcgis.com
aca-prod.accela.com  apps-secure.phoenix.gov
```

---

## 5. Recommended sequence once unblocked

1. `--probe` every endpoint. Fix field names in `sources.yaml`. Confirm mechanical
   permits are present in Mesa, St. Paul, Tempe, Scottsdale, Gilbert extracts.
2. Run Minneapolis first. It is the cleanest source and calibrates the classifier:
   pull 200 random ambiguous permits and 200 confirmed, hand-label, report precision
   and recall. Adjust patterns. This is where the "90%" claim gets tested.
3. Open the data.nj.gov `w9se-dmra` schema. If it is aggregates, drop Newark to a
   state-aggregate proxy and say so.
4. Request the Mecklenburg extract (permit subtype, issue date, description, Appendix 5
   fields). Ask specifically whether equipment type is a database field. This is the
   only route to a real mini-split / dual fuel / full-system split in any market.
5. Test the Phoenix legacy PDD CSV export. If dead, file a records request.
6. Pull utility rebate counts (CenterPoint dual fuel, Xcel, Duke Smart $aver, NJCEP)
   as the type-mix cross-check, and present type as a range per market.

---

## 6. Sources consulted

Search results only. No page was fetched.

Newark: [Newark Open Data](https://data.ci.newark.nj.us/), [NJ Construction Permit Data](https://data.nj.gov/Reference-Data/NJ-Construction-Permit-Data/w9se-dmra), [DCA Construction Reporter](https://www.nj.gov/dca/codes/reporter/), [DCA Permit Activity Dashboard](https://datahub.dca.nj.gov/datasets/permit-activity-dashboard/about), [N.J.A.C. 5:23-2.17A](https://www.law.cornell.edu/regulations/new-jersey/N-J-A-C-5-23-2-17A), [NJCEP reports](https://cleanenergy.nj.gov/resources/njcep-reports).

Minneapolis: [CCS Permits](https://opendata.minneapolismn.gov/datasets/ccs-permits), [Minneapolis mechanical permits](https://www.minneapolismn.gov/business-services/licenses-permits-inspections/construction-permits/permits-overview/permit-types/mechanical-heating-permits/), [St. Paul permits dataset](https://information.stpaul.gov/Buildings-Housing-Economic-Development/Approved-Building-Permits-Dataset/j8ip-eytd), [LOGIS ePermits](https://epermits.logis.org/default.aspx), [MN Rules 1300.0120](https://www.revisor.mn.gov/rules/1300.0120/), [MN ASHP State of the Market](https://www.mnashp.org/heat-pump-state-market-report), [CenterPoint ducted ASHP rebate](https://www.centerpointenergy.com/en-us/SaveEnergyandMoney/Pages/Ducted-Air-Source-Heat-Pump-Rebate.aspx?sa=MN&au=bus).

Charlotte: [Mecklenburg Code Enforcement](https://code.mecknc.gov/), [TIP](https://code.mecknc.gov/permitting/tip), [Building Permits layer metadata](https://maps.mecknc.gov/opendata/metadata/BuildingPermits.html), [Accela Mecklenburg](https://aca-prod.accela.com/Mecklenburg/Home.html), [G.S. 160D-1110](https://www.ncleg.gov/EnactedLegislation/Statutes/HTML/BySection/Chapter_160D/GS_160D-1110.html), [Cabarrus open data](https://gis-cabarrus.opendata.arcgis.com/), [Duke Smart $aver HVAC](https://www.duke-energy.com/home/products/smart-saver/hvac-install).

Phoenix: [Phoenix building permit data](https://www.phoenixopendata.com/dataset/phoenix-az-building-permit-data), [PDD Issued Permits](https://apps-secure.phoenix.gov/PDD/Search/IssuedPermit), [SHAPE PHX](https://shapephx.phoenix.gov/s/), [Phoenix AC replacement guideline](https://www.phoenix.gov/content/dam/phoenix/pddsite/documents/trt/external/dsd_trt_pdf_00687.pdf), [Mesa permits](https://data.mesaaz.gov/Development-Services/Building-Permits-Commercial-Residential-and-Signs-/m2kk-w2hz), [Tempe permits](https://data.tempe.gov/datasets/tempegov::permits-issued-by-building-safety/about), [Scottsdale permits](https://data.scottsdaleaz.gov/datasets/planning-and-development-building-permits), [Gilbert permits](https://data-tog.opendata.arcgis.com/datasets/cba4345453f94ca5881b7727f069a431_3/about), [EIA RECS 2020 state space heating](https://www.eia.gov/consumption/residential/data/2020/state/pdf/State%20Space%20Heating.pdf).

Compliance and aggregators: [CalMAC HVAC permit study](https://www.calmac.org/publications/HVAC_WO6_FINAL_REPORT_VolumeI_22Sept2017.pdf), [NRDC on unpermitted HVAC](https://www.nrdc.org/bio/kiki-velez/poor-quality-hvac-installs-are-costing-us-solution-within-reach), [Shovels heat pump tag validation](https://github.com/davidjdevine/shovels-heatpump-validation).
