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
  
  2. Identify problems (NOT just gaps)
     - Load strategy/problem_discovery.md
     - Find contradictions: Paper A says X, Paper B says ¬X
     - Find tensions: Same result, different conditions (scale, time, method)
     - Find inconsistencies: Same method, different results
     - Gaps are weakest—only pursue if clearly important
  
  3. Select problem
     - Evaluate: Is it real? Important? Tractable?
     - Generate question that would resolve it
  
  4. Generate competing hypotheses
     - 2-3 hypotheses that make different predictions
     - Each must be falsifiable
  
  5. Specify evidence patterns
     - What would support H1?
     - What would refute H1?
     - What would support H2?
  
  6. Position in Claim Graph
     - Map hypotheses onto existing debates
     - Identify what's novel
Output: {question, hypotheses[], evidence_patterns[], claim_position, problem}
```

## Literature Integration

Use `references/literature_search.md` for systematic approach.

When provider access is available, use `scripts/literature_search.py` to create
a real candidate pool before creating literature objects:

```bash
python scripts/literature_search.py --workspace <working-directory> \
  --query "<research topic or claim cluster>" \
  --per-page 25 \
  --output literature_candidates.json
```

Candidate files are discovery artifacts, not citations. Create literature
objects only after inspecting candidates for relevance, source role, and
metadata quality.

Before finalizing a publication-style output, run `scripts/audit_literature.py`
when cited literature has provider IDs. Treat provider metadata mismatches as
citation repair work; do not hide them by changing the review verdict alone.
The audit helper attempts provider lookup by stable ID, DOI, and title. If ID
or DOI points to the wrong work, repair the literature object's metadata and
record the repair event before finalization. Small year differences can reflect
online-first versus issue publication dates; wrong titles, wrong DOI, or wrong
provider IDs require correction.

For each paper:
- Extract: question, methods, findings, limitations
- Record: source_role/evidence_role, stable identifier or needs_verification
- Map to Claim Graph: what does this claim? what does it refute?
- Identify: relevance to your question

Stop when:
- Can articulate main approaches in field
- Understand current debates
- Can identify problems (contradictions, tensions)
- Can position your question

Typically: 10-30 papers depending on field maturity.

## Problem Discovery (Critical)

**Load `strategy/problem_discovery.md` for full specification.**

Problem types (in order of value):
1. **Tension** (most valuable): Paper A says X under C1, Paper B says X under C2, conditions conflict
2. **Contradiction**: Paper A says X, Paper B says ¬X (someone must be wrong)
3. **Inconsistency**: Same method gives different results
4. **Unexplained**: Established pattern without mechanism
5. **Gap** (weakest): Nobody studied X (may not matter)

Key insight: Gap ≠ contribution. Contradiction resolution = contribution.

Example tension:
```
Paper A: "Outcome Y is driven by mechanism A" (aggregate scale)
Paper B: "Outcome Y is driven by mechanism B" (local scale)

Problem: Both could be right at different scales
Question: "What is the scale-dependent contribution?"
```

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
    "problem": {
      "id": "prob_001",
      "type": "tension",
      "description": "Paper A finds X at scale S1; Paper B finds Y at scale S2",
      "source_papers": ["lit_001", "lit_003"],
      "resolving_question": "What mediates the difference?"
    },
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
- [ ] Problem identified (contradiction/tension preferred over gap)
- [ ] 2+ hypotheses that make different predictions
- [ ] Each hypothesis is falsifiable
- [ ] Evidence patterns specified for each hypothesis
- [ ] Position in literature identified
- [ ] Scale context defined
