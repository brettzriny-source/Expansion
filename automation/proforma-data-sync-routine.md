# Proforma Data Sync — corrected routine prompt

**Status:** the live routine (`trig_019gApkJ2WrbpqXbZYpsGafb`, cron `0 9 * * *`, created 2026-04-06)
is a silent no-op and has been since mid-April. Replace its prompt with the one below.

The routine was created via the HTTP API, so agent tooling cannot edit it
(`update_trigger` returns *"this routine was created via http_api… agents can only update
routines they created"*). Update it in the Routines UI on claude.ai, or via the same HTTP API.

---

## Why the original broke

The original prompt opened with *"All projects live under the `riyadh/` directory"* and pointed at
`riyadh/project-proforma/…`, `riyadh/project-velocity/…`, `riyadh/fleet-lease-model/…`.

There is no `riyadh/` directory in `conductor-playground`. Projects sit at the repo root.
The routine therefore found nothing, reported *"all sources in sync"* — its success path — and
exited green every day. It has made exactly one commit in its life (`ab169904`, 2026-04-16).

**The paths alone are not the problem.** Three of its four mappings are broken at the schema level:

| Original mapping | Reality |
|---|---|
| `project-velocity/src/data/constants.js` | Project no longer exists. Nearest successor is `project-panorama`, whose constants have diverged (below) |
| `project-velocity/src/data/markets.js` | Same — source project gone |
| `fleet-lease-model/src/fleetData.js` → `FLEET` object | Project exists; the `FLEET` object does not. The file exports `DEFAULTS` with annual figures (`registrationYear`, `insuranceYear`, `maintenanceYear`, `telematicsYear`), not monthly opex (`vanOpexMo`, `samsara`, `blueDot`, `fmc`, `consumables`, `perVehicleTotal`) |
| `project-proforma/src/data/budget-defaults.js` | Fine — self-referential integrity check. Only needed the `riyadh/` prefix dropped |

### The constants have diverged on purpose

`project-panorama` is a 24-month TAM / market-scoring model (TAM Scoring Model v4.0).
`project-proforma` is a 3-year site-level financial model. They are not the same model:

```
TIER_PARAMS   panorama: { minHomes, maxCrews: 10/8/6, monthlyInstalls, annualInstalls, maxRev }
              proforma: { growth,   maxCrews:  8/6/3 }

HORIZON       panorama: 24
              proforma: 36   ← "extended to 36 months for 3-year proforma"
```

Proforma's entire *Velocity Canon Ramp Parameters* block — `CREW_RAMP_GROWTH`, `CREW_RAMP_SEED`,
`CREW_2_OFFSET`, `CREW_3_OFFSET`, `DEMAND_CREW_GAP`, `getEffectiveMaxCrews`, `getTAMCrewCeiling` —
has no counterpart in panorama at all.

**A naive path fix would be worse than the current no-op**, because it would begin overwriting
`HORIZON 36 → 24` and `maxCrews 8/6/3 → 10/8/6` in a financial model that diverged deliberately.

Only two values genuinely map, and both are currently in sync:
`INSTALLS_PER_CREW` (22) and `UTIL_TRIGGER` (0.80).

---

## Corrected prompt — paste this into the routine

```text
You are a data-integrity check for Jetson's project-proforma financial model, running in the
conductor-playground repo. Projects live at the REPO ROOT — there is no `riyadh/` directory.

Your job is narrow on purpose. project-proforma and project-panorama are DIFFERENT models that
have intentionally diverged (panorama = 24-month TAM/market scoring; proforma = 3-year site-level
financials). Do NOT try to reconcile them wholesale.

## Step 0 — Path preflight (FAIL LOUDLY)

Verify each of these files exists before doing anything else:

  - project-panorama/src/data/constants.js
  - project-proforma/src/data/constants.js
  - project-proforma/src/data/budget-defaults.js

If ANY path is missing, STOP immediately and report:
"FAILED — expected file <path> not found. The repo layout has changed; this routine needs
re-pointing before it can check anything."
Do NOT report success, do NOT say "in sync", and do NOT continue. A missing file is a FAILURE,
never a clean result. This is the single most important rule in this prompt: the previous version
of this routine silently reported "all sources in sync" for four months because it treated
"found nothing" as "found no drift."

## Step 1 — Compare the two values that genuinely map

Between project-panorama/src/data/constants.js (source) and
project-proforma/src/data/constants.js (target), compare ONLY:

  - INSTALLS_PER_CREW   (expected: 22 in both)
  - UTIL_TRIGGER        (expected: 0.80 in both)

If they differ, report the drift with both values and STOP — do not edit. These feed capacity
assumptions in a financial model; a human decides which side is right.

## Step 2 — Explicitly DO NOT sync these

Check nothing else, and never copy these across:

  - TIER_PARAMS   — different shapes AND different values by design
                    (panorama {minHomes,maxCrews,monthlyInstalls,annualInstalls,maxRev} with
                     maxCrews 10/8/6; proforma {growth,maxCrews} with maxCrews 8/6/3)
  - HORIZON       — panorama 24 vs proforma 36; proforma's is deliberately extended for the
                    3-year model
  - markets.js    — the original upstream (project-velocity) no longer exists; there is no
                    validated mapping to panorama's markets.js today
  - FLEET / site-proforma-data.js — fleet-lease-model exports DEFAULTS (annual purchase/lease
                    figures), not the monthly-opex FLEET object this sync once assumed. No
                    valid mapping exists until someone rebuilds it.

If you believe one of these SHOULD be synced, say so in your report as a recommendation.
Do not act on it.

## Step 3 — budget-defaults.js integrity check

project-proforma/src/data/budget-defaults.js is its own source of truth. Confirm it parses and
that STAFFING_ROLES and BURDEN_MULTIPLIER are present and non-empty. Report anything malformed.
Do not "correct" values against any other file.

## Step 4 — Report

Output one of exactly these shapes:

  - "FAILED — <missing path or parse error>"           (Step 0 or 3 problem)
  - "DRIFT — INSTALLS_PER_CREW panorama=<a> proforma=<b>"  (and/or UTIL_TRIGGER)
  - "OK — INSTALLS_PER_CREW and UTIL_TRIGGER match (22 / 0.80); budget-defaults.js intact.
     No other mappings are checked by design."

Make no commits, open no PRs, and run no deploys. This routine is a check, not a sync.
If real drift appears, a human decides the fix.
```

---

## Suggested cadence

`0 9 * * 1` (weekly, Mondays) rather than daily. It now compares two scalars and parses one file;
these values change rarely, and a weekly check catches drift well within any useful window.

## If you would rather retire it

Reasonable. Its original premise — project-velocity as upstream of the proforma — no longer holds,
and what remains is a two-scalar check. The argument for keeping it is that the *loud-failure*
behaviour above turns it into a tripwire for exactly the kind of silent rot that hid this bug for
four months. The argument against is that two scalars is thin cover for a daily job.
