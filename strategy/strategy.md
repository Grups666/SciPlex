# Research Strategy Layer

## Purpose

Decide **which experiments to run**, not just **how to run them**.

This layer bridges workflow/ and runtime/: workflow defines what to do, strategy decides what to do first.

## Core Problem

Research has limited resources:
- Token budget
- Computation time
- Experiment slots (max 10)
- Reframing budget (max 2)

The question: **Given multiple valid methods, which one should we try first?**

## Strategy Framework

### 1. Method Evaluation Matrix

For each hypothesis, evaluate all candidate methods:

```json
{
  "id": "strat_001",
  "type": "strategy",
  "attributes": {
    "hypothesis_id": "hyp_001",
    "candidate_methods": [
      {
        "method_id": "meth_a",
        "name": "Simple threshold analysis",
        "cost": {
          "computation": "low",
          "tokens": "~1000",
          "time": "minutes"
        },
        "information_gain": {
          "answers_question": "partial",
          "distinguishes_hypotheses": "no",
          "provides_bounds": "yes"
        },
        "risk": {
          "assumption_dependency": "low",
          "failure_probability": "low",
          "if_fails": "low cost to retry"
        },
        "score": 0.6
      },
      {
        "method_id": "meth_b",
        "name": "Getis-Ord Gi* spatial statistics",
        "cost": {
          "computation": "medium",
          "tokens": "~3000",
          "time": "hours"
        },
        "information_gain": {
          "answers_question": "full",
          "distinguishes_hypotheses": "yes",
          "provides_bounds": "no"
        },
        "risk": {
          "assumption_dependency": "medium",
          "failure_probability": "medium",
          "if_fails": "need alternative approach"
        },
        "score": 0.75
      }
    ],
    "selected_sequence": ["meth_a", "meth_b"],
    "rationale": "Try low-cost probe first. If inconclusive, escalate to full method."
  }
}
```

### 2. Scoring Formula

```
score = information_gain / (cost × risk)

Where:
  information_gain = answers_question + distinguishes_hypotheses + provides_bounds
  cost = computation + tokens + time
  risk = assumption_dependency + failure_probability + recovery_cost
```

Normalization:
- All factors normalized to [0, 1]
- Higher score = better strategy

### 3. Escalation Strategy

```
Strategy patterns:

Pattern A: Low-cost probe → Full method
  1. Try simple analysis (threshold, basic correlation)
  2. If pattern visible: escalate to rigorous method
  3. If no pattern: save resources, try different approach

Pattern B: Parallel low-risk methods
  1. Run multiple simple analyses concurrently
  2. Convergence = strong evidence
  3. Divergence = need deeper investigation

Pattern C: Single high-information method
  1. When hypothesis requires specific method (e.g., causal inference)
  2. Skip probes, go directly
  3. Accept higher risk for necessary information
```

### 4. Resource Budgeting

```json
{
  "resource_budget": {
    "total_experiments": 10,
    "allocated": {
      "hyp_001": 3,
      "hyp_002": 3,
      "hyp_003": 2,
      "reserve": 2
    },
    "token_budget": 50000,
    "reframing_budget": 2
  }
}
```

**Budget rules:**
- Reserve 20% for unexpected needs
- Max 3 experiments per hypothesis before escalating
- Track budget consumption in orchestrator

### 5. Exploration vs. Exploitation

**Exploration:** Try new approaches, gather information about problem space

**Exploitation:** Deepen existing findings, refine established methods

```
Early phases (FORMULATION, LITERATURE): exploration-heavy
  - Survey approaches
  - Test multiple hypotheses
  - Gather information about problem

Middle phases (EXECUTION): exploitation-heavy
  - Focus on promising methods
  - Deepen analysis
  - Refine results

Late phases (SYNTHESIS): balanced
  - Validate findings (exploitation)
  - Check unexpected patterns (exploration)
```

**Decision rule:**
```
if exploration_ratio > 0.7 and iterations < 2:
  // Try new approach
elif exploitation_ratio > 0.8 and evidence_strength == "weak":
  // Need more exploration
else:
  // Balance based on phase
```

## Strategy Decision Tree

```
At DESIGNING_METHODS phase:

1. List all candidate methods for each hypothesis
2. Score each method
3. Group by risk level:
   - Low-risk: can try in parallel
   - Medium-risk: try sequentially
   - High-risk: use as last resort

4. Sequence:
   a. Low-cost + low-risk methods first (probes)
   b. If probes inconclusive: escalate to medium
   c. If still inconclusive: high-risk or REFRAME

5. Document strategy in strategy object
6. Update budget allocation
```

## Strategy Object

```json
{
  "id": "strat_001",
  "type": "strategy",
  "state": "evaluated",
  "attributes": {
    "phase": "DESIGNING_METHODS",
    "hypothesis_id": "hyp_001",
    "candidates": [...],
    "selected_sequence": ["meth_a", "meth_b"],
    "rationale": "Probe → Escalate pattern",
    "budget_allocation": {
      "experiments": 3,
      "tokens": 10000
    },
    "exploration_ratio": 0.3,
    "fallback_if_fails": "meth_c or REFRAME",
    "timestamp": "2024-01-15T10:00:00"
  }
}
```

## Integration with State Machine

**Strategy evaluation at DESIGNING_METHODS:**

```
State transition: REVIEWING_LITERATURE → DESIGNING_METHODS

Action:
  1. Load method candidates
  2. Apply strategy framework
  3. Create strategy objects
  4. Allocate budgets
  5. Document sequence

Guard before PREPARING_DATA:
  - Strategy objects created?
  - Budget allocated?
  - Fallback defined?
```

## Failure Integration

**When method fails:**

```
After failure logged:
  1. Check strategy object
  2. Is this expected failure (in plan)?
     - Yes: proceed to next method in sequence
     - No: update strategy, reconsider approach
  3. Budget consumed?
     - If over budget: escalate or REFRAME
     - If under budget: continue planned sequence
```

## Output

Strategy layer produces:
- Strategy objects (for each hypothesis)
- Budget allocation plan
- Method sequence with rationale
- Fallback plans
- Exploration/exploitation balance