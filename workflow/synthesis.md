# Synthesis

## Phase Goal

Transform results → coherent findings with evidence chains.

## Process

```
Input: {results, figures, hypotheses}
Steps:
  1. Hypothesis summary
     - Which hypotheses supported?
     - Which refuted?
     - Evidence strength for each?
  
  2. Evidence chains
     - For each finding: trace back to evidence
     - Finding → Experiment → Method → Data
     - Identify any gaps
  
  3. Literature comparison
     - How do findings compare to existing work?
     - Confirm, extend, contradict?
     - Position in Claim Graph
  
  4. Limitation analysis
     - What couldn't be tested?
     - What assumptions unverified?
     - What confounders unaddressed?
  
  5. Implication extraction
     - What do findings mean?
     - What are practical implications?
     - What are theoretical implications?
Output: {findings[], evidence_chains, limitations[], implications[]}
```

## Finding Documentation

For each finding, create object:
```json
{
  "id": "find_001",
  "type": "finding",
  "state": "validated",
  "attributes": {
    "statement": "Clear statement of finding",
    "hypothesis": "hyp_001",
    "support": "supported|refuted|inconclusive",
    "evidence_strength": "strong|moderate|weak",
    "evidence_chain": [
      "exp_001: correlation analysis",
      "exp_002: robustness check",
      "fig_001: visual confirmation"
    ],
    "limitations": ["Limitation 1"],
    "comparison_to_literature": "How this relates to existing work"
  }
}
```

## Evidence Chain Construction

Every finding must have complete chain:

```
Finding: "X correlates with Y (r=0.72, p<0.01)"
  ↓
Experiment: exp_001
  ↓
Method: meth_001 (Pearson correlation)
  ↓
Data: data_001 (n=1500, cleaned)
  ↓
Source: Original data with access info
```

If chain incomplete:
- Identify missing link
- Either complete it or acknowledge as limitation

## Literature Comparison

For each finding, compare:

```
This study: X correlates with Y (r=0.72)
Smith 2020: X correlates with Y (r=0.65) — CONFIRMS
Jones 2021: No correlation found — CONTRADICTS

Resolution: Different context? Different method? Different scale?
```

Position in Claim Graph:
- Does this extend existing claims?
- Does this challenge existing claims?
- Does this synthesize competing claims?

## Limitation Acknowledgment

Be honest about limitations:

**Methodological:**
- Assumptions that couldn't be verified
- Methods that couldn't be applied
- Analyses that couldn't be completed

**Data:**
- Coverage gaps
- Quality issues
- Temporal/spatial limitations

**Causal:**
- Confounders not controlled
- Mechanism not demonstrated
- Counterfactuals not tested

**Generalizability:**
- Scale limitations
- Context specificity
- Sample constraints

## Implication Extraction

**Practical implications:**
- What should practitioners do differently?
- What policies should change?
- What interventions might work?

**Theoretical implications:**
- What does this mean for theory?
- What mechanisms are suggested?
- What new questions arise?

**Future work:**
- What questions remain?
- What would strengthen evidence?
- What should be studied next?

## Quality Gate

Before proceeding to Communication:

- [ ] All hypotheses have findings
- [ ] Evidence chains complete
- [ ] Literature compared
- [ ] Limitations acknowledged
- [ ] Implications extracted
- [ ] Findings calibrated to evidence strength
