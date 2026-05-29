# Critical Review

## Purpose

Systematic critique of research quality. Identify weaknesses **before they become fatal flaws**.

## Review Philosophy

Not just "what are the limitations?" but:
- "What would make this entire paper invalid?"
- "What assumptions are we depending on?"
- "Did we actually do what we claimed?"

## Review Dimensions

### 1. Method Fidelity (NEW - Critical)

**Question:** Did we implement what we designed?

Check:
```
For each method object:
  - Design: "Use Getis-Ord Gi* spatial statistics"
  - Implementation: Check actual code
  - Match? YES/NO

Red flags:
- Designed: Gi* → Implemented: threshold (降级)
- Designed: k-means → Implemented: manual classification (降级)
- Manuscript claims "statistically significant" but code uses ad-hoc threshold
```

**Severity: CRITICAL if mismatch**

This is scientific dishonesty, not just limitation.

### 2. Physical Sanity (NEW - Critical)

**Question:** Do the numbers make physical sense?

Domain-specific checks:

**For hydrology:**
```
- Water availability > Precipitation? → ERROR
- Groundwater depletion > Recharge + Extraction? → ERROR
- TWS trend globally positive while climate change suggests negative? → QUESTION
- Values 10x off from literature? → ERROR
```

**For general analysis:**
```
- Values within known physical bounds?
- Orders of magnitude reasonable?
- Trends match established patterns (or have explanation)?
```

**What to do if fails:**
- Block SYNTHESIZING
- Log as failure with lesson
- Force ITERATING or REFRAMING

### 3. Critical Assumption Audit (NEW - Critical)

**Question:** What assumptions would invalidate everything?

For each finding, list assumptions:
```json
{
  "id": "find_001",
  "attributes": {
    "statement": "X causes Y",
    "critical_assumptions": [
      {
        "assumption": "Discharge represents local water availability",
        "validated": false,
        "validation_method": "Compare with precipitation",
        "if_invalid": "Entire finding collapses"
      },
      {
        "assumption": "No major confounders beyond those controlled",
        "validated": true,
        "validation_method": "Literature review"
      }
    ]
  }
}
```

**Audit questions:**
- What does this finding depend on?
- If assumption X fails, what survives?
- Has each critical assumption been validated or acknowledged?

### 4. Claim Validity

**Question:** Are claims calibrated to evidence?

Check:
- Strong evidence → strong claims ✓
- Moderate evidence → moderate claims ✓
- Weak evidence → strong claims ✗ (overclaiming)
- No evidence → any claim ✗ (fabrication)

Red flags:
- "We demonstrate..." without strong evidence
- "X causes Y" without mechanism
- "Statistically significant" but method was ad-hoc threshold

### 5. Evidence Chain Completeness

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
- Method with no implementation file

### 6. Hypothesis Coverage

**Question:** Were all hypotheses tested?

Check:
- Each hypothesis has experiment?
- Results interpreted for each?
- Inconclusive hypotheses acknowledged?

Red flags:
- Hypothesis mentioned but never tested
- Results not mapped to hypotheses
- Selective reporting (only successful tests)

### 7. Objective Completion (NEW - Critical)

**Question:** Did we address all stated objectives?

```
Original goal: 4 objectives
Check:
  ✓ Objective 1: Completed
  ✓ Objective 2: Completed
  ⚠ Objective 3: Partially addressed
  ✗ Objective 4: Missing

Decision: Cannot proceed to COMPLETE if any objective unaddressed.
```

**What to do if missing:**
- Block COMPLETE
- Force ITERATING to address missing objectives
- Or: explicitly acknowledge as limitation with reason

### 8. Confounder Control

**Question:** Are confounders addressed?

For causal claims:
- Confounders identified?
- Control strategy documented?
- Unaddressed confounders acknowledged?

Red flags:
- Causal claim with no confounder analysis
- Ignoring obvious confounders
- Claiming causation from correlation

### 9. Limitation Acknowledgment

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

### 10. Literature Positioning

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

## Review Process by Phase

```
FORMULATION review:
  - Question specific? Falsifiable?
  - Hypotheses distinct and testable?
  - Scale context defined?

LITERATURE review:
  - Claim Graph built?
  - Contradictions/tensions noted? (not just gaps)
  - Position relative to debates clear?

METHOD review:
  - Methods match hypotheses?
  - Strategy evaluated (cost vs. information gain)?
  - Critical assumptions listed?
  - Data documented?
  - Units and variables understood?

EXECUTION review (CRITICAL):
  - Method fidelity: implemented == designed?
  - Physical sanity: values reasonable?
  - All hypotheses tested?
  - Figures validated?
  - Failures recorded?

VALIDATION review:
  - Sanity checks pass?
  - Evidence chains complete?
  - Assumptions still valid?

SYNTHESIZING review:
  - Claims calibrated to evidence?
  - Limitations acknowledged?
  - Findings connected to hypotheses?

WRITING review:
  - Method-claim consistency?
  - Figures embedded and accurate?
  - Citations correct?
  - Objectives all addressed?
```

## Review Object

```json
{
  "id": "rev_001",
  "type": "review",
  "state": "completed",
  "attributes": {
    "phase": "VALIDATING_RESULTS",
    "issues": [
      {
        "dimension": "method_fidelity",
        "severity": "critical",
        "finding": "meth_001",
        "issue": "Designed: Getis-Ord Gi*, Implemented: threshold",
        "recommendation": "Either implement Gi* or revise method description"
      },
      {
        "dimension": "physical_sanity",
        "severity": "critical",
        "finding": "find_001",
        "issue": "Water availability 1,969,235 mm/year > precipitation",
        "recommendation": "Discharge ≠ local availability. Reframe calculation."
      },
      {
        "dimension": "objective_completion",
        "severity": "major",
        "issue": "Objective 4 (Regional analysis) missing",
        "recommendation": "Either implement or explicitly acknowledge as limitation"
      }
    ],
    "passed": false,
    "blocked_transitions": ["SYNTHESIZING"],
    "must_fix": ["method fidelity", "physical sanity"],
    "timestamp": "2024-01-15T12:00:00"
  }
}
```

## Severity Levels

| Severity | Meaning | Action |
|----------|---------|--------|
| Critical | Fatal flaw, blocks progress | Must fix immediately |
| Major | Significant weakness | Must fix before COMPLETE |
| Minor | Small issue | Fix if time permits |
| Suggestion | Improvement idea | Optional |

**Critical severity triggers:**
- Method != implementation
- Physical values absurd
- Critical assumption invalidated
- Objective completely missing
- Evidence fabricated

## Review Triggers

**Mandatory reviews:**
- After VALIDATING_RESULTS (before SYNTHESIZING) — sanity check
- After WRITING (before COMPLETE) — final review
- After REFRAMING — verify new direction

**Automatic blocks:**
- Any critical issue → block transition
- Must fix or explicitly acknowledge

## Self-Review Mindset

Review as **hostile reviewer**:

- "What would make me reject this?"
- "What assumption would invalidate everything?"
- "Did they actually do what they claimed?"
- "Do these numbers make any sense?"

Then fix before reviewer sees it.

## Difference from Overclaim Detection

- **Overclaim detection**: claims vs evidence strength
- **Critical review**: methods vs implementation, physical sanity, assumptions

Both needed. This catches different problems.