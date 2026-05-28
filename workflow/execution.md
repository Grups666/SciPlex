# Execution

## Phase Goal

Execute plan, adapt based on results, iterate toward convergence.

## Process

```
Input: {methods, workflow, data}
Steps:
  1. Data exploration
     - Load data
     - Check structure, quality, missing values
     - Visualize distributions
     - Document anomalies
  
  2. Method implementation
     - Implement methods incrementally
     - Validate each step
     - Generate figures for every result
  
  3. Hypothesis testing
     - Compare results to predictions
     - Which hypotheses supported/refuted?
     - Record evidence strength
  
  4. Iteration
     - If ambiguous: refine method or hypothesis
     - If unexpected: investigate (artifact or finding?)
     - If stuck: check failure memory, try alternative
  
  5. Convergence check
     - Multiple independent analyses?
     - Results robust?
     - Evidence chains complete?
Output: {results[], figures[], decisions_log, failures[]}
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
- Result interpretation
- Next step decision

## Figure Generation

Use `references/figure_guidelines.md` for best practices.

For every result, generate figure:
- Visualize the pattern
- Inspect before using
- Verify it shows what you claim
- Create complete caption

Figure object:
```json
{
  "id": "fig_001",
  "type": "figure",
  "state": "finalized",
  "attributes": {
    "name": "Figure name",
    "purpose": "What it shows",
    "type": "scatter|histogram|map|...",
    "caption": "Complete caption with data source",
    "key_pattern": "What pattern is visible",
    "data_source": "exp_001",
    "file_path": "objects/figure/fig_001.png"
  }
}
```

## Iteration Strategy

**Resource bounds:**
- Max iterations per hypothesis: 3
- Max total experiments: 10
- Convergence criteria: 2+ independent analyses agree

**When results are ambiguous:**
1. Check assumptions
2. Try alternative method
3. Refine hypothesis
4. After 3 iterations: acknowledge limitation

**When results are unexpected:**
1. Investigate first, don't dismiss
2. Could be artifact? Check data, code
3. Could be real finding? Document, test further
4. Could be method failure? Try alternative

## Failure Memory

Record what didn't work:

```json
{
  "id": "fail_001",
  "type": "failed",
  "attributes": {
    "approach": "What was tried",
    "failure_mode": "Why it didn't work",
    "lesson": "What to avoid",
    "alternatives": "What might work instead",
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

Before trying approach: Check failure memory.
After approach fails: Record it.

## Decision Logging

Every decision creates event:

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "action": "iterate",
  "object_id": "meth_001",
  "reason": "Results ambiguous, refining method",
  "decision": "Add robustness check"
}
```

## Quality Gate

Before proceeding to Synthesis:

- [ ] All hypotheses tested
- [ ] Every result has figure
- [ ] Figures inspected and validated
- [ ] Evidence strength assessed
- [ ] Decisions logged
- [ ] Failures recorded
- [ ] Iteration limit respected
