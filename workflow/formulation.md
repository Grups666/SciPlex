# Problem Formulation

## Phase Goal

Transform vague interest → precise question → testable hypotheses.

## Process

```
Input: Research interest or problem statement
Steps:
  1. Survey literature
     - What's known?
     - What's debated?
     - What's unknown?
  
  2. Identify specific question
     - Narrow enough to answer
     - Broad enough to matter
  
  3. Generate competing hypotheses
     - 2-3 hypotheses that make different predictions
     - Each must be falsifiable
  
  4. Specify evidence patterns
     - What would support H1?
     - What would refute H1?
     - What would support H2?
  
  5. Position in Claim Graph
     - Map hypotheses onto existing debates
     - Identify what's novel
Output: {question, hypotheses[], evidence_patterns[], claim_position}
```

## Literature Integration

Use `references/literature_search.md` for systematic approach.

For each paper:
- Extract: question, methods, findings, limitations
- Map to Claim Graph: what does this claim? what does it refute?
- Identify: relevance to your question

Stop when:
- Can articulate main approaches in field
- Understand current debates
- Can identify clear gaps
- Can position your question

Typically: 10-30 papers depending on field maturity.

## Hypothesis Quality

Good hypotheses:
- Make different predictions (distinguishable)
- Are falsifiable (could be proven wrong)
- Connect to theory (not just data mining)
- Are specific (not vague)

Bad hypotheses:
- "X is important" (not testable)
- "X and Y are related" (too vague)
- "X might affect Y" (not falsifiable)

## Output Objects

Create orchestrator object:
```json
{
  "id": "orch_001",
  "type": "orchestrator",
  "state": "formulating",
  "attributes": {
    "question": "Specific research question",
    "hypotheses": [
      {
        "id": "hyp_001",
        "statement": "H1: ...",
        "predictions": ["If H1 true, we expect..."],
        "falsification": ["If H1 false, we expect..."]
      }
    ],
    "claim_position": "How this relates to existing literature",
    "scale_context": {
      "temporal": "...",
      "spatial": "...",
      "organizational": "..."
    }
  }
}
```

## Quality Gate

Before proceeding to Method Design:

- [ ] Question is specific and answerable
- [ ] 2+ hypotheses that make different predictions
- [ ] Each hypothesis is falsifiable
- [ ] Evidence patterns specified for each hypothesis
- [ ] Position in literature identified
- [ ] Scale context defined
