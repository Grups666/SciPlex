# Execution

## Phase Goal

Execute plan, adapt based on results, iterate toward convergence.

## Process

```
Input: {methods, workflow, data}
Steps:
  1. Pre-execution checks
     - Load method objects
     - Check: what was designed to do?
     - List: required implementation elements
     - Query failure memory for similar approaches
  
  2. Data exploration
     - Load data
     - Check structure, quality, missing values
     - UNDERSTAND UNITS (critical!)
     - Visualize distributions
     - Document anomalies
  
  3. Method implementation
     - Implement incrementally
     - CHECKPOINT: Does implementation match design?
     - If mismatch: STOP, log failure, decide
     - Validate each step
     - Generate figures for every result
  
  4. Hypothesis testing
     - Compare results to predictions
     - Which hypotheses supported/refuted?
     - Record evidence strength
  
  5. Sanity checks (before proceeding)
     - Physical values reasonable?
     - Method == design?
     - Objectives addressed?
  
  6. Iteration decision
     - If ambiguous: refine method or hypothesis
     - If absurd: REFRAME (not just iterate)
     - If stuck: check failure memory, try alternative
  
  7. Convergence check
     - Multiple independent analyses?
     - Results robust?
     - Evidence chains complete?
Output: {results[], figures[], decisions_log, failures[]}
```

## Pre-Execution Protocol (NEW)

**Before starting any experiment:**

```
1. Load method object
   meth_XXX.attributes:
     - name: "Method name"
     - approach: "Technical approach"
     - parameters: {...}

2. Extract design intent
   What exactly was designed?
   - Method specification
   - Success criteria
   - Expected output

3. Query failure memory
   failures where method_type == similar:
   → Identify past failures with this approach
   → Adjust: prepare missing prerequisites

4. Create implementation checklist
   Required elements for this method:
   - Prerequisite data/parameters
   - Required transformations
   - Validation criteria

5. If missing elements: STOP
   Log failure: "Method requires X, not available"
   Choose: implement missing element OR simplify AND document
```

## Unit Understanding (NEW - Critical)

**Common failure pattern: Misunderstanding units**

```
Before any calculation:
  1. Check data units
     - Variable: what unit?
     - Check: variable description in data source
     - Verify: read documentation, not assume

  2. Check output units needed
     - Target: required unit for comparison or interpretation

  3. Conversion plan
     - If mismatch: calculate conversion
     - Document: how converted
     - Validate: check result magnitude

  4. Sanity check after conversion
     - Is result magnitude physically plausible?
     - Compare to known reference values if available

Example pattern (generic):
  Failure: "Variable in unit A, treated as unit B, absurd result"
  Lesson: "Always check units before calculation"
```

## Method Implementation with Fidelity Check (NEW)

```
IMPLEMENTATION_CHECKPOINT:

Phase 1: Initial implementation
  - Implement according to design
  - Checkpoint: does code match design?

  checkpoint_check():
    Design: "Method X with parameters Y"
    Code:
      implementation_different_from_design ← mismatch!

    Mismatch detected!

    Decision required:
      A) Fix implementation (align with design)
      B) Revise design AND document why
         - Reason: "Why method changed"
         - Update: method object
         - Manuscript: "Revised method description" (not original claim)

      Cannot: claim Method X in manuscript but implement Method Y
```

## Execution Protocol

**LLM reasons, scripts execute.**

Use `scripts/execute_analysis.py` for reproducible runs:
```bash
python execute_analysis.py \
  --method meth_001 \
  --data data_001 \
  --config '{"param": "value"}'
```

Script handles:
- Deterministic execution
- Logging
- Error handling
- Output organization

LLM handles:
- Method selection
- Parameter choice
- **Fidelity check (implementation == design)**
- Result interpretation
- Sanity check
- Next step decision

## Failure Memory: Active Query (NEW)

**Before every attempt:**
```
query_failure_memory(context):

  # Similar method types
  failures where approach contains similar technique:
  → lesson: "What went wrong with this approach"

  # Similar variables
  failures where variables contains similar type:
  → lesson: "Misinterpretation to avoid"

  # Similar domain
  failures where domain == current_domain:
  → lesson: "Domain-specific pitfalls"

Apply lessons:
  - Check if similar failure mode possible
  - Add preventive check if applicable
  - Document context for future reference
```

**After failure:**
```
Record failure:
  {
    "id": "fail_XXX",
    "type": "failed",
    "attributes": {
      "phase": "RUNNING_EXPERIMENTS",
      "approach": "What was tried",
      "failure_mode": "Why it didn't work",
      "lesson": "What to avoid",
      "alternatives": "What might work",
      "context_tags": ["method_type", "domain", "data_type"],
      "timestamp": "..."
    }
  }
```

## Iteration vs. Reframing Decision (NEW)

```
After VALIDATING_RESULTS:

if results_reasonable():
  → proceed to SYNTHESIZING
  
elif results_need_refinement():
  → ITERATING (max 3)
  
elif results_absurd():
  → REFRAMING (fundamental issue)
  
elif method_implementation != method_design():
  → Decision:
    - If can fix: ITERATING + fix implementation
    - If fundamental mismatch: REFRAMING
```

**Reframing triggers (not just iteration):**
- Physical values absurd (not just off)
- Method fundamentally different from design
- Multiple assumptions invalidated
- Core hypothesis premise wrong

## Quality Gate (Enhanced)

Before proceeding to Synthesis:

- [ ] All hypotheses tested
- [ ] Every result has figure
- [ ] Figures inspected and validated
- [ ] **Method fidelity check passed** (implementation == design)
- [ ] **Physical sanity check passed** (values reasonable)
- [ ] **Unit conversion validated** (magnitude correct)
- [ ] Evidence strength assessed
- [ ] Decisions logged
- [ ] Failures recorded with lessons
- [ ] Failure memory queried for next iteration
- [ ] **Objectives progress checked** (at least attempted all)
- [ ] Iteration limit respected (or reframing triggered)

## Decision Logging

Every decision creates event:

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "action": "checkpoint|iterate|reframe",
  "object_id": "meth_001",
  "reason": "Method fidelity check: threshold != Gi*",
  "decision": "Revise design to threshold-based, update manuscript description"
}
```

## Example: Handling Physical Sanity Failure (Abstract Pattern)

```
Experiment exp_XXX:
  derived_quantity = variable / transformation_factor
  Result: implausible_value

Sanity check:
  reference_value ~ expected_range
  derived_value > reference_value? → ERROR

Action:
  1. STOP (don't proceed to SYNTHESIZING)
  2. Log failure:
     fail_XXX:
       approach: "What was calculated"
       failure_mode: "Why result implausible"
       lesson: "Conceptual misunderstanding"
       alternatives: "Correct approach"
  3. Decision: REFRAME (not just iterate)
     - Variable concept misunderstood
     - Need to rethink the derivation
  4. New direction: Use appropriate proxy or transformation
```