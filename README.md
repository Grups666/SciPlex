# SciPlex

A layered cognitive architecture for autonomous scientific research.

## Overview

SciPlex is a skill framework designed for coding agents to conduct complete scientific studies—from problem formulation to publication-quality manuscript. It provides structured thinking frameworks rather than step-by-step procedures, allowing the agent to make reasoned decisions at each phase.

## Architecture

The skill is organized as a layered cognitive stack:

```
Layer 1 — Scientific Philosophy (core/)
  Epistemology, evidence standards, identity

Layer 2 — Research Workflow (workflow/)
  Formulation → Methods → Execution → Synthesis → Writing

Layer 3 — Strategy & Discovery (strategy/)
  Method selection, problem discovery, resource allocation

Layer 4 — Runtime Infrastructure (runtime/)
  Object system, event tracking, state machine, failure memory

Layer 5 — Quality Assurance (reviewer/)
  Critique, overclaim detection, causal validity checks

Layer 6 — Transparency (console/)
  Research trajectory visualization, audit trail
```

## Key Features

**Scientific Philosophy Layer**
- Epistemological framework for evidence calibration (Strong/Moderate/Weak/None)
- Claim Graph methodology: literature as argument topology, not just background
- Causal reasoning requirements: mechanism, confounders, counterfactuals
- Scale awareness: explicit temporal/spatial/organizational scope for hypotheses

**Strategy & Discovery Layer**
- Problem discovery: find contradictions/tensions, not just gaps
- Method evaluation matrix: cost vs information gain vs risk
- Resource budgeting: experiments per hypothesis, reframing limits
- Exploration/exploitation balance

**Runtime Infrastructure**
- Explicit 11-state research state machine with REFRAMING support
- Transition guards: method fidelity, physical sanity, objective completion
- Object-centric process tracking with JSON definitions
- Event system for complete audit trail
- Failure memory to avoid repeating mistakes

**Quality Assurance**
- Method fidelity check: implementation == design (scientific honesty)
- Physical sanity check: values within reasonable bounds
- Critical assumption audit: what would invalidate everything
- Overclaim detection: automatic calibration of claims to evidence strength
- Causal validity checks: pattern ≠ explanation
- Objective completion check: all stated goals addressed

**Transparency Layer**
- Research console: 10 visualization components
- Question evolution tree, hypothesis tracker, experiment trajectory
- Evidence accumulation, assumption audit, failure memory
- Complete state history with transition guards

**Resource-Aware Planning**
- Iteration limits per hypothesis (max 3)
- Reframing budget (max 2)
- Total experiment budget (max 10)
- Convergence criteria: 2+ independent analyses

## Structure

```
sciplex/
├── SKILL.md              # Orchestrator and entry point
├── core/
│   ├── epistemology.md   # Scientific reasoning framework
│   ├── evidence.md       # Evidence calibration standards
│   └── identity.md       # Skill identity and principles
├── workflow/
│   ├── formulation.md    # Problem formulation phase
│   ├── methods.md        # Method design phase
│   ├── execution.md      # Execution and iteration
│   ├── synthesis.md      # Evidence synthesis
│   └── writing.md        # Manuscript production
├── strategy/
│   ├── strategy.md       # Method evaluation, resource allocation
│   └── problem_discovery.md # Contradiction/tension finding
├── runtime/
│   ├── object_system.md  # Object types and structure
│   ├── event_system.md   # Event tracking
│   ├── state_machine.md  # Research state transitions
│   └── failure_memory.md # Learning from failures
├── reviewer/
│   ├── critique.md       # Critical review dimensions
│   ├── overclaim.md      # Overclaim detection rules
│   └── causal_validity.md # Causal claim validation
├── console/
│   └── console_design.md # Research trajectory visualization
├── scripts/
│   └── execute_analysis.py # Deterministic execution
└── references/
    ├── literature_search.md   # Systematic review methods
    ├── method_templates.md    # Analysis pattern catalog
    ├── figure_guidelines.md   # Visualization best practices
    └── manuscript_template.md # Paper structure guide
```

## Workspace Structure

When invoked, SciPlex creates a workspace:

```
sciplex/
├── state.json         # Object index
├── events.json        # Event log
└── objects/           # All files here
    ├── orchestrator/  # Research question, hypotheses
    ├── literature/    # Papers + notes
    ├── data/          # Datasets
    ├── method/        # Methods + code
    ├── experiment/    # Runs + outputs
    ├── figure/        # Visualizations
    ├── finding/       # Conclusions
    ├── failed/        # Failed attempts
    └── paper/         # Manuscript
```

## Usage

```
/sciplex "<research goal>"
```

Example:
```
/sciplex "Investigate groundwater depletion patterns in North China Plain using GRACE data"
```

## Design Philosophy

**Framework over script:** The skill teaches how to think about research, not what to do step-by-step.

**LLM reasons, scripts execute:** Deterministic operations handled by scripts; reasoning and judgment by the agent.

**Honesty over appearance:** Negative results, limitations, and uncertainty are part of science.

**Traceability:** Every decision, state transition, and output is recorded.

## Requirements

This skill is designed for agents with:
- Strong logical reasoning capabilities
- Long-context handling (>50k tokens)
- Code execution abilities
- Web search for literature

Recommended models: Claude 3.5 Sonnet+, OpenAI o1, or similar high-capability reasoning models.

## Limitations

- Cannot access proprietary databases without credentials
- Cannot run experiments requiring physical equipment
- Results depend on data quality
- High token consumption for full research cycle

## Version

v0.2.5 - Complete object type definitions, event implementation clarification.

## License

MIT

## Author

Designed for autonomous scientific research workflows.