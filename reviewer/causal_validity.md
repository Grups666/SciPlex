# Causal Validity

## Problem

"Pattern = Explanation" is a trap.

Correlation does not imply causation. But causal claims are often what research aims for.

This module provides systematic check for causal validity.

## Causal Claim Requirements

For a valid causal claim, require:

```
├── Mechanism Evidence
│   - What is the causal pathway?
│   - How does X lead to Y?
│   - Is mechanism plausible?
│
├── Confounder Control
│   - What else could cause Y?
│   - Are confounders identified?
│   - Are confounders measured/controlled?
│   - Are unaddressed confounders acknowledged?
│
├── Counterfactual Reasoning
│   - What if X were absent?
│   - Would Y still occur?
│   - Is there comparison group?
│
└── Alternative Explanations
    - What else could explain pattern?
    - Are alternatives tested?
    - Are alternatives acknowledged?
```

## Evidence Levels for Causality

| Level | Evidence | Causal Claim Strength |
|-------|----------|----------------------|
| Strong | Mechanism + Confounder control + Counterfactual + Alternatives tested | "X causes Y" |
| Moderate | Mechanism + Confounder control acknowledged + Counterfactual considered | "X likely contributes to Y" |
| Weak | Mechanism proposed + Confounders listed (not controlled) | "X may influence Y" |
| None | Correlation only | "X is associated with Y" |

## Causal Validity Checklist

For each causal claim:

```
MECHANISM:
  [ ] Causal pathway proposed?
  [ ] Pathway plausible given domain knowledge?
  [ ] Intermediate steps identified?
  [ ] Mechanism testable?

CONFOUNDERS:
  [ ] Potential confounders listed?
  [ ] Each confounder addressed?
      - Measured and controlled statistically?
      - Design minimizes confounder?
      - Acknowledged as limitation?
  [ ] Obvious confounders not ignored?

COUNTERFACTUAL:
  [ ] What if X absent? Considered?
  [ ] Comparison group exists?
      - Experimental: control group
      - Observational: natural comparison
  [ ] Comparison valid (similar conditions)?

ALTERNATIVES:
  [ ] Alternative explanations listed?
  [ ] Alternatives tested where possible?
  [ ] Alternatives acknowledged where not testable?
  [ ] Strongest alternative addressed?
```

## Causal Claim Correction

**Invalid causal claim:**
> "Exposure X causes outcome Y (r=0.72, p<0.01)."

**Analysis:**
- Evidence: correlation only
- Mechanism: missing
- Confounders: not addressed (e.g., policy changes, technology)
- Counterfactual: missing
- Alternatives: not considered

**Correction:**
> "Exposure X is associated with outcome Y (r=0.72, p<0.01). Potential mechanisms are plausible but not directly tested. Confounders such as policy changes, technology adoption, and selection effects were not controlled in this analysis and may contribute to the observed pattern. Causal attribution requires further investigation with confounder control and mechanism validation."

## Causal Reasoning Patterns

### Pattern 1: Mechanism Inference

```
Observation: X correlates with Y
Mechanism: X → Z → Y (mediated path)
Test: Measure Z, check mediation
If mediation confirmed: strengthens causal claim
```

### Pattern 2: Confounder Elimination

```
Observation: X correlates with Y
Confounder: C could cause both X and Y
Test: Measure C, control statistically
If correlation persists after control: strengthens causal claim
```

### Pattern 3: Comparison Group

```
Observation: X correlates with Y in group A
Comparison: Group B similar but X absent
Test: Compare Y in A vs B
If Y different: strengthens causal claim
```

### Pattern 4: Temporal Sequence

```
Observation: X correlates with Y
Temporal: X before Y?
Test: Check timing
If X precedes Y: necessary for causation
If Y precedes X: causation impossible (reverse causality)
```

## Causal Claim Severity

| Severity | Issue | Fix |
|----------|-------|-----|
| Critical | Causal claim with no mechanism | Remove causality, use association |
| Major | Obvious confounder ignored | Address or acknowledge |
| Moderate | Mechanism implausible | Revise mechanism or remove claim |
| Minor | Alternatives not listed | Add alternatives section |

## Preventing Invalid Causal Claims

**Before making causal claim:**
1. Check checklist
2. If any item missing: use association language
3. If strong causal evidence: claim cautiously with caveats

**When evidence is weak:**
- "associated with" not "causes"
- "may influence" not "leads to"
- "related to" not "drives"

**When evidence is moderate:**
- "likely contributes to" with confounder acknowledgment
- "may play a role in" with mechanism proposal

**When evidence is strong:**
- "causes" with mechanism, confounder control, and alternatives
- Still acknowledge residual uncertainty
