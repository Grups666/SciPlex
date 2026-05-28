# Critical Review

## Purpose

Systematic critique of research quality. Identify weaknesses before they become problems.

## Review Dimensions

### 1. Claim Validity

**Question:** Are claims calibrated to evidence?

Check:
- Strong evidence → strong claims ✓
- Moderate evidence → moderate claims ✓
- Weak evidence → strong claims ✗ (overclaiming)
- No evidence → any claim ✗ (fabrication)

Red flags:
- "We prove..." without strong evidence
- "X causes Y" without mechanism
- Broad generalizations from narrow data

### 2. Evidence Chain Completeness

**Question:** Can every claim trace back to data?

For each finding:
```
Finding → Experiment → Method → Data → Source
```

Check:
- All links present?
- All links valid (object exists)?
- Data actually supports claim?

Red flags:
- Claim with no experiment
- Experiment with no data
- Method with no implementation

### 3. Hypothesis Coverage

**Question:** Were all hypotheses tested?

Check:
- Each hypothesis has experiment?
- Results interpreted for each?
- Inconclusive hypotheses acknowledged?

Red flags:
- Hypothesis mentioned but never tested
- Results not mapped to hypotheses
- Selective reporting (only successful tests)

### 4. Confounder Control

**Question:** Are confounders addressed?

For causal claims:
- Confounders identified?
- Control strategy documented?
- Unaddressed confounders acknowledged?

Red flags:
- Causal claim with no confounder analysis
- Ignoring obvious confounders
- Claiming causation from correlation

### 5. Limitation Acknowledgment

**Question:** Are limitations honest?

Check:
- Methodological limitations listed?
- Data limitations listed?
- Generalizability limitations listed?
- Limitations affect conclusions?

Red flags:
- No limitations section
- Limitations not connected to findings
- "No limitations" claim

### 6. Literature Positioning

**Question:** Is work properly positioned?

Check:
- Claim Graph shows position?
- Comparison to existing work?
- Novelty articulated?
- Dependencies acknowledged?

Red flags:
- "No prior work" claim (usually false)
- Ignoring contradictory literature
- Misrepresenting prior findings

## Review Process

```
For each phase:

FORMULATION review:
  - Question specific? Falsifiable?
  - Hypotheses distinct?
  - Scale context defined?

METHOD review:
  - Methods match hypotheses?
  - Data documented?
  - Confounders identified?

EXECUTION review:
  - All hypotheses tested?
  - Figures validated?
  - Failures recorded?

SYNTHESIS review:
  - Evidence chains complete?
  - Claims calibrated?
  - Limitations acknowledged?

WRITING review:
  - Argument logical?
  - Figures embedded?
  - Citations accurate?
```

## Review Object

```json
{
  "id": "rev_001",
  "type": "review",
  "state": "completed",
  "attributes": {
    "phase": "SYNTHESIZING",
    "issues": [
      {
        "dimension": "claim_validity",
        "severity": "major",
        "finding": "find_002",
        "issue": "Strong claim from weak evidence",
        "recommendation": "Reduce claim strength or strengthen evidence"
      },
      {
        "dimension": "confounder_control",
        "severity": "minor",
        "finding": "find_001",
        "issue": "Confounder X not addressed",
        "recommendation": "Acknowledge in limitations"
      }
    ],
    "passed": false,
    "must_fix": ["find_002 overclaiming"],
    "timestamp": "2024-01-15T12:00:00"
  }
}
```

## Severity Levels

| Severity | Meaning | Action |
|----------|---------|--------|
| Critical | Fatal flaw | Must fix before proceeding |
| Major | Significant weakness | Should fix |
| Minor | Small issue | Fix if time permits |
| Suggestion | Improvement idea | Optional |

## Review Triggers

**Mandatory reviews:**
- After each phase (Quality Gate)
- Before manuscript finalization

**Optional reviews:**
- After unexpected results
- After iteration
- When stuck

## Self-Review Mindset

Review as hostile reviewer:

- "What would a critic say?"
- "Where are the weak points?"
- "What would make me reject this?"

Then fix before reviewer sees it.