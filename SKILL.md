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

Layer 3 — Strategy & Discovery (strategy/)
  What to try: method selection, problem discovery, resource allocation

Layer 4 — Runtime Infrastructure (runtime/)
  How to execute: objects, events, state machine

Layer 5 — Quality Assurance (reviewer/)
  How to validate: critique, overclaim detection, causal validity

Layer 6 — Transparency (console/)
  How to see: visualization, trajectory audit
```

Load modules on demand. Don't load everything at once.

---

## Research State Machine

Research is a **graph with cycles**, not a linear pipeline.

```
IDLE → FORMULATING → REVIEWING_LITERATURE → DESIGNING_METHODS
         ↓                    ↓                    ↓
      REFRAMING ←──────────────────────────────────┘
         ↓
      (can return to ANY state)
      
DESIGNING_METHODS → PREPARING_DATA → RUNNING_EXPERIMENTS → VALIDATING_RESULTS
                                              ↓                    ↓
                                           ITERATING ←────────────┘
                                              ↓
                                          REFRAMING (if fundamental issue)

VALIDATING_RESULTS → SYNTHESIZING → WRITING → REVIEWING → COMPLETE
```

**REFRAMING state:** When question assumptions fail, method fundamentally mismatched design, or physical values absurd.

**Transition guards:** Sanity checks at each transition prevent proceeding with invalid results.

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

### Strategy & Discovery Modules

| Purpose | Module |
|---------|--------|
| Method selection | `strategy/strategy.md` |
| Problem discovery | `strategy/problem_discovery.md` |

### Runtime Modules

| Purpose | Module |
|---------|--------|
| Object system | `runtime/object_system.md` |
| Event system | `runtime/event_system.md` |
| State machine | `runtime/state_machine.md` |
| Failure memory | `runtime/failure_memory.md` |

### Quality Modules

| Purpose | Module |
|---------|--------|
| Evidence standards | `core/evidence.md` |
| Causal validity | `reviewer/causal_validity.md` |
| Overclaim detection | `reviewer/overclaim.md` |
| Critical review | `reviewer/critique.md` |

### Transparency Modules

| Purpose | Module |
|---------|--------|
| Research console | `console/console_design.md` |

---

## Execution Protocol

### 1. Initialize

Load `runtime/object_system.md` for workspace structure.

Create workspace at `<current_working_directory>/sciplex/`:

```
sciplex/
├── state.json         # Object index
├── events.json        # Event log
└── objects/           # All research content
    ├── orchestrator/  # Question, hypotheses, progress
    ├── literature/    # Papers + notes
    ├── problem/       # Identified problems
    ├── data/          # Datasets
    ├── method/        # Methods + code
    ├── strategy/      # Method evaluation
    ├── experiment/    # Analysis outputs
    ├── figure/        # Visualizations
    ├── finding/       # Conclusions
    ├── failed/        # Failures + lessons
    ├── paper/         # Manuscript
    └── console/       # Trajectory visualization
```

All content goes in `objects/`. See `runtime/object_system.md` for structure.

### 2. Formulate

Load `workflow/formulation.md`, `core/epistemology.md`, and `strategy/problem_discovery.md`.

Generate:
- Question object (orchestrator)
- Hypothesis objects
- Literature objects (from search)
- Problem objects (from contradiction/tension finding)

**Quality Gate:** Question specific? Hypotheses falsifiable? Problem identified (not just gap)?

### 3. Design

Load `workflow/methods.md` and `strategy/strategy.md`.

Generate:
- Method objects
- Data objects
- Strategy objects (method evaluation, budget allocation)

**Quality Gate:** Methods match hypotheses? Data documented? Strategy evaluated? Confounders identified?

### 4. Execute

Load `workflow/execution.md`, `runtime/failure_memory.md`.

**Pre-execution checks:**
- Load method object, extract design intent
- Query failure memory for similar approaches
- Create implementation checklist

**Execution checkpoints:**
- Unit understanding (check before calculation)
- Method fidelity (implementation == design?)
- Physical sanity (values reasonable?)

Use `scripts/execute_analysis.py` for reproducible runs.

Generate:
- Experiment objects
- Figure objects
- Failure objects (with lessons)

**Quality Gate:**
- All hypotheses tested
- Method fidelity check passed
- Physical sanity check passed
- Objectives progress checked
- Failures recorded with lessons

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

Run critical checks:
- **Method fidelity:** implementation == design?
- **Physical sanity:** values reasonable?
- **Objective completion:** all objectives addressed?
- **Critical assumptions:** what would invalidate everything?
- Overclaim detection
- Causal validity check

**Quality Gate:**
- No critical issues (blocks COMPLETE)
- Method-claim consistency verified
- Objectives all addressed or acknowledged

### 8. Generate Console

Load `console/console_design.md`.

After each phase transition, update the research console:

```
Console components (auto-generated from research objects):
1. Research Timeline — state transitions with timestamps
2. Question Evolution — question changes and reframings
3. Hypothesis Tracker — status and evidence for each hypothesis
4. Experiment Trajectory — method design, execution, results
5. Evidence Accumulation — evidence strength per hypothesis
6. Assumption Audit — validated/invalidated assumptions
7. Claim Graph — position in literature debates
8. Failure Memory — failures and lessons learned
9. Objective Progress — completion status
10. State History — all transitions with guards

Output:
- objects/console/console_data.json
- objects/console/index.html (interactive visualization)
```

**Console provides audit trail for entire research trajectory.**

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
