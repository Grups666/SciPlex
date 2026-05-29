# Research Console

## Purpose

Visualize the complete research trajectory from question to conclusion. Make research transparent and auditable.

## Important: Schema vs Runtime Data

**All visual examples in this document are SCHEMAS, not static data.**

- Schema shows structure and format
- Runtime data is auto-generated from research objects
- Agent should NOT copy these examples as actual data
- Agent should generate console content from current research state

This module defines WHAT to visualize and HOW to structure it. The actual content comes from the research objects created during execution.

## Console Architecture

```
sciplex/
└── objects/
    └── console/
        └── index.html    # Interactive console (generated)
```

The console is auto-generated from research objects and updated after each phase.

## Console Components

### 1. Research Timeline

Visual: Horizontal timeline with all phases and transitions

```
IDLE ── FORMULATING ── REVIEWING ── DESIGNING ── PREPARING ── RUNNING ── VALIDATING ── SYNTHESIZING ── WRITING ── REVIEWING ── COMPLETE
         ↓                ↓             ↓                          ↓                    ↓                  ↓
      REFRAMING ←─────────────────────────────────────────────────────────────────────────────────────────────┘
```

Interactive:
- Click any phase → see what happened
- Click transition → see event log
- Click REFRAMING → see problem reconstruction

### 2. Question Evolution

Visual: Tree showing question changes

```
Original Question (Q0)
  ├── Hypotheses
  │   ├── H1: ...
  │   ├── H2: ...
  │   └── H3: ...
  │
  ├── REFRAMING_1: "Question premise wrong"
  │   └── New Question (Q1)
  │       ├── H1': ...
  │       └── H2': ...
  │
  └── Final Question (Q_final)
```

Interactive:
- Expand/collapse each branch
- See rationale for each change
- Link to problem object

### 3. Hypothesis Tracker

Visual: Cards for each hypothesis with status

```
┌─────────────────────────┐
│ H1: Hypthesis statement │
│ Status: SUPPORTED        │
│ Evidence: Strength       │
│ Experiments: N          │
│ ┌─────────────────────┐ │
│ │ exp_XXX: analysis    │ │
│ │ exp_YYY: validation  │ │
│ └─────────────────────┘ │
└─────────────────────────┘

┌─────────────────────────┐
│ H2: Hypthesis statement │
│ Status: REFUTED         │
│ Evidence: Strength       │
│ Experiments: N          │
│ ┌─────────────────────┐ │
│ │ exp_XXX: test        │ │
│ └─────────────────────┘ │
└─────────────────────────┘

┌─────────────────────────┐
│ H3: Hypthesis statement │
│ Status: INCONCLUSIVE    │
│ Evidence: Weak           │
│ Experiments: N          │
│ Needs: Refinement       │
└─────────────────────────┘
```

Interactive:
- Click hypothesis → see evidence chain
- Click experiment → see details and figures
- Status color-coded (green/yellow/red)

### 4. Experiment Trajectory

Visual: Flow diagram showing experiment sequence

```
meth_XXX (method name)
  ↓
exp_XXX ── FAIL ──┐
  ↓                │
fail_XXX: failure description
  ↓                │
ITERATING          │
  ↓                │
meth_XXX' (revised method)
  ↓                │
exp_YYY ───────────┘
  ↓
SUCCESS
  ↓
fig_XXX: Output visualization
```

Interactive:
- Click FAIL → see failure object and lesson
- Click SUCCESS → see results and figures
- Click method → see design vs implementation comparison

### 5. Evidence Accumulation

Visual: Progress bar showing evidence strength

```
Hypothesis H_N:
  [████████░░] 80% → Strong

Evidence lines:
  ✓ exp_XXX: Evidence type A (Moderate)
  ✓ exp_YYY: Evidence type B (Strong)
  ✓ exp_ZZZ: Converges with literature (Moderate)

Convergence: N independent lines
```

Interactive:
- Hover over evidence → see details
- Click → see chain to data

### 6. Assumption Audit

Visual: Dependency graph showing assumptions

```
Finding F_N: "Finding statement"
  │
  ├── [✗] Assumption: Key assumption text
  │     └── INVALIDATED → TRIGGERED REFRAMING
  │
  ├── [✓] Assumption: Another assumption
  │     └── Validated: validation method
  │
  └── [⚠] Assumption: Third assumption
        └── Acknowledged in limitations
```

Color coding:
- Green: validated
- Yellow: acknowledged
- Red: invalidated (blocks finding)

### 7. Claim Graph

Visual: Network graph of literature claims

```
[Paper A: Claim text]
        │
        ├── supports → [Evidence: Data source]
        │
        ├── contradicts → [Paper B: Contradicting claim]
        │                      │
        │                      └── reason for difference
        │
        └── tension_with → [Paper C: Tension claim]
                                  │
                                  └── dimension of tension

[My work]
  └── resolves tension → "Resolution approach"
```

Interactive:
- Click node → see paper object
- Click edge → see relationship type
- Highlight my position in graph

### 8. Failure Memory

Visual: Timeline of failures and lessons

```
fail_XXX: Failure type description
  └── Lesson: What to avoid
  └── Impact: What was blocked
  └── Recovery: How it was resolved

fail_YYY: Another failure description
  └── Lesson: What to avoid
  └── Impact: What was blocked
  └── Recovery: How it was resolved
```

### 9. Objective Progress

Visual: Checklist with status

```
Original Goal: N objectives

[✓] Objective 1: Description
    └── Completed in exp_XXX

[✓] Objective 2: Description
    └── Completed in exp_YYY

[⚠] Objective 3: Description
    └── Partial: progress details

[✗] Objective N: Description
    └── Missing
    └── Reason: Why not completed
    └── Status: Acknowledged as limitation
```

Color coding:
- Green: complete
- Yellow: partial
- Red: missing

### 10. State History

Visual: Interactive timeline with all state transitions

```
Time: ISO-8601 timestamp
State: PREVIOUS_STATE → NEXT_STATE
Reason: Transition trigger description
Guard: PASSED | BLOCKED (reason)

Time: ISO-8601 timestamp
State: VALIDATING_RESULTS → REFRAMING
Reason: Sanity check FAILED
Guard: BLOCKED (check description)

Time: ISO-8601 timestamp
State: REFRAMING → DESIGNING_METHODS
Reason: New direction defined
New Direction: Revised approach description
```

Interactive:
- Click transition → see full event details
- Click guard → see check results
- Filter by state type

## Console Generation

Auto-generated after each phase:

```python
# In orchestrator state update:
def update_console():
    console = {
        "timeline": build_timeline(),
        "question_evolution": build_question_tree(),
        "hypotheses": build_hypothesis_cards(),
        "experiments": build_experiment_flow(),
        "evidence": build_evidence_bars(),
        "assumptions": build_assumption_graph(),
        "claims": build_claim_graph(),
        "failures": build_failure_timeline(),
        "objectives": build_objective_checklist(),
        "history": build_state_history()
    }
    
    write("objects/console/console_data.json", console)
    generate_html("objects/console/index.html", console)
```

## Console Object

```json
{
  "id": "console_XXX",
  "type": "console",
  "state": "active",
  "attributes": {
    "generated_at": "ISO-8601 timestamp",
    "current_phase": "CURRENT_PHASE",
    "file_path": "objects/console/index.html",
    "data_path": "objects/console/console_data.json",
    "components": [
      "timeline",
      "question_evolution",
      "hypothesis_tracker",
      "experiment_trajectory",
      "evidence_accumulation",
      "assumption_audit",
      "claim_graph",
      "failure_memory",
      "objective_progress",
      "state_history"
    ]
  }
}
```

## Access

```
Open in browser: file://<workspace>/sciplex/objects/console/index.html

Features:
- Real-time updates (refresh after each phase)
- Interactive exploration
- Export as PDF (for audit trail)
- Deep links to specific objects
```

## Integration Points

```
After each state transition:
  → update console

After each experiment:
  → update experiment_trajectory
  → update evidence_accumulation

After REFRAMING:
  → update question_evolution
  → update state_history

After REVIEWING:
  → update assumption_audit
  → update objective_progress

On failure:
  → update failure_memory
  → update experiment_trajectory
```