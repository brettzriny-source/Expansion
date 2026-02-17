# Gate Integration Roadmap

How to reference gates throughout the Expansion Playbook — and what's been updated so far.

---

## Current State Assessment

### What's Already Done

- **Section 2.1** (Master Launch Timeline): Complete Gantt chart with all 9 phases, task dependencies, and critical path items
- **Appendix A-9** (Gates & Readiness Criteria): Complete gate definitions (G0-G6) with pass criteria, Smartsheet mappings, and failure modes
- **Appendix A-10** (Weekly Launch Call): Updated with War Room distinction, attendance requirements, and agenda process

### What Needs Integration

Sections 3-11 need gate cross-references added to tie the narrative content back to the gate framework and Gantt timeline.

---

## Integration Checklist by Section

### Section 3: Market Identification & Prioritization

**Status:** Complete — see [Section 3.2 — Market Greenlight Criteria & Gate G0](section-3.2-market-greenlight-criteria.md)

---

### Section 4: Market Launch Planning

**Current State:** Narrative about launch planning activities
**Needs:** Gate G1 and G2 cross-references across subsections

#### 4.1 Launch Timeline Template

**Add cross-reference to Section 2.1:**

> **Timeline Reference:** This T-minus countdown view complements the phase-based view in Section 2.1 (Master Launch Timeline). Both views represent the same Smartsheet Gantt chart — Section 2.1 organizes by phase, this section organizes by days-to-launch.

#### 4.2 Pre-Launch Checklist

**Add gate mapping at top:**

```markdown
### Gate Checkpoints: G0 → G1 → G2

This checklist spans three gates:
- **G0** (Market Assessment): Tasks 1.1–1.7
- **G1** (Real Estate): Tasks 2.1–2.9 ⚠️ Lease negotiation and occupancy are critical path
- **G2** (Compliance & Leadership): Tasks 3.1–3.4 and 4.1–4.3

See Appendix A-9 for complete gate criteria.
```

#### 4.3 Budget & Financial Model

**Add G0 reference:**

> **Gate Requirement:** Budget approval is a G0 pass criterion (see Appendix A-9). No market advances past G0 without CFO and CEO budget approval.

#### 4.4 Facility & Warehouse Readiness

**Add G1 reference:**

```markdown
### Gate G1: Real Estate Secured

**Gantt Reference:** Phase 2 — Real Estate (Tasks 2.1-2.9)

**Critical Path Dependencies:**
- Lease negotiation (Task 2.7): 12-16 days ⚠️ At Risk
- Warehouse occupancy (Task 2.9): Must complete for G1 pass ⚠️ At Risk

**G1 Pass Criteria (5 total):**
- Lease executed
- Insurance and deposit in place
- Occupancy date confirmed (≤ T-30 from go-live)
- Facility layout finalized
- Site meets minimum requirements

**Escalation:** Report G1 status weekly in Expansion Launch Call (Appendix A-10). Lease delays are common failure mode — see Appendix A-9 for mitigation strategies.
```

#### 4.5 Fleet & Equipment Procurement

**Add G4 reference:**

> **Gate Requirement:** Vehicles must be landed and outfitted for G4 pass (vehicle readiness criteria). Gantt Task 6.1 (Place Rivian order) is 25-33 days and sits on critical path ⚠️. Order vehicles at T-90 or earlier.

---

### Section 5: Hiring Strategy for New Markets

**Current State:** Narrative about hiring
**Needs:** Gate G2 and G3 cross-references

#### 5.2 GM Selection for New Markets

**Add at top:**

```markdown
### Gate G2: GM Hired

**Gantt Reference:** Phase 4 — Talent Launch, Tasks 4.1-4.3

**Timeline:**
- Jobs posted: T-90 (Task 4.1)
- Recruiting window: 20 days (Task 4.2) ⚠️ At Risk
- Hired milestone: T-60 minimum (Task 4.3) ⚠️ Critical

**G2 Pass Criterion:** Signed offer letter + start date ≤ T-45 from go-live

**Common Failure:** GM hire falls through or delays. See Appendix A-9, Gate G2 failure modes for mitigation strategies.

**Related:** See Appendix A-5 for GM 30/60/90 onboarding plan.
```

#### 5.3 Field Team Recruiting

**Add at top:**

```markdown
### Gate G3: Ops & WH Coordinators Hired

**Gantt Reference:** Phase 4 — Talent Launch, Tasks 4.5-4.8

**Timeline:**
- Jobs posted: T-90 (Task 4.5)
- Recruiting window: 20 days (Task 4.6) ⚠️ At Risk
- Hired milestone: T-30 minimum (Task 4.7) ⚠️ Critical
- Onboarding: 2-4 days (Task 4.8)

**G3 Pass Criteria (hiring):**
- All ops and warehouse coordinator roles filled (signed offers)
- Background checks and onboarding paperwork complete

**Escalation:** Ops hiring shortfalls are common. Report status in Weekly Launch Call. VP may reallocate TA resources between markets or authorize borrowing installers from existing markets.
```

---

### Section 6: Training & Readiness

**Current State:** Narrative about training programs
**Needs:** Gate G4 cross-references

#### 6.2 Field Team Certification Before Go-Live

**Add at top:**

```markdown
### Gate G4: Training & Certification Complete

**Gantt Reference:** Phase 4 — Talent Launch, Tasks 4.9-4.11 + Phase 6, Task 6.20

**Training Timeline:**
- Onsite shadow/evaluation: 5 days (Task 4.9)
- JetStart (Jetson University): 10-12 days (Task 4.10)
- Training + readiness gate: 11 days (Task 6.20) ⚠️ Critical Path
- Ready to install: T-0 (Task 4.11)

**G4 Pass Criteria (training):**
- Training completion certificates for all installers
- Certification checklist signed by Training Lead
- Quality, safety, and customer interaction standards met

**NON-NEGOTIABLE:** No crew goes on a customer site without completing training and certification. If hiring slips, training timeline does NOT compress — the launch date moves.

See Appendix A-9, Gate G4 for certification standards.
```

---

### Section 7: Local Market Entry Strategy

**Current State:** Narrative about sales and GTM
**Needs:** Gate G4 (sales enablement) and G5 cross-references

#### 7.1 Brand Introduction & Local Awareness

**Add at top:**

```markdown
### Gate G4: Sales Enablement Complete

**Gantt Reference:** Phase 7 — Sales Enablement (Tasks 7.1-7.10)

**Sales Enablement Timeline:**
- Pricing locked: 5 days (Task 7.1) ⚠️ Critical Path
- Digital/website/intake setup: 1 day each (Tasks 7.2-7.9)
- **Sales start: T-30 to T-40** (Task 7.10) — Pipeline build window

**G4 Pass Criterion (sales enablement):**
Customer can request a quote and be scheduled in target service area. All enablement items live:
- Pricing, intake, phone tree, website, digital ads, PR, affiliates, referral lists

**CRITICAL RULE from MA Expansion:** Sales does NOT begin until Market Launch Lead and VP of Field Operations jointly approve G4 pass. This is the #1 lesson learned — never start sales before ops is ready.
```

---

### Section 8: The Launch Playbook

**Current State:** Narrative about launch execution
**Needs:** Gate G5 cross-references and War Room clarification

#### 8.1 Soft Launch Phase

**Add at top:**

```markdown
### Gate G5: Go-Live — First Installation

**Gantt Reference:** Phase 8 — Operations Launch (Task 8.1)

**Go-Live Prerequisites (G4 must pass):**
- Vehicles landed and outfitted
- Inventory kitted and staged
- Training certified
- Systems live
- Sales enablement complete

**G5 Pass Criteria (5 total):**
- First installation completed successfully
- Customer satisfaction confirmed (NPS ≥ 8)
- Quality standards met (QA checklist passed, no immediate callbacks)
- System commissioned and functional
- Installation time within target range (8-hour window)

**What Happens After G5:**
- Hypercare support begins (daily standups)
- Report status in Weekly Launch Call (Appendix A-10)
- VP of Expansion may call War Room if launch at risk

See Appendix A-9, Gate G5 for complete pass criteria and failure modes.
```

#### 8.4 Launch War Room Protocol

**Add clarification at top:**

```markdown
## 8.4 Launch War Room Protocol

> **When the War Room is Called**
>
> The Launch War Room is a **temporary, high-intensity forum** called by the VP of Expansion when:
> - A launch date is **deemed at risk**, AND
> - There is **no clear path to resolution** through normal escalation
>
> The War Room is **NOT a standing meeting**. Most launches will never require a War Room.
> Standard tracking and decision-making happens in the Weekly Expansion Launch Call (Appendix A-10).
>
> **Entry Criteria:**
> - Critical gate blocked (typically G3, G4, or G5)
> - Timeline slip > 2 weeks with no mitigation plan
> - Multiple red workstreams with cross-functional dependencies
> - VP of Expansion determines standard escalation insufficient
>
> **Exit Criteria:**
> - Crisis resolved, clear path to launch date
> - OR timeline adjusted and all stakeholders aligned
> - OR launch decision made (pause/proceed)
```

---

### Section 9: Post-Launch Stabilization

**Current State:** Narrative about stabilization
**Needs:** Gate G6 cross-references

#### 9.2 Stabilization Scorecard

**Add at top:**

```markdown
### Gate G6: Stabilization & Handoff

**Gantt Reference:** Phase 9 — Post Launch Scaling (Tasks 9.1-9.11)

**Timeline:** 60-90 days post-launch (data-driven, not calendar-driven)

**G6 is the handoff gate:** When this gate passes, the market transitions from Expansion Playbook governance to GM Playbook governance.

The stabilization scorecard below mirrors **Gate G6 pass criteria** (see Appendix A-9 for complete criteria).

**Critical Principle:** Handoff is scorecard-gated, not date-driven. No amount of calendar pressure should force a premature handoff. The GM inherits a stable, running market — not operational debt.
```

---

## War Room Protocol Clarification

### Key Points to Emphasize Throughout Playbook

**When War Room is Called:**
- Only when a launch date is **deemed at risk**
- Only when there is **no clear path to resolution**
- Called **by VP of Expansion** (not automatically triggered)
- Temporary measure, not standard operating procedure

**Locations to Add War Room Context:**
1. **Section 1.5: Escalation Paths** — Add War Room as highest escalation level. Criteria: "Launch date at risk with no mitigation plan"
2. **Section 8.4: Launch War Room Protocol** — Lead with entry/exit criteria and distinction from Weekly Launch Call
3. **Appendix A-9: Gate definitions** — Note in "Common Failure Modes" when War Room might be invoked (e.g., G3 racking permit delay with no resolution path)

---

## Cross-Reference Architecture

### Recommended Pattern for Every Section

Each playbook section should include:
1. **Gate mapping** (which gates this section supports)
2. **Gantt task reference** (which Smartsheet tasks are covered)
3. **Related appendices** (which templates/checklists apply)
4. **Escalation path** (when to escalate to Weekly Launch Call or War Room)

### Example Template

```markdown
## Section X.X: [Section Title]

**Gate Mapping:** G2 (Compliance & Leadership in Place) → G3 (Facility Ready)
**Gantt Reference:** Phase 4 — Talent Launch (Tasks 4.1-4.11)
**Related Appendices:**
- A-9: Gate G2 criteria
- A-5: New Market GM 30/60/90 Plan
- A-4: Expansion RACI Matrix

**Escalation Path:**
- Yellow status: Report in Weekly Launch Call
- Red status: Escalate to VP of Expansion
- Critical blocker: VP may call War Room
```

### Section Cross-Reference Box Template

Use this template when updating sections:

```markdown
---
### Gate & Timeline Reference

**Gate Checkpoint:** [G0/G1/G2/G3/G4/G5/G6]
**Gantt Phase:** Phase X — [Phase Name]
**Critical Tasks:** [Task numbers with ⚠️ for at-risk items]
**Related Appendices:**
- A-9: Gate [X] criteria
- [Other relevant appendices]

**Escalation:** Report status in Weekly Launch Call (Appendix A-10). VP of Expansion may call War Room if critical path at risk.
---
```

---

## Implementation Priority

### Phase 1: Immediate (Complete)

- [x] Appendix A-10 updates (War Room distinction, attendance, agenda requirements, presentation order)
- [x] Gate integration roadmap documented (this file)

### Phase 2: High Priority (Next Update)

- [ ] Section 7.1 (Sales Enablement) — Add G4 sales enablement reference and MA lesson learned
- [ ] Section 8.1 (Go-Live) — Add G5 reference
- [ ] Section 8.4 (War Room) — Add entry/exit criteria and distinction from Weekly Call
- [ ] Section 9.2 (Stabilization) — Add G6 reference
- [ ] Section 1.5 (Escalation Paths) — Add War Room as highest escalation level

### Phase 3: Medium Priority

- [ ] Section 4.2 (Pre-Launch Checklist) — Add G0, G1, G2 references
- [ ] Section 4.4 (Facility) — Add G1 detailed callout
- [ ] Section 5.2 (GM Hiring) — Add G2 (GM hired) reference
- [ ] Section 5.3 (Field Hiring) — Add G3 (ops & WH hiring) reference

### Phase 4: Lower Priority

- [x] Section 3.2 (Greenlight) — G0 reference added (see section-3.2-market-greenlight-criteria.md)
- [ ] Section 6.2 (Training) — Add G4 (training & certification) reference
- [ ] Section 4.3 (Budget) — Add G0 (budget approval) reference
- [ ] Section 4.5 (Fleet) — Add G4 (vehicle readiness) reference

---

## Maintenance Going Forward

Every time a new section is added or updated:
1. Identify which gate(s) it relates to
2. Add gate mapping callout using template above
3. Reference Gantt tasks from Section 2.1
4. Link to Appendix A-9 for detailed criteria
5. Note escalation path (Weekly Call or War Room)

Every time gates are updated (lessons learned from launches):
1. Update Appendix A-9 (gate criteria)
2. Update Section 2.1 (Gantt timeline if tasks change)
3. Update cross-references in related sections
4. Update Appendix A-10 (Weekly Call agenda if gate reporting changes)

---

## Document Control

**Created:** February 16, 2026
**Purpose:** Roadmap for integrating gate structure throughout Expansion Playbook
**Status:** Ready for implementation
**Next Steps:** Begin with Phase 2 (High Priority) sections, then work through Medium and Lower Priority items
