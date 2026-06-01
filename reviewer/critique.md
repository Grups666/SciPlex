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
  - Design: "Use method X with parameters Y"
  - Implementation: Check actual code
  - Match? YES/NO

Red flags:
- Designed: statistical method → Implemented: ad-hoc threshold (downgrade)
- Designed: algorithmic classification → Implemented: manual rules (downgrade)
- Manuscript claims "rigorous method" but code uses simplified approach
- Output claims raw-data empirical analysis but implementation used documented
  statistics, simulated values, examples, or literature summaries
```

**Severity: CRITICAL if mismatch**

This is scientific dishonesty, not just limitation.

If raw data was promised but not acquired and processed, do not treat this as a
minor limitation. Either run the raw-data workflow, or downgrade the output
target and evidence mode to literature synthesis, documented-statistics
synthesis, scoping analysis, or protocol.

### 2. Physical Sanity (NEW - Critical)

**Question:** Do the numbers make physical sense?

Domain-specific checks:

**Principle:**
```
- Derived values within known physical bounds?
- Orders of magnitude reasonable?
- Ratios and proportions meaningful?
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
  "id": "find_XXX",
  "attributes": {
    "statement": "X causes Y",
    "critical_assumptions": [
      {
        "assumption": "Variable A represents underlying concept B",
        "validated": false,
        "validation_method": "Compare with established proxy",
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

### 4a. Result Consistency

**Question:** Does the manuscript say the same thing as the tables, figures,
and analysis outputs?

Check:
- Numeric coefficients, signs, sample sizes, dates, and units match the
  experiment outputs and figure/table files.
- Text does not describe a positive estimate as negative, a null result as
  significant, or a descriptive association as causal.
- Figure captions, result paragraphs, finding objects, and claim audits agree.
- If specifications disagree, the disagreement is stated explicitly rather than
  smoothed into a single narrative.

Red flags:
- A coefficient plot shows sign reversal while prose says all models agree
- A table reports a smaller or different sample than the methods imply
- A finding object preserves an outdated interpretation after results changed
- Review passes without checking output numbers against generated artifacts

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
- Data object only identifies a source but experiment claims processed results
- Event log lacks create/update/transition events for objects supporting a finding

### 5a. Workspace and Ledger Integrity

**Question:** Did the run obey the SciPlex workspace contract?

Run:

```bash
python scripts/sciplex_runtime.py --workspace <working-directory> validate-workspace
```

Check:
- No research artifact folders directly under `sciplex/`
- JSON files parse
- Objects in `state.json` have matching files and paths
- Object creation and transitions are covered by `events.json`
- `context.md` and `.sciplex` exist and were followed

Critical or major ledger issues block `COMPLETE`. They can be fixed by
repairing the ledger, regenerating invalid objects, or honestly downgrading the
run to a partial test.

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
- Search-result bibliography: many cited sources have no explicit relevance or
  inclusion rationale
- Weakly related background sources are used to inflate citation count instead
  of supporting the paper's actual claims

### 11. Manuscript Body Integrity

**Question:** Is the submitted paper body itself journal-grade?

For publication-style `paper` outputs:
- Count the body separately from references, appendices, claim audits, and
  reproducibility logs.
- Check that Introduction, literature/background, methods/data, results,
  discussion, and conclusion each have substantive section depth.
- Verify the section order is readable and numbering is coherent.
- Treat appendix-heavy word counts as a blocker when the main text is thin.

Red flags:
- A 7000-word Markdown file whose body is only a short report plus long
  appendices
- One-paragraph Introduction, Methods, Results, or Discussion sections
- Generic numbered robustness notes or repeated limitation paragraphs
- Appendices that contain prose padding rather than supplemental evidence,
  tables, code outputs, derivations, or reproducibility details

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
  "id": "rev_XXX",
  "type": "review",
  "state": "completed",
  "attributes": {
    "phase": "VALIDATING_RESULTS",
    "issues": [
      {
        "dimension": "method_fidelity",
        "severity": "critical",
        "finding": "meth_XXX",
        "issue": "Designed: method A, Implemented: method B",
        "recommendation": "Either implement method A or revise method description"
      },
      {
        "dimension": "physical_sanity",
        "severity": "critical",
        "finding": "find_XXX",
        "issue": "Derived value exceeds physical bounds",
        "recommendation": "Check conceptual model. Reframe calculation."
      },
      {
        "dimension": "objective_completion",
        "severity": "major",
        "issue": "Objective N not addressed",
        "recommendation": "Either implement or explicitly acknowledge as limitation"
      }
    ],
    "passed": false,
    "blocked_transitions": ["SYNTHESIZING"],
    "must_fix": ["method fidelity", "physical sanity"],
    "timestamp": "ISO-8601"
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
- Claimed raw-data analysis without raw data acquisition and processing
- Invalid JSON or broken state/event ledger supporting final claims

**Major severity triggers:**
- Output target standards not met without justification
- Output exceeds target range and should be compressed before finalization
- Literature coverage far below target for a publication-style paper
- Figures are illustrative but described as empirical results
- Final report or paper cites literature objects that remain only `identified`
- Workspace marked COMPLETE without a console/audit object
- Workspace marked COMPLETE without a problem object for the research tension/gap
- Workspace marked COMPLETE with untested hypotheses
- Workspace marked COMPLETE with unvalidated methods
- Final output exists without an indexed review object
- Final output state conflicts with workspace phase
- Workspace marked COMPLETE while orchestrator objects are not complete
- Final output object lacks a valid `file_path`
- Final output `file_path` is relative to the outer workspace instead of the `sciplex/` root
- Final paper lacks lineage metadata linking hypotheses, data/sources, and methods
- Final paper lacks a structured key-claim audit linking claims to evidence, strength, and limitations
- Final paper cites literature that is only marked `read` rather than `cited` or `validated`
- Final bibliography contains many sources with no clear in-text use
- Cited literature lacks stable identifiers and is not marked for verification
- Final output lacks source-role coverage appropriate to the output target
- Final output references findings without explicit evidence chains
- Completed experiment lacks evidence mode or data/source inputs
- Paper target lacks a section plan or section draft files
- Finalized figure remains marked as needing generation
- Finalized image file is a text placeholder or invalid image bytes
- Final output lists figure objects but does not embed or link the figure files
- Finalized figure/table lacks evidence sources or displayed-data metadata
- Object-like JSON files under `objects/` are not indexed in `state.json`
- Reference section does not match cited literature object metadata
- Final output review lacks mandatory dimensions or only records a pass/fail result
- Review or console claims validation passed while runtime validation has blocking issues
- Final console validator result or object counts are stale relative to `state.json`

## Review Triggers

**Mandatory reviews:**
- After VALIDATING_RESULTS (before SYNTHESIZING) — sanity check
- After WRITING (before COMPLETE) — final review
- After REFRAMING — verify new direction

Final-output reviews must be diagnostic, not ceremonial. For a final report or
paper, record judgments for these dimensions at minimum:

- `method_fidelity`
- `evidence_chain`
- `claim_validity`
- `source_coverage`
- `result_consistency`
- `output_standards`
- `limitations`
- `overclaim`

Each dimension should include enough detail for another agent to understand the
defect or why it passed. A bare `passed: true` is not a review.

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
