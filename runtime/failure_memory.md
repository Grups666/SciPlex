# Failure Memory

## Purpose

Record what didn't work. Avoid repeating mistakes. Learn from failures.

## Failure Philosophy

Failures are data. They constrain the solution space.

- Failed approach → won't work
- Failed assumption → incorrect
- Failed method → inappropriate

Recording failures accelerates convergence by eliminating dead ends.

## Failure Object

```json
{
  "id": "fail_001",
  "type": "failed",
  "state": "recorded",
  "attributes": {
    "timestamp": "2024-01-15T10:30:00",
    "approach": "What was attempted",
    "context": "Why this seemed reasonable",
    "failure_mode": "What went wrong",
    "error_message": "Technical error if any",
    "lesson": "What to avoid next time",
    "alternatives": ["What might work instead"],
    "related_to": "hyp_001"
  }
}
```

## Failure Categories

| Category | Example | Lesson |
|----------|---------|--------|
| Method inappropriate | Correlation on non-linear data | Check assumptions first |
| Data insufficient | Too few samples for ML | Need more data or simpler method |
| Hypothesis wrong | Prediction contradicted | Revise hypothesis |
| Implementation error | Bug in code | Fix and retry |
| Resource exceeded | Timeout | Optimize or simplify |

## Workflow Integration

**Before trying approach:**
```
1. Check failure memory for similar approaches
2. If found: read lesson, consider alternatives
3. If not found: proceed
```

**After approach fails:**
```
1. Record failure object
2. Extract lesson
3. Identify alternatives
4. Log failure event
5. Try alternative
```

## Failure Analysis

Periodically analyze failures:

```
failures where failure_mode = "Method inappropriate"
→ Which methods failed? Why? Pattern?

failures where related_to = "hyp_001"
→ Is hypothesis fundamentally wrong?

failures where timestamp in last_hour
→ Am I stuck in a loop?
```

## Failure Patterns

**Loop detection:**
- Same failure type 3+ times → stop, reassess
- Different failures, same goal → maybe goal wrong

**Failure clustering:**
- Multiple methods fail on same hypothesis → hypothesis may be wrong
- Same method fails on different data → method may be inappropriate

**Learning:**
- After 5+ failures on hypothesis → consider abandoning
- After 10+ total failures → step back, reconsider question

## Example Session

```
Attempt 1: Linear regression on X-Y
→ Fails: Non-linear relationship visible
→ Record: fail_001 (method inappropriate, use non-linear)

Attempt 2: Polynomial regression
→ Fails: Overfitting, poor generalization
→ Record: fail_002 (overfitting, try regularization)

Attempt 3: Regularized polynomial
→ Succeeds: Good fit, robust
→ Lesson: For this data, regularization essential
```

## Failure Memory vs. Results

- Results: what worked
- Failures: what didn't work

Both are essential. Results show the path taken. Failures show paths not taken.

## Querying Failures

**"Why didn't I try X?"**
→ Check if X in failures

**"What have I tried for this hypothesis?"**
→ experiments where hypothesis = H1
→ failures where related_to = H1

**"Am I making progress?"**
→ Compare recent failures to older failures
→ Are failures different? (learning)
→ Are failures same? (stuck)
