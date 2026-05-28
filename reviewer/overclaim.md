# Overclaim Detection

## Problem

LLMs tend to overclaim. Pattern observation becomes definitive conclusion. Weak evidence becomes proof.

This is scientific dishonesty. Must be caught and corrected.

## Overclaim Patterns

| Weak Evidence | Overclaim | Correct Claim |
|---------------|-----------|---------------|
| Single correlation | "X causes Y" | "X correlates with Y" |
| Pattern visible | "We demonstrate..." | "We observe a pattern..." |
| Limited data | "This shows..." | "In this sample, we find..." |
| Ambiguous result | "We prove..." | "Evidence suggests..." |
| No validation | "The analysis shows..." | "The analysis suggests..." |

## Detection Rules

**Rule 1: Causal words require causal evidence**

Words: "causes", "leads to", "results in", "drives", "produces"

Required evidence:
- Mechanism demonstrated
- Confounders controlled
- Counterfactual considered
- Alternatives tested

If missing: Replace with "associated with", "correlated with", "related to"

**Rule 2: Strong verbs require strong evidence**

| Verb | Minimum Evidence |
|------|-------------------|
| demonstrate, prove, establish | Strong (convergence) |
| show, find, reveal | Moderate (clear analysis) |
| observe, suggest, indicate | Weak (pattern exists) |
| cannot conclude | None |

Check: Does evidence level match verb?

**Rule 3: Generalizations require scope statement**

Bad: "X correlates with Y"
Good: "In this sample (n=500, US cities 2010-2020), X correlates with Y"

Always specify:
- Sample size
- Population/context
- Time/space scope

**Rule 4: Certainty requires validation**

Bad: "The result is..."
Good: "The result appears to be... (validated by robustness check)"

Certainty words: "is", "shows", "clearly", "obviously", "definitely"
Qualified words: "appears", "suggests", "indicates", "likely"

Replace certainty with qualification unless validated.

**Rule 5: Claims must match hypothesis**

If hypothesis: "X correlates with Y"
Claim: "X correlates with Y" ✓

If hypothesis: "X causes Y"
Claim: "X correlates with Y" ✗ (underclaiming, but honest)
Claim: "X causes Y" ✗✗ (overclaiming if evidence weak)

Better: Revise hypothesis to match what can actually test.

## Overclaim Review Process

```
For each finding:

1. Extract claim verbs
   - "demonstrates", "shows", "suggests"

2. Check evidence level
   - Strong, Moderate, Weak, None

3. Compare verb to evidence
   - Verb too strong? → Overclaim
   - Verb appropriate? ✓

4. Check scope
   - Generalization without scope? → Overclaim

5. Check causality
   - Causal word without causal evidence? → Overclaim

6. Generate correction
   - Replace verb with appropriate one
   - Add scope context
   - Remove causal words if unsupported
```

## Examples

**Overclaim:**
> "Our analysis demonstrates that groundwater depletion causes agricultural decline."

**Detection:**
- Verb: "demonstrates" (requires Strong)
- Evidence: correlation analysis (Moderate)
- Causal word: "causes" (requires causal evidence)
- Scope: missing

**Correction:**
> "Our analysis suggests groundwater depletion is associated with agricultural decline in this study region (North China Plain, 2000-2019). Mechanisms and confounders require further investigation."

**Overclaim:**
> "We prove that the new method outperforms existing approaches."

**Detection:**
- Verb: "prove" (requires Strong)
- Evidence: single comparison test (Moderate)
- Scope: missing (what methods, what data?)

**Correction:**
> "We find evidence that the new method performs better than existing approaches on this benchmark dataset (n=100). Robustness across other datasets requires validation."

## Overclaim Severity

| Severity | Overclaim Type | Fix Priority |
|----------|---------------|--------------|
| Critical | Fabrication (no evidence) | Must fix immediately |
| Major | Causal claim without evidence | Must fix before proceed |
| Moderate | Strong verb, weak evidence | Should fix |
| Minor | Missing scope context | Fix if time permits |

## Prevention

**Write findings with calibration:**
- Start with evidence level
- Choose verb to match
- Add scope context
- Remove unsupported causal words
- Acknowledge limitations

**Review before finalizing:**
- Run overclaim detection
- Fix identified issues
- Re-review until clean