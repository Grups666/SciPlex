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
   meth_001.attributes:
     - name: "Hotspot Analysis"
     - approach: "Getis-Ord Gi* spatial statistics"
     - parameters: {...}
   
2. Extract design intent
   What exactly was designed?
   - Statistical method: Gi*
   - Significance test: p < 0.05
   - Output: hotspot mask
   
3. Query failure memory
   failures where method_type == "spatial":
   → fail_002: "Gi* requires spatial weights matrix"
   → Adjust: prepare weights matrix before running
   
4. Create implementation checklist
   Required for Gi*:
   - Spatial weights matrix ✓
   - Distance band specification ✓
   - Multiple testing correction ✓
   
5. If missing elements: STOP
   Log failure: "Gi* requires X, not available"
   Choose: implement missing element OR simplify AND document
```

## Unit Understanding (NEW - Critical)

**Common failure pattern: Misunderstanding units**

```
Before any calculation:
  1. Check data units
     - ptotuse: what unit? m³/s or mm/year?
     - Check: variable description in data source
     - Verify: read documentation, not assume
     
  2. Check output units needed
     - Target: mm/year for comparison with storage
     
  3. Conversion plan
     - If mismatch: calculate conversion
     - Document: how converted
     - Validate: check result magnitude
     
  4. Sanity check after conversion
     - 1,969,235 mm/year? → ERROR
     - Should be ~500-2000 mm/year for precipitation
     
Example failure:
  fail_001: "ptotuse in m³/s, treated as mm, absurd result"
  lesson: "Always check units before calculation"
```

## Method Implementation with Fidelity Check (NEW)

```
IMPLEMENTATION_CHECKPOINT:

Phase 1: Initial implementation
  - Implement according to design
  - Checkpoint: does code match design?
  
  checkpoint_check():
    Design: "Getis-Ord Gi* with distance band"
    Code:
      self.hotspot_mask = (use > 0.15) & (tws < -2)  ← threshold!
    
    Mismatch detected!
    
    Decision required:
      A) Fix implementation (implement Gi*)
      B) Revise design AND document why
         - Reason: "Gi* too complex, use threshold"
         - Update: method object
         - Manuscript: "threshold-based hotspots" (not "statistically significant")
      
      Cannot: claim Gi* in manuscript but implement threshold
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
  failures where approach contains "spatial":
  → fail_001: "Threshold substituted for Gi*"
  → lesson: "Don't claim statistical significance for threshold"
  
  # Similar variables
  failures where variables contains "discharge":
  → fail_002: "Discharge ≠ local water availability"
  → lesson: "Use precipitation or runoff per cell"
  
  # Similar domain
  failures where domain == "hydrology":
  → fail_003: "Unit mismatch caused absurd values"
  → lesson: "Check units before calculation"
  
Apply lessons:
  - If Gi* in design: ensure implementation matches
  - If using discharge: don't treat as local availability
  - Before calculation: verify units
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
      "context_tags": ["spatial", "hydrology", "units"],
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

## Example: Handling Physical Sanity Failure

```
Experiment exp_001:
  water_availability = discharge / cell_area
  Result: 1,969,235 mm/year

Sanity check:
  precipitation ~ 500-2000 mm/year
  availability > precipitation? → ERROR
  
Action:
  1. STOP (don't proceed to SYNTHESIZING)
  2. Log failure:
     fail_002:
       approach: "Discharge / cell_area"
       failure_mode: "Discharge is cumulative, not local"
       lesson: "Discharge ≠ water availability"
       alternatives: "Use precipitation or runoff per unit area"
  3. Decision: REFRAME (not just iterate)
     - Discharge concept misunderstood
     - Need to rethink "water availability"
  4. New direction: Use precipitation as availability proxy
```