# Research State Machine

## Core Concept

The research process is a state machine. Explicit states prevent drift and enable recovery.

## States

```
IDLE
  ↓ (user provides goal)
FORMULATING
  ↓ (question, hypotheses defined)
REVIEWING_LITERATURE
  ↓ (gap identified, position clear)
DESIGNING_METHODS
  ↓ (methods, data sources defined)
PREPARING_DATA
  ↓ (data validated, preprocessed)
RUNNING_EXPERIMENTS
  ↓ (hypotheses tested)
VALIDATING_RESULTS
  ↓ (figures inspected, evidence assessed)
ITERATING
  ↓ (refinement if needed, or proceed)
SYNTHESIZING
  ↓ (findings extracted, chains built)
WRITING
  ↓ (manuscript drafted)
REVIEWING
  ↓ (self-review passed)
COMPLETE
```

## State Definitions

| State | Purpose | Exit Condition |
|-------|---------|----------------|
| IDLE | Waiting for input | User provides goal |
| FORMULATING | Define question, hypotheses | Question specific, 2+ hypotheses |
| REVIEWING_LITERATURE | Survey field, position work | Gap identified, Claim Graph built |
| DESIGNING_METHODS | Plan analysis | Methods match hypotheses |
| PREPARING_DATA | Load, validate, preprocess | Data ready for analysis |
| RUNNING_EXPERIMENTS | Execute methods | All hypotheses tested |
| VALIDATING_RESULTS | Check outputs | Figures inspected, evidence assessed |
| ITERATING | Refine if needed | Convergence or iteration limit |
| SYNTHESIZING | Extract findings | Evidence chains complete |
| WRITING | Produce manuscript | Draft complete |
| REVIEWING | Quality check | Self-review passed |
| COMPLETE | Done | Manuscript finalized |

## State Transitions

Each transition has conditions:

```
FORMULATING → REVIEWING_LITERATURE
  Condition: question defined, hypotheses generated
  Action: Begin literature survey

REVIEWING_LITERATURE → DESIGNING_METHODS
  Condition: gap identified, position in Claim Graph
  Action: Begin method design

DESIGNING_METHODS → PREPARING_DATA
  Condition: methods defined, data sources identified
  Action: Begin data preparation

PREPARING_DATA → RUNNING_EXPERIMENTS
  Condition: data validated, preprocessed
  Action: Begin experiment execution

RUNNING_EXPERIMENTS → VALIDATING_RESULTS
  Condition: all hypotheses tested
  Action: Begin result validation

VALIDATING_RESULTS → ITERATING | SYNTHESIZING
  Condition: results assessed
  Decision:
    - If ambiguous AND iterations < max: ITERATING
    - If clear OR iterations = max: SYNTHESIZING

ITERATING → RUNNING_EXPERIMENTS
  Condition: refinement identified
  Action: Execute refined approach

SYNTHESIZING → WRITING
  Condition: findings extracted, evidence chains complete
  Action: Begin manuscript

WRITING → REVIEWING
  Condition: draft complete
  Action: Begin self-review

REVIEWING → COMPLETE | WRITING
  Condition: review complete
  Decision:
    - If issues found: WRITING (revise)
    - If passed: COMPLETE
```

## State Object

Track current state in orchestrator:

```json
{
  "id": "orch_001",
  "type": "orchestrator",
  "state": "running_experiments",
  "attributes": {
    "current_phase": "RUNNING_EXPERIMENTS",
    "phase_history": [
      {"phase": "FORMULATING", "entered": "2024-01-15T09:00:00", "exited": "2024-01-15T09:30:00"},
      {"phase": "REVIEWING_LITERATURE", "entered": "2024-01-15T09:30:00", "exited": "2024-01-15T10:00:00"},
      {"phase": "DESIGNING_METHODS", "entered": "2024-01-15T10:00:00", "exited": "2024-01-15T10:30:00"},
      {"phase": "PREPARING_DATA", "entered": "2024-01-15T10:30:00", "exited": "2024-01-15T11:00:00"},
      {"phase": "RUNNING_EXPERIMENTS", "entered": "2024-01-15T11:00:00"}
    ],
    "iterations": 0,
    "max_iterations": 3
  }
}
```

## Recovery

If session interrupted:

1. Read orchestrator state
2. Identify current phase
3. Check what's complete
4. Resume from current phase

Example:
```
Session resumes. Orchestrator state: RUNNING_EXPERIMENTS
Check: Which experiments complete? exp_001, exp_002
Check: Which hypotheses tested? hyp_001 (supported), hyp_002 (inconclusive)
Decision: Run additional experiment for hyp_002, then validate
```

## Error Handling

If error in state:

```
RUNNING_EXPERIMENTS → error
  → Log failure event
  → Check failure memory
  → Identify alternative
  → Transition to ITERATING (refine method)
  → Back to RUNNING_EXPERIMENTS
```

## Progress Reporting

At any time, can report:

```
Research Progress:
  Phase: RUNNING_EXPERIMENTS (5 of 11 phases)
  
  Complete:
    - Question formulated
    - 3 hypotheses generated
    - 5 literature sources reviewed
    - 2 methods designed
    - 2 data sources validated
  
  In Progress:
    - Experiment exp_003 running
  
  Pending:
    - Result validation
    - Synthesis
    - Writing
    - Review
  
  Iterations: 0/3
  Experiments: 2/10
```
