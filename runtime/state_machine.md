# Research State Machine

## Core Concept

Research is NOT a linear pipeline. It's a **graph with cycles**.

Real research:
```
Question → try method → realize question wrong → reframe → new question → ...
```

This state machine supports:
1. Linear progression (when things work)
2. Backward jumps (when发现问题)
3. Problem reframing (when question itself is wrong)

## State Graph

```
                    ┌─────────────────────────────────────┐
                    │                                     │
                    ▼                                     │
IDLE → FORMULATING → REVIEWING_LITERATURE → DESIGNING_METHODS
         │                    │                    │
         │                    │                    │
         │         ┌──────────┴──────────┐         │
         │         │                     │         │
         │         ▼                     ▼         │
         │    REFRAMING ←────────── REFRAMING     │
         │         │                     │         │
         │         └─────────────────────┘         │
         │                                     │
         ▼                                     ▼
      PREPARING_DATA → RUNNING_EXPERIMENTS → VALIDATING_RESULTS
                              │                    │
                              │                    │
                              ▼                    ▼
                           ITERATING ←─────── ITERATING
                              │
                              ▼
                         REFRAMING (if fundamental issue)
                              │
                              └─────────────→ 回到任意状态

VALIDATING_RESULTS → SYNTHESIZING → WRITING → REVIEWING → COMPLETE
```

## States

| State | Purpose | Can Jump Back To |
|-------|---------|------------------|
| IDLE | Waiting for input | - |
| FORMULATING | Define question, hypotheses | - |
| REVIEWING_LITERATURE | Survey field, build Claim Graph | FORMULATING |
| DESIGNING_METHODS | Plan analysis, evaluate strategy | FORMULATING, REVIEWING_LITERATURE |
| PREPARING_DATA | Load, validate data | - |
| RUNNING_EXPERIMENTS | Execute methods | DESIGNING_METHODS |
| VALIDATING_RESULTS | Check outputs, sanity check | DESIGNING_METHODS, PREPARING_DATA |
| ITERATING | Refine approach | DESIGNING_METHODS |
| REFRAMING | **Reconstruct the problem itself** | ANY state (restart) |
| SYNTHESIZING | Extract findings | RUNNING_EXPERIMENTS |
| WRITING | Produce manuscript | SYNTHESIZING |
| REVIEWING | Quality check | ANY state (if critical flaw) |
| COMPLETE | Done | - |

## REFRAMING State (Critical Addition)

**When to enter REFRAMING:**
- Question assumptions prove invalid
- Multiple iterations fail for same hypothesis
- Evidence contradicts question premise
- Realize "we're solving the wrong problem"

**What happens in REFRAMING:**
```
1. Audit: What assumptions failed?
2. Reconstruct: What's the real problem?
3. Decide: 
   - New question? → back to FORMULATING
   - New approach? → back to DESIGNING_METHODS
   - Different scale? → back to REVIEWING_LITERATURE
```

**Reframing triggers:**
```
- 3+ failures for same hypothesis
- Physical calculation yields absurd values (sanity check fail)
- Method implementation fundamentally different from design
- Question's premise contradicted by data
```

## State Transitions with Guards

Each transition now has a **guard** (sanity check):

```
FORMULATING → REVIEWING_LITERATURE
  Guard: question defined, hypotheses falsifiable
  Action: Begin literature survey

REVIEWING_LITERATURE → DESIGNING_METHODS
  Guard: gap identified, Claim Graph built, contradictions noted
  Action: Begin method design
  Can also: → REFRAMING (if gap is false)

DESIGNING_METHODS → PREPARING_DATA
  Guard: methods defined, strategy evaluated, assumptions listed
  Action: Begin data preparation
  Can also: → REFRAMING (if methods can't address question)

PREPARING_DATA → RUNNING_EXPERIMENTS
  Guard: data validated, physical units correct
  Action: Begin experiment execution

RUNNING_EXPERIMENTS → VALIDATING_RESULTS
  Guard: all planned experiments executed
  Action: Begin result validation
  Can also: → ITERATING (if partial results need refinement)

VALIDATING_RESULTS → SYNTHESIZING | ITERATING | REFRAMING
  Guard: sanity checks pass
  Decision tree:
    - Results reasonable? → SYNTHESIZING
    - Results need refinement? → ITERATING
    - Results absurd? → REFRAMING
    - Method != design? → REFRAMING

ITERATING → RUNNING_EXPERIMENTS | REFRAMING
  Guard: refinement plan defined
  Decision:
    - If iteration < max: RUNNING_EXPERIMENTS
    - If iterations exhausted: REFRAMING or acknowledge limitation

REFRAMING → ANY STATE
  Guard: new direction defined, reason documented
  Action: Jump to appropriate state with new context

SYNTHESIZING → WRITING
  Guard: evidence chains complete, findings calibrated
  Action: Begin manuscript

WRITING → REVIEWING
  Guard: draft complete
  Action: Begin self-review

REVIEWING → COMPLETE | WRITING | REFRAMING
  Guard: review complete
  Decision:
    - Minor issues: WRITING (revise)
    - Passed: COMPLETE
    - Critical flaw: REFRAMING (fundamental problem found)
```

## Output Generation

Each state transition produces:

```
1. Event log entry (events.json)
   - timestamp, action, object_id, state_before, state_after, reason

2. Console update (objects/console/)
   - Auto-generated from research objects
   - 10 components: timeline, hypotheses, experiments, evidence, assumptions, claims, failures, objectives, history
   - Location: objects/console/ (follows object system structure)

3. State update (state.json)
   - Current phase, object counts, last_updated
```

Console generation is automatic, not optional. It provides the audit trail for research transparency.

## Transition Guards (Sanity Checks)

**Guard at VALIDATING_RESULTS:**
```
sanity_check():
  1. Method fidelity check
     - Implemented method == designed method?
     - If not: log failure, block SYNTHESIZING

  2. Physical sanity check
     - Values in reasonable range?
     - Check: derived values vs expected bounds
     - Check: ratios and proportions meaningful

  3. Objective completion check
     - All stated objectives addressed?
     - If missing: block SYNTHESIZING, force ITERATING

  4. Assumption audit
     - Critical assumptions still valid?
     - If invalidated: block, force REFRAMING
```

**Guard at REVIEWING:**
```
critical_review():
  1. What would invalidate this entire paper?
     - List critical assumptions
     - Check each: validated? acknowledged?

  2. Method-claim consistency
     - Manuscript claims match actual method?
     - If mismatch: scientific dishonesty flag

  3. Objective completion
     - All objectives from original goal addressed?
     - If missing: incomplete, cannot COMPLETE
```

## State Object

```json
{
  "id": "orch_001",
  "type": "orchestrator",
  "state": "running_experiments",
  "attributes": {
    "current_phase": "RUNNING_EXPERIMENTS",
    "phase_history": [...],
    "reframing_history": [
      {
        "trigger": "Reason for reframing",
        "from_phase": "PREVIOUS_PHASE",
        "reason": "What assumption failed",
        "new_direction": "What changed",
        "timestamp": "ISO-8601"
      }
    ],
    "iterations": 0,
    "max_iterations": 3,
    "reframing_count": 0,
    "max_reframing": 2
  }
}
```

## Research Strategy (Design Phase)

When in DESIGNING_METHODS, evaluate strategy:

```
For each hypothesis, list possible methods:

Method A:
  - cost: low (simple computation)
  - information_gain: medium (answers part of question)
  - risk: low (well-established)

Method B:
  - cost: high (complex computation)
  - information_gain: high (answers full question)
  - risk: medium (requires assumptions)

Strategy:
  1. Try Method A first (low cost probe)
  2. If inconclusive, escalate to Method B
  3. Document strategy in method object
```

## Recovery After Reframing

Reframing doesn't restart everything:
- Literature already reviewed → keep Claim Graph
- Data already loaded → keep validated data
- Only: reconstruct question and methods

```
REFRAMING → FORMULATING
  Keep: literature objects, data objects (validated)
  Discard: hypothesis objects, method objects
  Generate: new hypotheses for reframed question
```

## Progress Reporting

```
Research Progress:
  Phase: CURRENT_PHASE

  Reframings: N/MAX
    - Reason: "Why reframing occurred"
    - New direction: "What changed"

  Iterations: N/MAX

  Objectives:
    ✓ Objective 1: Completed
    ✓ Objective 2: Completed
    ⏳ Objective N: In progress
    ✗ Objective M: Pending

  Critical Assumptions:
    ✓ Assumption A: Validated
    ✓ Assumption B: Validated
    ⚠ Assumption C: INVALIDATED → triggered reframing
```