# 2.1 Master Launch Timeline

> 📋 The single-source schedule for every phase, milestone, and dependency in a market launch.

## Purpose

This section translates the Smartsheet Gantt chart into a structured playbook reference — every phase, every task, every dependency, every critical-path item, in one place. It is the bridge between the project management tool (Smartsheet) and the governance framework (RACI, readiness gates, handoff criteria) in the rest of this playbook.

Use this section to:
- Understand the full launch timeline from market assessment through post-launch scaling
- Identify critical-path items that drive the launch date
- See dependencies between phases (and where parallel work is possible)
- Flag at-risk items that need proactive management

> 💡 **Core rule:** The critical path drives the launch date. Every item marked as critical path below is a potential launch-date mover. If a critical-path task slips, the launch date slips — unless the Market Launch Lead finds a way to compress downstream work. Manage the critical path daily.

---

## Timeline Overview

| Phase | Description | Start | Finish | Duration | Parallel? |
|-------|-------------|-------|--------|----------|-----------|
| **Phase 1** | Market Assessment | 12/29/25 | 01/09/26 | 10 days | Kickoff — sequential |
| **Phase 2** | Real Estate | 01/01/26 | 02/20/26 | 37 days | Overlaps Phase 1 |
| **Phase 3** | Compliance & Business Set Up | 02/02/26 | 02/20/26 | 15 days | Parallel with Phases 2, 4, 5 |
| **Phase 4** | Talent Launch | 01/26/26 | 03/16/26 | 36 days | Parallel with Phases 2, 3, 5 |
| **Phase 5** | Facility Set-Up | 02/09/26 | 03/17/26 | 27 days | Parallel with Phases 3, 4 |
| **Phase 6** | Physical Deployment | 02/02/26 | 04/20/26 | 56 days | Parallel — longest phase |
| **Phase 7** | Sales Enablement | 01/26/26 | 02/04/26 | 8 days | Parallel with Phases 2–5 |
| **Phase 8** | Operations Launch | 03/16/26 | 03/16/26 | 1 day | Go-live milestone |
| **Phase 9** | Post-Launch Scaling | 03/17/26 | 06/03/26 | 57 days | Post-launch — sequential |

**Total timeline: ~23 weeks (12/29/25 through 06/03/26)**

---

## Phase 1 — Market Assessment (12/29/25 – 01/09/26)

*Duration: 10 days | All items on critical path*

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 1.1 | Warehouse location/zip code assessment | Expansion/Ops | 12/29/25 | 12/31/25 | 3 | — | **Y** | |
| 1.2 | Rebate identification | Finance | 01/01/26 | 01/02/26 | 2 | 1.1 | **Y** | |
| 1.3 | Loan identification | Finance | 01/01/26 | 01/02/26 | 2 | 1.1 | **Y** | |
| 1.4 | License requirements identification | Expansion/Ops | 01/01/26 | 01/02/26 | 2 | 1.1 | **Y** | |
| 1.5 | Confirm launch installation volume targets | Expansion/Ops | 01/01/26 | 01/07/26 | 5 | 1.1 | **Y** | |
| 1.6 | Confirm capex/opex budget and approval gates | Expansion/Finance | 01/01/26 | 01/07/26 | 5 | 1.1 | **Y** | |
| 1.7 | Market launch charter and budget approval | Expansion/Ops | 01/01/26 | 01/09/26 | 7 | 1.1 | **Y** | **Y** |

> **Key dependencies:** Task 1.1 (warehouse location assessment) gates everything else. Tasks 1.2–1.6 run in parallel after 1.1. Task 1.7 (charter approval) is the phase gate — nothing moves to Phase 2 without it.

> **At-risk item:** Charter and budget approval (1.7) — requires leadership alignment on budget and volume targets. If Finance or leadership review cycles slip, this delays the entire cascade.

**Playbook cross-reference:** Phase 1 maps to **Section 1.2 RACI Phase 1 — Market Identification & Greenlight**. The VP of Expansion is Accountable for the greenlight decision.

---

## Phase 2 — Real Estate (01/01/26 – 02/20/26)

*Duration: 37 days | Critical path runs through lease negotiation and warehouse occupancy*

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 2.1 | Interview local broker | Expansion | 01/01/26 | 01/02/26 | 2 | 1.1 | **Y** | |
| 2.2 | Receive 1st warehouse survey from local broker | Expansion | 01/05/26 | 01/08/26 | 4 | 2.1 | | |
| 2.3 | Return comments on warehouse survey | Expansion | 01/09/26 | 01/09/26 | 1 | 2.2 | | |
| 2.4 | Finalize list of ~5 warehouse sites for tours | Expansion | 01/12/26 | 01/16/26 | 5 | 2.3 | | |
| 2.5 | Warehouse tours | Expansion | 01/19/26 | 01/20/26 | 2 | 2.4 | **Y** | |
| 2.6 | Define and present site racking, layout, parking, and EV charger plan | Expansion/Supply Chain | 01/21/26 | 01/22/26 | 2 | 2.5 | | |
| 2.7 | Lease negotiation to execution | Expansion/Finance | 01/21/26 | 02/05/26 | 12 | 2.5 | **Y** | **Y** |
| 2.8 | Facility insurance set-up and security deposit | Finance | 02/06/26 | 02/12/26 | 5 | 2.7 | | |
| 2.9 | Warehouse occupancy | Expansion/Ops | 02/19/26 | 02/19/26 | 1 | 2.8 FS+4d | **Y** | **Y** |

> **Key dependencies:** Lease execution (2.7) is the longest single task and sits on the critical path. Warehouse occupancy (2.9) has a 4-day lag after insurance — this is the buffer for move-in prep. Everything in Phases 5 and 6 depends on occupancy.

> **At-risk items:** Lease negotiation (2.7) — 12-day window is tight for commercial lease negotiation, especially if landlord pushback or legal review cycles extend. Warehouse occupancy (2.9) — if lease slips, occupancy slips, and the entire downstream schedule compresses.

> ⚠️ **Operational lesson (from Section 1.2):** "Lease signed" ≠ "warehouse ready." The gap between 2.7 (lease execution) and 2.9 (occupancy) includes insurance and deposit only. Racking, IT, and stocking happen in Phases 5–6 *after* occupancy. The Market Launch Lead must track this chain daily.

**Playbook cross-reference:** Maps to **Section 1.2 RACI Phase 2 — Market Launch Planning** and **Section 1.4 Readiness Gate domain B (Facility & Warehouse Readiness)**. Criteria F-1 through F-5 depend on Phase 2 completion.

---

## Phase 3 — Compliance & Business Set Up (02/02/26 – 02/20/26)

*Duration: 15 days | All items on critical path*

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 3.1 | Business license applications | Expansion/Ops | 01/30/26 | 02/05/26 | 5 | 2.7 FS-5d | **Y** | |
| 3.2 | Contractor/home improvement license applications | Expansion/Ops | 02/13/26 | 02/19/26 | 5 | 3.1 FS+5d | **Y** | |
| 3.3 | Rebate/preferred contractor applications | Expansion/Ops | 02/13/26 | 02/19/26 | 5 | 3.1 FS+5d | **Y** | |
| 3.4 | Loan partner set-up | Finance | 02/13/26 | 02/19/26 | 5 | 3.1 FS+5d | **Y** | |

> **Key dependencies:** Business license applications (3.1) start 5 days *before* lease execution finishes — deliberate overlap to compress the schedule. Tasks 3.2–3.4 run in parallel after a 5-day lag from 3.1. Licensing timelines are jurisdiction-dependent and can vary significantly.

**Playbook cross-reference:** Maps to **Section 1.4 Readiness Gate domain A (Legal & Entity Readiness)**. Criteria L-1 through L-4 depend on Phase 3 completion.

---

## Phase 4 — Talent Launch (01/26/26 – 03/16/26)

*Duration: 36 days | Leadership and ops hiring are critical path*

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 4.1 | Leadership jobs posted (GM, FSM, WH Manager) | People/TA | 01/26/26 | 01/26/26 | 1 | — | **Y** | |
| 4.2 | Leadership recruiting and interviews | People/TA | 01/26/26 | 02/20/26 | 20 | 4.1 FS-1d | **Y** | |
| 4.3 | Leadership hired | People/TA | 02/20/26 | 02/20/26 | 1 | 4.2 FS-1d | **Y** | **Y** |
| 4.4 | Finalize ops role scorecards and comp bands | People/TA | 01/27/26 | 02/02/26 | 5 | 4.1 | | |
| 4.5 | Ops + WH Coordinator roles posted | People/TA | 01/26/26 | 01/26/26 | 1 | 4.1 FS-1d | **Y** | |
| 4.6 | Ops + WH Coordinator recruiting, interviews, and background checks | People/TA | 01/26/26 | 02/20/26 | 20 | 4.5 FS-1d | **Y** | |
| 4.7 | Ops + WH Coordinator hired | People/TA | 02/20/26 | 02/20/26 | 1 | 4.6 FS-1d | **Y** | **Y** |
| 4.8 | Onboarding paperwork, payroll, & safety docs | People/TA | 02/20/26 | 02/23/26 | 2 | 4.7 FS-1d | **Y** | |
| 4.9 | Onsite field ops training (shadow/evaluation) | Training/Ops | 02/23/26 | 02/27/26 | 5 | 4.8 | | |
| 4.10 | Field ops to JetStart (Jetson University) | Training/Ops | 03/02/26 | 03/13/26 | 10 | 4.9 | | |
| 4.11 | Field ops ready to install | Training/Ops | 03/16/26 | 03/16/26 | 1 | 4.10 | | |

> **Key dependencies:** Leadership and ops hiring tracks run in parallel (both 20-day recruiting windows). Both must complete by 02/20 to keep the training pipeline on track. Training is sequential: onboarding → shadow/evaluation → JetStart → ready to install. No compression possible in the training chain.

> **At-risk items:** Leadership hired (4.3) and Ops hired (4.7) — recruiting timelines are inherently uncertain. If the right candidates aren't in the pipeline by early February, the 02/20 hire date slips, which compresses training and jeopardizes the 03/16 go-live.

> 🚨 **Non-negotiable (from Section 1.4):** No crew goes on a customer site without completing training, certification, and at least one supervised ride-along. If hiring slips, the training timeline does not compress — the launch date moves.

**Playbook cross-reference:** Maps to **Section 1.2 RACI Phase 3 — Hiring, Training & Pre-Launch Readiness** and **Section 1.4 Readiness Gate domain D (Team & Staffing Readiness)**. Criteria T-1 through T-5 depend on Phase 4 completion.

---

## Phase 5 — Facility Set-Up (02/09/26 – 03/17/26)

*Duration: 27 days | Racking permit window is the long pole*

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 5.1 | Finalize facility layout and define racking/CO/permitting requirements | Expansion/Supply Chain | 02/06/26 | 02/12/26 | 5 | 2.7 | **Y** | **Y** |
| 5.2 | Engage racking contractor | Expansion/Supply Chain | 02/13/26 | 02/16/26 | 2 | 5.1 | | |
| 5.3 | Racking permit window | Expansion/Supply Chain | 02/17/26 | 03/16/26 | 20 | 5.2 | **Y** | **Y** |
| 5.4 | Define IT requirements and make site plan | Expansion/IT | 02/06/26 | 02/16/26 | 7 | 2.7 | | |
| 5.5 | Select providers and set-up trash/internet/utilities | Expansion/IT | 02/13/26 | 02/19/26 | 5 | 2.9 FS-5d | | |
| 5.6 | Spec forklift and EV charging equipment/electrical scope | Expansion/Supply Chain | 02/13/26 | 02/16/26 | 2 | 5.1 | | |
| 5.7 | Initial BOM planning & PO release long-lead HVAC items | Supply Chain | 02/13/26 | 02/19/26 | 5 | 5.1 | **Y** | **Y** |

> **Key dependencies:** Everything starts after facility layout (5.1) is finalized. The racking permit window (5.3) is 20 days — jurisdiction-dependent and cannot be compressed. BOM planning (5.7) runs in parallel with the permit window.

> **At-risk items:** Racking permit (5.3) — 20-day window is an estimate; actual permit timelines vary by jurisdiction. If permits take longer, racking installation (Phase 6) slips, which delays inventory stocking and kitting. BOM planning (5.7) — long-lead HVAC items must be ordered early; any delay here ripples into Phase 6 inventory.

**Playbook cross-reference:** Maps to **Section 1.4 Readiness Gate domain B (Facility & Warehouse Readiness)**, criteria F-2 (warehouse racked and receiving-ready).

---

## Phase 6 — Physical Deployment (02/02/26 – 04/20/26)

*Duration: 56 days | The longest and most complex phase — multiple parallel workstreams*

### A) Fleet

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 6.1 | Place Rivian van order | Expansion/Fleet | 02/02/26 | 03/06/26 | 25 | 5.7 FS-31d | **Y** | **Y** |
| 6.2 | Vehicles landed | Expansion/Fleet | 03/09/26 | 03/09/26 | 1 | 6.1 | **Y** | **Y** |
| 6.3 | Vehicle readiness check — standardized loadout | Expansion/Fleet | 03/10/26 | 03/13/26 | 4 | 6.2 | | |

### B) IT & Office

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 6.4 | IT installation | Expansion/IT | 02/27/26 | 03/05/26 | 5 | 5.5 FS+8d | | |
| 6.5 | Office set up | Expansion/IT | 02/20/26 | 02/26/26 | 5 | 2.9 | | |
| 6.6 | Workstations/printing/scanning setup | Expansion/IT | 03/05/26 | 03/05/26 | 1 | 6.5 FS-1d | | |

### C) Racking & Warehouse Infrastructure

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 6.7 | Racking installed | Expansion/Supply Chain | 03/17/26 | 03/19/26 | 3 | 5.3 | **Y** | **Y** |
| 6.8 | Racking set up (label locations — aisle/bay/level/master setup) | Warehouse | 03/20/26 | 03/26/26 | 5 | 6.7 | | |

### D) Systems Configuration

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 6.9 | Configure ServiceTitan dispatch workflows | Warehouse/Ops | 02/23/26 | 02/27/26 | 5 | 4.8 | | |
| 6.10 | Configure NetSuite locations, items, approvals | Warehouse/Ops | 02/20/26 | 03/03/26 | 8 | 2.9 | | |
| 6.11 | Mobile device setup — field MDM, logins, MFA apps | Warehouse/Ops | 03/02/26 | 03/04/26 | 3 | 6.10 | | |

### E) Inventory & Kitting

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 6.12 | Order/receive/put-away inventory | Supply Chain | 03/27/26 | 04/17/26 | 16 | 6.8 | **Y** | **Y** |
| 6.13 | Finalize SKU list + min/max + reorder points | Supply Chain | 03/04/26 | 03/04/26 | 1 | 6.10 | | |
| 6.14 | Receive initial POs — QC, discrepancy resolution | Warehouse | 03/05/26 | 03/05/26 | 1 | 6.13 | | |
| 6.15 | Put-away + cycle count baseline | Warehouse | 03/06/26 | 03/10/26 | 3 | 6.14 | | |
| 6.16 | Define kit BOM, pick lists, packaging standard | Supply Chain | 03/02/26 | 03/03/26 | 2 | 6.10 | | |
| 6.17 | Build kits + stage in S/R | Warehouse | 03/04/26 | 03/04/26 | 1 | 6.16 | | |
| 6.18 | Mock install + truck load/unload time trials | Training/Ops | 03/05/26 | 03/05/26 | 1 | 6.17 | | |
| 6.19 | Build installation kits + dry runs | Warehouse | 03/06/26 | 03/17/26 | 8 | 6.14 | **Y** | **Y** |

### F) Training & Readiness

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 6.20 | Training + launch readiness gate | Training/Ops | 02/24/26 | 03/10/26 | 11 | 4.8 | **Y** | **Y** |
| 6.21 | WH SOPs — receiving, put-away, cycle count, kitting | Warehouse | 03/11/26 | 03/12/26 | 2 | 6.15 | | |
| 6.22 | Field install safety toolbox QA checklist | Warehouse | 03/16/26 | 03/16/26 | 1 | 6.3 | | |
| 6.23 | Systems training — NetSuite, comms | Training/Ops | 03/05/26 | 03/06/26 | 2 | 6.11 | | |
| 6.24 | Readiness — staffing, permits, vehicles, training | Expansion/Training/Ops | 03/13/26 | 03/19/26 | 5 | 6.23 | | |

> 🚨 **System note:** The Gantt references **ServiceTitan** (task 6.9) for dispatch workflows. The playbook RACI and readiness gates currently reference **Zuper**. Confirm which platform is current and update Section 1.4 (readiness gate criteria S-1) accordingly.

**Playbook cross-reference:** Maps to **Section 1.2 RACI Phases 2–3** and **Section 1.4 Readiness Gate domains B, C, D** (Facility, Systems, Team).

---

## Phase 7 — Sales Enablement (01/26/26 – 02/04/26)

*Duration: 8 days | Runs early and in parallel with hiring and real estate*

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 7.1 | Pricing locked | Finance/Expansion | 01/26/26 | 01/30/26 | 5 | 1.7 FS-8d | **Y** | |
| 7.2 | Equipment selection matrix updated | Product | 01/26/26 | 01/26/26 | 1 | 1.7 FS-8d | | |
| 7.3 | Intake enabled | Product/Expansion | 01/26/26 | 01/26/26 | 1 | 1.7 FS-8d | | |
| 7.4 | Phone tree set-up and enabled | Expansion/IT | 01/26/26 | 01/26/26 | 1 | 1.7 FS-8d | | |
| 7.5 | Digital set-up | Marketing/Expansion | 01/26/26 | 01/26/26 | 1 | 1.7 FS-8d | | |
| 7.6 | Website set-up | Marketing/Expansion | 01/26/26 | 01/26/26 | 1 | 1.7 FS-8d | | |
| 7.7 | PR launch | Marketing/Expansion | 01/26/26 | 01/26/26 | 1 | 1.7 FS-8d | | |
| 7.8 | Affiliates launch | Marketing/Expansion | 01/26/26 | 01/26/26 | 1 | 1.7 FS-8d | | |
| 7.9 | Preferred vendor referral list (ESUs, etc.) | Expansion/Ops | 01/26/26 | 01/26/26 | 1 | 1.7 FS-8d | | |
| 7.10 | Sales start | Sales | 02/03/26 | 02/04/26 | 2 | 7.1 FS-30d | | |

> **Key dependencies:** All tasks start 8 days *before* charter approval (1.7) finishes — calculated overlap to build pipeline ahead of go-live. Sales start (7.10) is ~6 weeks before operations launch, giving the pipeline time to build.

**Playbook cross-reference:** Maps to **Section 1.4 Readiness Gate domain E (Sales & Demand Readiness)**. Criteria D-1 through D-4 depend on Phase 7 activation.

---

## Phase 8 — Operations Launch (03/16/26)

*Duration: 1 day | Go-live milestone*

| # | Task | Owner | Start | Finish | Days | Pred. | CP | Risk |
|---|------|-------|-------|--------|------|-------|:--:|:----:|
| 8.1 | Installations begin | Ops | 03/16/26 | 03/16/26 | 1 | 4.11 | **Y** | |

> This is the soft launch date. The readiness gate (Section 1.4) must pass at **T-7 (03/09/26)** for this date to hold. War room cadence begins on this date (see Section 8.4, forthcoming).

**Playbook cross-reference:** Maps to **Section 1.2 RACI Phase 4 — Soft Launch & Go-Live**. The VP of Expansion approves the go-live decision.

---

## Phase 9 — Post-Launch Scaling (03/17/26 – 06/03/26)

*Duration: 57 days | No items on critical path — all post-launch optimization*

| # | Task | Owner | Start | Finish | Days | Pred. |
|---|------|-------|-------|--------|------|-------|
| 9.1 | Hypercare support period — standups, resolution | Expansion/Ops/Supply Chain/Sales | 03/17/26 | 03/30/26 | 10 | 8.1 |
| 9.2 | Daily ops huddle — scheduling, quality, safety | Ops | 03/31/26 | 04/13/26 | 10 | 9.1 |
| 9.3 | Fix gaps in SOPs + retrain as needed | Ops/Training | 04/14/26 | 04/20/26 | 5 | 9.2 |
| 9.4 | Process hardening + KPI tracking | Ops | 03/31/26 | 04/27/26 | 20 | 9.1 |
| 9.5 | Establish weekly KPI cadence + dashboard | Ops | 04/28/26 | 04/29/26 | 2 | 9.4 |
| 9.6 | Cycle count program + shrink controls | Warehouse/Supply Chain | 04/30/26 | 05/19/26 | 14 | 9.5 |
| 9.7 | Vendor + supply chain optimization | Warehouse/Supply Chain | 04/30/26 | 05/26/26 | 19 | 9.5 |
| 9.8 | Tune min/max based on consumption | Warehouse/Supply Chain | 05/27/26 | 06/03/26 | 6 | 9.7 |
| 9.9 | Local supplier onboarding + SLAs | Warehouse/Supply Chain | 04/28/26 | 05/18/26 | 15 | 9.4 |
| 9.10 | Post-mortem | Expansion/Ops/Supply Chain/Sales | 04/14/26 | 04/17/26 | 4 | 8.1 FS+20d |
| 9.11 | Lessons learned — update playbook/permitting/expansion template | Expansion/Ops/Supply Chain/Sales | 05/19/26 | 06/01/26 | 10 | 9.10 |

> **Key structure:** Hypercare (9.1) is the first 10 days — daily standups with all functions. This transitions into daily ops huddles (9.2) as the market stabilizes. Post-mortem (9.10) is scheduled ~30 days after launch. The phase ends with lessons learned captured and fed back into the playbook.

**Playbook cross-reference:** Maps to **Section 1.2 RACI Phase 5 — Stabilization & Handoff** and the forthcoming **Section 9.2 (Stabilization Scorecard)** and **Section 9.3 (Formal Handoff Criteria)**.

---

## Critical Path Summary

The following chains drive the 03/16 launch date. Any slip on these items moves go-live:

```
FACILITY CHAIN
  Warehouse location assessment (12/29)
    → Charter approval (01/09) ◄ AT RISK
      → Lease negotiation (01/21–02/05) ◄ AT RISK
        → Warehouse occupancy (02/19) ◄ AT RISK
          → Facility layout finalized (02/06–02/12) ◄ AT RISK
            → Racking permit window (02/17–03/16) ◄ AT RISK
              → Racking installed (03/17–03/19) ◄ AT RISK
                → Inventory stocked (03/27–04/17) ◄ AT RISK

TALENT CHAIN
  Leadership + Ops hiring (01/26–02/20) ◄ AT RISK
    → Onboarding (02/20–02/23)
      → Training + readiness gate (02/24–03/10) ◄ AT RISK
        → Field ops ready (03/16)
          → INSTALLATIONS BEGIN (03/16)

FLEET CHAIN
  Rivian van order (02/02–03/06) ◄ AT RISK
    → Vehicles landed (03/09) ◄ AT RISK
      → Loadout (03/10–03/13)
```

**Three critical chains converge at go-live.** All three must complete for 03/16 to hold.

---

## Flags for Review

> ⚠️ **Items requiring discussion during the next review session:**
>
> 1. **ServiceTitan vs. Zuper** — The Gantt references ServiceTitan for dispatch workflows (task 6.9). The playbook currently references Zuper throughout Section 1.4 (readiness gates). Confirm which platform is current and update accordingly.
>
> 2. **Inventory timeline extends past go-live** — Task 6.12 (order/receive/put-away inventory) runs 03/27–04/17, which is *after* the 03/16 go-live. Confirm whether initial inventory for soft launch is stocked earlier (via tasks 6.14–6.15) and task 6.12 represents the full inventory build-out.
>
> 3. **Sales start 6 weeks before ops launch** — Sales start (02/03) is 41 days before installations begin (03/16). Confirm pipeline management plan for managing customer expectations during this gap.
>
> 4. **Racking permit window (20 days)** — This is the single longest at-risk item on the critical path. If the jurisdiction requires more time, the entire facility chain slips. Consider identifying permit timelines during Phase 1 (market assessment) to de-risk early.

---

## 🎯 If You Only Remember 3 Things

1. **Three critical chains converge at go-live (03/16): facility, talent, and fleet.** All three must complete. The Market Launch Lead must track all three daily — not just the one that feels most urgent.
2. **Seven items are both critical-path and at-risk.** These are the tasks most likely to move the launch date: charter approval, lease negotiation, warehouse occupancy, hiring, racking permit, fleet delivery, and training readiness. Build mitigation plans for each.
3. **The schedule is aggressive but achievable — if the critical path is managed.** Total timeline is ~23 weeks from assessment to post-launch lessons learned. There is minimal float on the critical path. Slippage compounds. Catch it early or accept a date move.
