---
name: sciplex
description: Autonomous research agent. Conducts scientific studies from question to publication.
user-invocable: true
---

# SciPlex

A research operating system. Not a script—cognitive infrastructure for autonomous scientific inquiry.

## What It Does

Given a research goal, conducts complete scientific study and delivers publication-quality findings.

## When to Use

- User provides research proposal or scientific question
- User wants systematic investigation with proper methodology
- User needs rigorous evidence-based conclusions

## What It Delivers

- Tested hypotheses with calibrated evidence
- Publication-quality visualizations
- Complete manuscript with embedded figures and citations

---

## Architecture

This skill is a layered cognitive stack:

```
Layer 1 — Scientific Philosophy (core/)
  How to think: epistemology, evidence, identity
  
Layer 2 — Research Workflow (workflow/)
  How to work: formulation → execution → writing
  
Layer 3 — Runtime Infrastructure (runtime/)
  How to execute: objects, events, state machine
  
Layer 4 — Quality Assurance (reviewer/)
  How to validate: critique, overclaim detection, causal validity
```

Load modules on demand. Don't load everything at once.

---

## Research State Machine

Research is a state machine. Current phase determines valid actions.

```
IDLE → FORMULATING → REVIEWING_LITERATURE → DESIGNING_METHODS
  → PREPARING_DATA → RUNNING_EXPERIMENTS → VALIDATING_RESULTS
  → ITERATING | SYNTHESIZING → WRITING → REVIEWING → COMPLETE
```

**See:** `runtime/state_machine.md` for full specification.

---

## Quick Reference

### Phase Modules

| Phase | Module | Key Output |
|-------|--------|------------|
| Formulation | `workflow/formulation.md` | Question, hypotheses |
| Literature | `workflow/formulation.md` + `core/epistemology.md` | Claim Graph, gap |
| Methods | `workflow/methods.md` | Methods, data sources |
| Execution | `workflow/execution.md` | Results, figures |
| Synthesis | `workflow/synthesis.md` | Findings, evidence chains |
| Writing | `workflow/writing.md` | Manuscript |

### Quality Modules

| Purpose | Module |
|---------|--------|
| Evidence standards | `core/evidence.md` |
| Causal validity | `reviewer/causal_validity.md` |
| Overclaim detection | `reviewer/overclaim.md` |
| Critical review | `reviewer/critique.md` |

### Runtime Modules

| Purpose | Module |
|---------|--------|
| Object system | `runtime/object_system.md` |
| Event system | `runtime/event_system.md` |
| State machine | `runtime/state_machine.md` |
| Failure memory | `runtime/failure_memory.md` |

---

## Execution Protocol

### 1. Initialize

Load `runtime/object_system.md` for workspace structure.

Create workspace at `<current_working_directory>/sciplex/`:

```
sciplex/
├── state.json         # Object index
├── events.json        # Event log
└── objects/           # ALL files go here
    ├── orchestrator/  # Research question, hypotheses, progress
    ├── literature/    # Papers + notes
    ├── data/          # Datasets + definitions
    ├── method/        # Methods + implementation code
    ├── experiment/    # Analysis runs + outputs
    ├── figure/        # Visualizations
    ├── finding/       # Conclusions
    ├── failed/        # Failed attempts + lessons
    └── paper/         # Manuscript
```

**No top-level directories.** Everything goes under `objects/`.

### 2. Formulate

Load `workflow/formulation.md` and `core/epistemology.md`.

Generate:
- Question object (orchestrator)
- Hypothesis objects
- Literature objects (from search)

**Quality Gate:** Question specific? Hypotheses falsifiable? Gap identified?

### 3. Design

Load `workflow/methods.md`.

Generate:
- Method objects
- Data objects

**Quality Gate:** Methods match hypotheses? Data documented? Confounders identified?

### 4. Execute

Load `workflow/execution.md`, `runtime/failure_memory.md`.

Use `scripts/execute_analysis.py` for reproducible runs.

Generate:
- Experiment objects
- Figure objects

**Quality Gate:** All hypotheses tested? Figures validated? Failures recorded?

### 5. Synthesize

Load `workflow/synthesis.md`, `core/evidence.md`.

Generate:
- Finding objects
- Evidence chains

**Quality Gate:** Evidence chains complete? Claims calibrated? Limitations acknowledged?

### 6. Write

Load `workflow/writing.md`.

Generate:
- Paper object
- Manuscript file

**Quality Gate:** Full structure? Figures embedded? >3000 words?

### 7. Review

Load `reviewer/` modules.

Run:
- Overclaim detection
- Causal validity check
- Critical review

**Quality Gate:** No critical issues? No major overclaims? All causal claims valid?

---

## Commands

- `/sciplex "<goal>"` — Start research
- `/sciplex status` — Show progress (current phase, objects created)
- `/sciplex continue` — Resume from last state

---

## Scripts

| Script | Purpose |
|--------|---------|
| `execute_analysis.py` | Deterministic analysis execution |
| `validate_results.py` | Check result sanity |
| `format_paper.py` | LaTeX/markdown formatting |

Scripts handle determinism. You handle reasoning.

---

## References

| Reference | Content | When to Load |
|-----------|---------|--------------|
| `literature_search.md` | Systematic review methods | Phase 1 |
| `method_templates.md` | Common analysis patterns | Phase 2 |
| `figure_guidelines.md` | Visualization best practices | Phase 3 |
| `manuscript_template.md` | Paper structure | Phase 5 |

---

## Limitations

- Cannot access proprietary databases without credentials
- Cannot run experiments requiring physical equipment
- Cannot verify claims beyond available data
- Results depend on data quality

---

## API Keys

`config/.env.local`:
- SEMANTIC_SCHOLAR_API_KEY
- OPENALEX_EMAIL
- ZOTERO_API_KEY
