# Problem Discovery

## Purpose

Discover research problems from literature—not just "what hasn't been done" but "what needs to be resolved."

## Problem Types

| Type | Definition | Example |
|------|------------|---------|
| Gap | Nobody studied X | "No global assessment of X" |
| Contradiction | Paper A says X, Paper B says ¬X | "A: groundwater increasing; B: decreasing" |
| Tension | Paper A says X under condition C1, Paper B says X under C2, conditions conflict | "A: trend positive at basin scale; B: negative at point scale" |
| Inconsistency | Same method gives different results | "A's trend: +2mm/yr; B's same method: -3mm/yr" |
| Unexplained | Established pattern without explanation | "All studies show X, but mechanism unclear" |

## Gap vs. Contradiction vs. Tension

**Gap ( weakest problem):**
```
"Nobody studied groundwater decline in North China Plain"

Problem: 
  - May not matter
  - Gap ≠ contribution
  - Could be gap because it's trivial

Check: Why hasn't it been studied?
  - Too trivial? → not good problem
  - Too hard? → good problem
  - Data unavailable? → now available? → good problem
```

**Contradiction (stronger problem):**
```
Paper A: "Groundwater sustainable in North China Plain"
Paper B: "Groundwater depletion critical in North China Plain"

Problem:
  - Direct conflict
  - Someone must be wrong
  - Resolution has value

Check:
  - Same definition of "sustainable"?
  - Different time periods?
  - Different data sources?
  
Resolution path:
  - Compare definitions
  - Check methods
  - Reconcile or decide
```

**Tension (most subtle, often most valuable):**
```
Paper A: "TWS decline driven by groundwater extraction"
         (at basin scale, 2000-2015)
Paper B: "TWS decline driven by climate variability"
         (at point scale, 2000-2015)

Problem:
  - Both could be right at different scales
  - Scale mismatch creates tension
  - Resolution: "At what scale does each dominate?"

Check:
  - What differs? (scale, time, method, definition)
  - Can both be right?
  - What question would reconcile?

Tension → new question:
  "What is the scale-dependent contribution of extraction vs. climate?"
```

## Discovery Process

### Phase 1: Literature Survey

```
For each paper read:

1. Extract claims
   - Main claim
   - Supporting claims
   - Assumptions

2. Build Claim Graph
   - Claim → evidence → method → data
   - Position in debate landscape

3. Find connections
   - Same topic? → compare claims
   - Similar method? → check consistency
   - Same region? → check scale alignment
```

### Phase 2: Problem Identification

```
Compare claims across papers:

For each pair of papers (A, B) on same topic:

  if A.claim contradicts B.claim:
    → contradiction_type: direct
    → problem: "Why do A and B disagree?"
    → value: high (resolution matters)
    
  elif A.claim == B.claim but conditions differ:
    → check conditions:
      - time period? → temporal tension
      - spatial scale? → scale tension  
      - definition? → definitional tension
      - method? → methodological tension
    → problem: "What reconciles the tension?"
    → value: high (nuanced understanding)
    
  elif A.result != B.result with same method:
    → inconsistency
    → problem: "Why does same method give different results?"
    → value: medium (method reliability)
    
  elif all papers agree but mechanism missing:
    → unexplained pattern
    → problem: "What causes this established pattern?"
    → value: medium (mechanistic insight)
```

### Phase 3: Problem Evaluation

```
For each identified problem:

Evaluate:
  1. Is it real?
     - Check: are papers actually contradictory/tense?
     - Or: just different contexts?
     
  2. Is it important?
     - Resolution would affect field?
     - Policy implications?
     - Methodological advance?
     
  3. Is it tractable?
     - Data available?
     - Methods exist?
     - Within scope?

  4. What question would address it?
     - For contradiction: "Which is right and why?"
     - For tension: "What mediates the difference?"
     - For inconsistency: "What explains the variance?"
```

## Problem Object

```json
{
  "id": "prob_001",
  "type": "problem",
  "state": "identified",
  "attributes": {
    "problem_type": "tension",
    "description": "Paper A finds extraction-driven decline at basin scale; Paper B finds climate-driven at point scale",
    "papers_involved": ["lit_001", "lit_003"],
    "tension_dimension": "scale",
    "value": "high",
    "tractability": "high",
    "resolving_question": "What is the scale-dependent contribution of extraction vs. climate to TWS decline?",
    "hypotheses_generated": ["hyp_001", "hyp_002"]
  }
}
```

## Claim Graph Construction

```
Claim Graph structure:

Nodes:
  - Claims (paper assertions)
  - Evidence (data, methods)
  - Assumptions

Edges:
  - supports: A supports B
  - contradicts: A contradicts B
  - depends_on: A depends on assumption
  - tension_with: A tense with B (same result, different context)

Example:

[Claim: TWS declining in NCP]
  ↓ supports
[Evidence: GRACE trend -5mm/yr]
  ↓ depends_on
[Assumption: GRACE captures groundwater]

[Claim: TWS stable in NCP]
  ↓ contradicts
[Claim: TWS declining in NCP]

[Claim: Decline driven by extraction]
  ↓ tension_with (scale differs)
[Claim: Decline driven by climate]
```

## Integration with Formulation

```
FORMULATING → REVIEWING_LITERATURE
  ↓
Build Claim Graph
  ↓
Identify:
  - Gaps (what's missing)
  - Contradictions (what's conflicting)
  - Tensions (what's nuanced)
  ↓
Evaluate problems
  ↓
Select most valuable + tractable
  ↓
Generate question from problem
  ↓
Question object with problem_link
```

## Question-Problem Mapping

```json
{
  "id": "q_001",
  "type": "question",
  "attributes": {
    "statement": "What mediates extraction vs. climate contributions at different scales?",
    "origin": {
      "problem_id": "prob_001",
      "problem_type": "tension",
      "source_papers": ["lit_001", "lit_003"]
    },
    "novelty": "Reconciles scale-dependent findings",
    "importance": "Affects attribution for policy"
  }
}
```

## Output

Problem discovery produces:
- Problem objects (identified from literature)
- Claim Graph (visualizable)
- Problem-to-question mapping
- Value/tractability assessment