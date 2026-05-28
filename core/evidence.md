# Evidence Standards

## Evidence Levels

| Level | Criteria | Confidence | Appropriate Claims |
|-------|----------|------------|-------------------|
| Strong | Multiple independent methods converge, robust across subsets, clear visuals | High | "We demonstrate that X causes Y..." |
| Moderate | Single clear analysis, some alternative explanations tested | Medium | "We find evidence that X is associated with Y..." |
| Weak | Pattern exists but ambiguous, limited validation | Low | "We observe a pattern suggesting..." |
| None | Indistinguishable from noise, no clear pattern | Very Low | "We cannot conclude..." |

## Calibration Rules

**Rule 1:** Claims must match evidence strength.
- Overclaiming is scientific dishonesty
- Underclaiming is acceptable conservatism

**Rule 2:** Evidence strength can change with iteration.
- Weak evidence → iterate → moderate evidence
- Stuck at weak → acknowledge limitation

**Rule 3:** Multiple weak analyses ≠ moderate evidence.
- Quality over quantity
- Convergence requires independence

## Evidence Chains

Every finding must trace back to evidence:

```
Finding: "X correlates with Y"
  ↓
Evidence: exp_003 correlation analysis (r=0.72, p<0.01)
  ↓
Method: meth_001 Pearson correlation with bootstrapped CI
  ↓
Data: data_001 processed dataset (n=1500)
  ↓
Source: Original data source with access info
```

If any link is missing, evidence is incomplete.

## Validation Requirements

**For statistical claims:**
- Report effect size, not just p-values
- Check assumptions (normality, independence, etc.)
- Report confidence intervals
- Test robustness

**For visual claims:**
- Inspect every figure before using
- Verify axis labels, units, scales
- Check for visual artifacts
- Confirm pattern matches data

**For causal claims:**
- Require mechanism evidence
- Address confounders explicitly
- Consider counterfactuals
- Test alternative explanations

## Convergence Criteria

**Independence:** Different methods, same finding
- Example: Statistical test + visual pattern + domain validation

**Robustness:** Same method, different data subsets
- Example: Analysis on full data + analysis on each half

**Replication:** Same method, independent data
- Example: Analysis on 2020 data + analysis on 2021 data

Minimum for convergence: 2 independent lines of evidence.

## Handling Weak Evidence

When evidence is weak:

1. **Don't discard** — Investigate why
   - Data quality issue?
   - Method inappropriate?
   - Hypothesis wrong?

2. **Iterate** — Try to strengthen
   - Different method?
   - Additional data?
   - Focused hypothesis?

3. **Acknowledge** — If still weak
   - Report honestly
   - Identify what evidence would strengthen
   - Note as limitation
