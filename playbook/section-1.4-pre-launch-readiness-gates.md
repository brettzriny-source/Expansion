<callout icon="📋" color="blue_bg">
# 1.4 Pre-Launch Readiness Gates
The hard-stop checklist that determines whether a market moves to soft launch — or holds.
</callout>

## Purpose

A market launch is a one-shot first impression. Once the first install truck rolls and the first customer is scheduled, every gap in readiness becomes a live operational problem — visible to customers, partners, and the team. The Pre-Launch Readiness Gate is the formal mechanism that prevents premature launches. It forces every function to prove readiness against objective criteria *before* the VP of Expansion approves the move to soft launch.

This section defines:
- What "ready" means — the specific criteria, by function, that must be met
- How the gate review works — who runs it, who approves, and what happens when criteria aren't met
- The escalation path when a gate fails — because "push through anyway" is not an option

<callout icon="💡" color="yellow_bg">
**Core rule:** The readiness gate is pass/fail. There is no "conditional pass" or "pass with caveats." If a criterion is not met, the launch holds until it is — or the VP of Expansion explicitly accepts the risk in writing with a documented mitigation plan.
</callout>

---

<callout icon="1️⃣" color="green_bg">
### 1) Readiness Gate Principles
</callout>

**A) Why Gates Exist**

Every launch team feels pressure to "just get going." The pipeline is building, the team is hired, the market is waiting. That pressure is exactly why the gate exists. The most expensive launch failures at Jetson have not been caused by bad markets — they've been caused by launching before the market was actually ready to receive customers.

The readiness gate protects:
- **Customers** from a broken first experience (missed installs, scheduling failures, unqualified crews)
- **The field team** from being set up to fail (no parts, no warehouse, no systems access)
- **The business** from reputational damage that takes months to recover from

**B) Gate Principles**

1. **Objective, not subjective.** Every criterion has a measurable definition of "done." No "I think we're good" — show the evidence.
2. **Binary pass/fail.** Each criterion is either met or not met. Partial credit doesn't exist.
3. **One gate owner.** The Market Launch Lead compiles and presents the gate review. The VP of Expansion (Brett) approves or holds.
4. **No retroactive waivers.** You cannot pass the gate and then "finish up" a criterion post-launch. If it wasn't done at gate review, the gate didn't pass.
5. **Holds are not failures.** A hold means the team identified a gap before it became a customer problem. That's the system working. A hold with a clear remediation plan and revised timeline is a sign of operational maturity.

<callout icon="⚠️" color="orange_bg">
**The MA expansion taught us:** The team was 90% ready and the pipeline was hot. Leadership pressure to launch was real. The warehouse was "almost done" and the first crew hadn't completed certification ride-alongs. We launched anyway. Week 1 had three installs with missing parts and a crew that wasn't confident on a core product line. It took six weeks to rebuild customer trust and team morale. The readiness gate exists because of that experience.
</callout>

---

<callout icon="2️⃣" color="green_bg">
### 2) Readiness Gate Criteria — By Function
</callout>

The gate review covers **seven readiness domains**. Every domain must pass independently. A single domain failure holds the entire launch.

**A) Legal & Entity Readiness**

| # | Criterion | Evidence Required | Owner (R) |
|---|-----------|-------------------|-----------|
| L-1 | Business entity registered in state | Secretary of State filing confirmation | Market Launch Lead |
| L-2 | All required contractor/trade licenses obtained | License copies on file | Market Launch Lead |
| L-3 | General liability and workers' comp insurance active | Certificate of insurance with correct entity and coverage limits | Market Launch Lead |
| L-4 | Local permits secured (if applicable) | Permit copies or written confirmation from jurisdiction | Market Launch Lead |

> **Pass means:** All documents are on file, active, and verified — not "applied for" or "in process."

---

**B) Facility & Warehouse Readiness**

| # | Criterion | Evidence Required | Owner (R) |
|---|-----------|-------------------|-----------|
| F-1 | Warehouse lease signed and space available | Executed lease agreement | Procurement (Mike) |
| F-2 | Warehouse racked, organized, and receiving-ready | Photo documentation + walk-through sign-off | Procurement (Mike) |
| F-3 | Initial BOM inventory stocked per launch kitting list | Inventory count reconciled to kitting spec | Procurement (Mike) |
| F-4 | Fleet vehicles acquired, wrapped, and road-ready | Vehicle registration + fleet inspection checklist | Procurement (Mike) |
| F-5 | Warehouse address configured in logistics/routing systems | System screenshot showing active warehouse location | Market Launch Lead |

<callout icon="⚠️" color="orange_bg">
**Operational lesson:** "Lease signed" ≠ "warehouse ready." The readiness gate requires the warehouse to be **racked, stocked, and receiving-ready** — not just leased. Build in at least 2–3 weeks between lease signing and the gate review for buildout, stocking, and verification.
</callout>

---

**C) Systems & Technology Readiness**

| # | Criterion | Evidence Required | Owner (R) |
|---|-----------|-------------------|-----------|
| S-1 | **Zuper** instance configured: services, pricing, scheduling zones, and workflows active | QA walkthrough of booking → dispatch → completion flow | Customer Ops (Ryan) |
| S-2 | **HubSpot** market configured: pipeline stages, lead routing, and automation active | Test lead created and routed successfully | Sales (Angie) |
| S-3 | **Rippling** set up: new market employees onboarded, payroll state registered | Rippling org chart showing active employees in correct entity | Market Launch Lead |
| S-4 | **NetSuite** subsidiary or location configured: GL coding, PO workflows, AP/AR routing | Test PO and invoice processed through workflow | Market Launch Lead |
| S-5 | Phone/SMS lines active and routing to correct team | Test call and test SMS confirmed | Customer Ops (Ryan) |
| S-6 | Customer-facing scheduling portal live and tested (if applicable) | End-to-end test booking from customer perspective | Customer Ops (Ryan) |

> **Pass means:** Every system has been tested end-to-end with a realistic scenario — not just "provisioned" or "configured." A system that's set up but untested is a system that will break on Day 1.

---

**D) Team & Staffing Readiness**

| # | Criterion | Evidence Required | Owner (R) |
|---|-----------|-------------------|-----------|
| T-1 | All launch-critical roles filled and start dates confirmed | Hiring tracker showing filled positions, start dates, and onboarding status | Market Launch Lead |
| T-2 | Field crews trained and certified on core product lines | Training completion records + certification sign-off from Field Ops | Field Ops (Cameron) |
| T-3 | Field crews have completed ride-along / shadow shifts in an existing market | Ride-along log with dates, markets, and supervisor sign-off | Field Ops (Cameron) |
| T-4 | GM identified (or Market Launch Lead confirmed as acting GM through stabilization) | Org chart with named GM and reporting structure | VP of Expansion (Brett) |
| T-5 | All crew members have required safety certifications and background checks completed | HR compliance checklist — 100% completion | Market Launch Lead |

<callout icon="⚠️" color="red_bg">
**Non-negotiable:** No crew goes on a customer site without completing training, certification, and at least one supervised ride-along in an existing market. This is a safety and quality requirement — not a "nice to have." If crew certification is incomplete, the gate does not pass.
</callout>

---

**E) Sales & Demand Readiness**

| # | Criterion | Evidence Required | Owner (R) |
|---|-----------|-------------------|-----------|
| D-1 | Soft launch pipeline meets minimum threshold for controlled volume | HubSpot pipeline report showing qualified opportunities ≥ [market-specific target] | Sales (Angie) |
| D-2 | Sales team trained on market-specific positioning, pricing, and objection handling | Training completion records | Sales (Angie) |
| D-3 | Local marketing assets and lead gen campaigns staged (if applicable) | Campaign brief and creative assets approved | Sales (Angie) |
| D-4 | Referral and partner channel introductions completed (if applicable) | Meeting notes or partnership confirmation emails | Sales (Angie) |

> **Pass means:** There is enough qualified pipeline to sustain controlled volume during soft launch. The team is not launching into an empty market — and the sales team knows how to sell in this specific geography.

---

**F) Customer Operations Readiness**

| # | Criterion | Evidence Required | Owner (R) |
|---|-----------|-------------------|-----------|
| O-1 | Scheduling capacity configured for soft launch volume | Zuper capacity plan showing available slots vs. projected demand | Customer Ops (Ryan) |
| O-2 | Customer communication templates configured (confirmation, reminder, follow-up) | Template library reviewed and approved | Customer Ops (Ryan) |
| O-3 | Escalation and issue resolution workflow defined | Documented escalation path with named owners and SLAs | Customer Ops (Ryan) |
| O-4 | Post-install survey and feedback mechanism active | Test survey sent and received | Customer Ops (Ryan) |

---

**G) Financial & Budget Readiness**

| # | Criterion | Evidence Required | Owner (R) |
|---|-----------|-------------------|-----------|
| B-1 | Launch budget approved and coded in NetSuite | Budget document signed by VP of Expansion + NetSuite GL mapping | Market Launch Lead |
| B-2 | Spending to date within approved budget (no unresolved overruns) | Budget vs. actuals report | Market Launch Lead |
| B-3 | Ongoing operating expense forecast loaded for first 90 days | 90-day cash flow projection reviewed by VP of Expansion | Market Launch Lead |

> **Pass means:** The market has a funded, approved budget with no unresolved cost overruns from the planning phase. The 90-day operating forecast is realistic and reviewed — not a copy-paste from another market.

---

<callout icon="3️⃣" color="green_bg">
### 3) The Gate Review Process
</callout>

**A) Timeline**

The readiness gate review is scheduled for **T-7** (seven days before planned soft launch). This gives enough time to remediate minor gaps without delaying the launch, while being close enough to launch that the review reflects actual readiness — not projected readiness.

| Milestone | Timing | Action |
|-----------|--------|--------|
| Pre-gate self-assessment | T-14 | Market Launch Lead circulates the gate checklist to all functional owners. Each owner self-assesses their criteria and flags any at-risk items. |
| Risk mitigation window | T-14 to T-7 | Market Launch Lead works with functional owners to close any gaps identified in the self-assessment. |
| Formal gate review | T-7 | Market Launch Lead presents the completed gate checklist to the VP of Expansion and all functional leads. |
| Gate decision | T-7 (same day) | VP of Expansion issues one of three decisions: **Pass**, **Hold**, or **Conditional Pass with Risk Acceptance**. |

**B) Gate Review Format**

The gate review is a **60-minute structured meeting**, not a status update. The Market Launch Lead runs the meeting using the following agenda:

1. **Roll call and purpose** (2 min) — Confirm all functional owners are present.
2. **Domain-by-domain walkthrough** (40 min) — For each of the seven domains, the responsible owner presents:
   - Status of each criterion (Pass / Fail / At Risk)
   - Evidence for each passing criterion (document, screenshot, confirmation)
   - Remediation plan and timeline for any failing criterion
3. **Integrated risk assessment** (10 min) — Market Launch Lead presents the overall readiness picture: What's green, what's red, and what's the recommendation.
4. **Gate decision** (8 min) — VP of Expansion makes the call.

**C) Gate Decisions**

| Decision | Definition | What Happens Next |
|----------|-----------|-------------------|
| **Pass** | All seven domains meet all criteria. Evidence is on file. | Launch proceeds on planned date. War room cadence begins at T-0 (see Section 8.4). |
| **Hold** | One or more criteria are not met with no acceptable mitigation. | Launch date is pushed. Market Launch Lead publishes a revised timeline within 48 hours with specific remediation actions and a new gate review date. |
| **Conditional Pass (Risk Acceptance)** | One or more criteria are not met, but the VP of Expansion determines the risk is manageable with a documented mitigation plan. | Launch proceeds. VP of Expansion documents the specific risk accepted, the mitigation plan, and the accountable owner for remediation. This is the exception, not the norm — and it requires the VP of Expansion's written sign-off. |

<callout icon="⚠️" color="red_bg">
**Non-negotiable:** Only the VP of Expansion can issue a Conditional Pass. The Market Launch Lead cannot self-approve risk acceptance. If Brett is unavailable for the gate review, the review is rescheduled — it does not default to "pass."
</callout>

---

<callout icon="4️⃣" color="green_bg">
### 4) When the Gate Fails
</callout>

A gate hold is not a crisis — it's the system working. Here's how to handle it:

**A) Immediate Actions (Within 24 Hours of Hold)**

1. **Market Launch Lead** identifies every failing criterion and the responsible owner.
2. **Market Launch Lead** works with each owner to build a specific remediation plan:
   - What needs to happen?
   - Who will do it?
   - By when?
   - What resources or escalations are needed?
3. **Market Launch Lead** publishes a revised launch timeline to the VP of Expansion and all functional leads.
4. **Market Launch Lead** schedules a new gate review date — typically 7–14 days out, depending on the severity of the gaps.

**B) Communication**

- **Internal (Expansion team + functional leads):** Transparent communication about the hold, the reason, and the revised plan. No spin. The team should view the hold as a quality decision, not a setback.
- **External (if pipeline is active):** If customers have been scheduled or prospects are expecting a launch date, Sales and Customer Ops coordinate messaging. A delayed launch is far better than a botched one — frame accordingly.
- **Executive (if applicable):** VP of Expansion briefs leadership on the hold if it impacts broader company timelines or resource allocation.

**C) Remediation Tracking**

During the hold period, the Market Launch Lead runs a **daily stand-up** (15 minutes) focused exclusively on the failing criteria. This is not the full war room — it's a targeted remediation cadence:

- What was done yesterday toward the failing criteria?
- What's planned for today?
- What's blocking progress?

The stand-up continues until all criteria are resolved and the re-review is scheduled.

---

<callout icon="5️⃣" color="green_bg">
### 5) Common Failure Modes (And the Fix)
</callout>

**A) "We're 95% ready — let's just go"**

**Failure:** The team has invested months of work. The pipeline is strong. Leadership is eager. The only gap is one criterion — maybe crew certification is at 80%, or the warehouse is stocked but the routing system isn't configured. The pressure to launch is enormous.

**Fix:** 95% ready is not ready. The gate criteria exist because the missing 5% is typically the 5% that causes Week 1 failures. Hold the line. A one-week hold is invisible to customers three months from now. A botched launch sticks for a year.

---

**B) "The criterion is technically met, but barely"**

**Failure:** The evidence for a criterion is thin. Crew "training" was a two-hour walkthrough instead of supervised ride-alongs. The warehouse is "stocked" but the inventory count hasn't been reconciled. The system is "configured" but no one ran a test transaction.

**Fix:** The gate review is evidence-based, not checkbox-based. The VP of Expansion should probe the quality of the evidence, not just its existence. "Is this criterion truly met to the standard we'd be comfortable with if a journalist followed our crew on Day 1?"

---

**C) "We'll fix it during soft launch"**

**Failure:** A criterion fails, but the team argues that soft launch is "controlled volume" — so they can fix the gap while doing early installs.

**Fix:** Soft launch is live operations. Customers don't know they're "soft launch" customers — they expect the same quality as any other customer. Fixing foundational gaps while running live ops is how quality spirals. The readiness gate is the last clean checkpoint — use it.

---

**D) "We didn't have time for the self-assessment"**

**Failure:** The T-14 self-assessment was skipped or treated as a formality. Gaps surface for the first time at the T-7 gate review. There's not enough time to remediate, and the launch is held.

**Fix:** The T-14 self-assessment is not optional. The Market Launch Lead should treat T-14 as the "real" gate and T-7 as the confirmation. Any criterion that's red at T-14 needs an immediate remediation plan. If the Launch Lead isn't circulating the checklist at T-14, the VP of Expansion should ask why.

---

<callout icon="6️⃣" color="green_bg">
### 6) Readiness Gate Quick-Reference Checklist
</callout>

For fast reference, here is the consolidated pass/fail checklist the Market Launch Lead should use when preparing for the gate review:

| Domain | # | Criterion | Pass? |
|--------|---|-----------|:-----:|
| **Legal & Entity** | L-1 | Business entity registered | ☐ |
| | L-2 | Contractor/trade licenses obtained | ☐ |
| | L-3 | Insurance active (GL + WC) | ☐ |
| | L-4 | Local permits secured | ☐ |
| **Facility & Warehouse** | F-1 | Warehouse lease signed | ☐ |
| | F-2 | Warehouse racked, organized, receiving-ready | ☐ |
| | F-3 | BOM inventory stocked per kitting list | ☐ |
| | F-4 | Fleet vehicles acquired and road-ready | ☐ |
| | F-5 | Warehouse in logistics/routing systems | ☐ |
| **Systems & Technology** | S-1 | Zuper configured and tested | ☐ |
| | S-2 | HubSpot configured and tested | ☐ |
| | S-3 | Rippling set up for new market | ☐ |
| | S-4 | NetSuite subsidiary/location configured | ☐ |
| | S-5 | Phone/SMS lines active and routing | ☐ |
| | S-6 | Customer scheduling portal live and tested | ☐ |
| **Team & Staffing** | T-1 | All launch-critical roles filled | ☐ |
| | T-2 | Field crews trained and certified | ☐ |
| | T-3 | Ride-alongs / shadow shifts completed | ☐ |
| | T-4 | GM identified or acting GM confirmed | ☐ |
| | T-5 | Safety certs and background checks done | ☐ |
| **Sales & Demand** | D-1 | Soft launch pipeline meets minimum threshold | ☐ |
| | D-2 | Sales team trained on market positioning | ☐ |
| | D-3 | Marketing assets and campaigns staged | ☐ |
| | D-4 | Partner/referral introductions completed | ☐ |
| **Customer Ops** | O-1 | Scheduling capacity configured | ☐ |
| | O-2 | Customer communication templates ready | ☐ |
| | O-3 | Escalation workflow defined | ☐ |
| | O-4 | Post-install feedback mechanism active | ☐ |
| **Financial & Budget** | B-1 | Launch budget approved and coded | ☐ |
| | B-2 | Spending within approved budget | ☐ |
| | B-3 | 90-day operating expense forecast loaded | ☐ |

---

<callout icon="⚠️" color="red_bg">
**Non-negotiable: No market moves to soft launch without a passed readiness gate. The gate is the last line of defense between planning and live operations. If it feels like overhead during a smooth launch, that's the system working. If it catches a gap, it just saved you six weeks of recovery.**
</callout>

<callout icon="📝" color="gray_bg">
**Note:** This section covers the pre-launch readiness gate at the Phase 3 → Phase 4 boundary (T-0 soft launch). For the stabilization scorecard that governs the Phase 5 handoff gate (Expansion → GM), see **Section 9.2: Stabilization Scorecard**. For the formal handoff criteria and process, see **Section 9.3: Formal Handoff Criteria**.
</callout>

---

<callout icon="🎯" color="red_bg">
## If You Only Remember 3 Things
1. **The readiness gate is pass/fail — not a negotiation.** Every criterion has objective evidence. If the evidence isn't there, the gate doesn't pass. A one-week hold beats a botched launch every time.
2. **T-14 is the real gate. T-7 is the confirmation.** If you're seeing red criteria for the first time at T-7, you've already lost a week. The self-assessment at T-14 is where remediation starts.
3. **Only the VP of Expansion can approve a Conditional Pass.** Risk acceptance is a leadership decision, not a team decision. If it needs to be escalated, escalate it. That's what the gate is for.
</callout>
