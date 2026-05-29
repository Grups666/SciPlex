# Object System

## Object Philosophy

Objects are research memory. They persist across sessions, enable traceability, support reasoning.

Every meaningful research artifact is an object with:
- Identity (unique ID)
- Type (what kind of thing)
- State (where in lifecycle)
- Attributes (specific properties)

## Object Types

| Type | Purpose | States |
|------|---------|--------|
| orchestrator | Research question, hypotheses, progress | formulating, designing, executing, synthesizing, writing, complete |
| literature | Papers, notes, claim positions | identified, read, cited |
| problem | Identified research problems | identified, resolved |
| data | Datasets | identified, validated, processed |
| method | Analysis methods | designed, implemented, validated |
| strategy | Method evaluation, budget allocation | evaluated, active |
| experiment | Analysis runs | running, completed, failed |
| figure | Visualizations | draft, finalized |
| finding | Conclusions | draft, validated |
| failed | Failed attempts | recorded |
| paper | Manuscript | draft, reviewed, final |
| console | Research trajectory visualization | active |

## Object Structure

Every object has JSON definition:

```json
{
  "id": "meth_001",
  "type": "method",
  "state": "implemented",
  "attributes": {
    "name": "Method name",
    "...": "Type-specific attributes"
  }
}
```

Physical files in same directory:
- `objects/method/meth_001.json` — definition
- `objects/method/meth_001.py` — implementation

## Object Directory

**CRITICAL: Only `objects/` directory at top level. No `scripts/`, `data/`, `figures/`, etc.**

```
sciplex/
├── state.json         # Object index
├── events.json        # Event log
└── objects/           # ALL content goes here
    ├── orchestrator/
    │   └── orch_XXX.json
    ├── literature/
    │   ├── lit_XXX.json
    │   └── notes or pdfs if available
    ├── problem/
    │   └── prob_XXX.json
    ├── data/
    │   ├── data_XXX.json
    │   └── data files (.csv, .parquet, etc.)
    ├── method/
    │   ├── meth_XXX.json
    │   └ meth_XXX.py (implementation script if needed)
    ├── strategy/
    │   └── strat_XXX.json
    ├── experiment/
    │   └── exp_XXX/
    │       ├── exp_XXX.json
    │       └── outputs/
    ├── figure/
    │   ├── fig_XXX.json
    │   └── fig_XXX.png
    ├── finding/
    │   └── find_XXX.json
    ├── failed/
    │   └── fail_XXX.json
    ├── paper/
    │   ├── paper_XXX.json
    │   └── paper_XXX.md
    └── console/
        ├── console_data.json  # visualization data
        └── index.html         # interactive console
```

**Common violations to avoid:**
- Creating `scripts/` at sciplex root → scripts go in `objects/method/`
- Creating `data/` at sciplex root → goes in `objects/data/`
- Creating `figures/` at sciplex root → goes in `objects/figure/`
- Creating `manuscript/` at sciplex root → goes in `objects/paper/`

## State Index

`state.json` tracks all objects:

```json
{
  "objects": {
    "orch_001": {"type": "orchestrator", "state": "executing"},
    "meth_001": {"type": "method", "state": "implemented"},
    "exp_001": {"type": "experiment", "state": "completed"}
  },
  "counts": {
    "literature": 5,
    "data": 2,
    "method": 3,
    "experiment": 4,
    "figure": 6,
    "finding": 2,
    "failed": 1
  },
  "last_updated": "2024-01-15T10:30:00"
}
```

## Object Lifecycle

Objects transition through states:

```
orchestrator: formulating → designing → executing → synthesizing → writing → complete
method: designed → implemented → validated
experiment: running → completed | failed
figure: draft → finalized
paper: draft → reviewed → final
```

Invalid transitions are rejected. All transitions logged as events.

## Object Relationships

Objects reference each other:

```
problem.source_papers → [literature, ...]
problem.hypotheses_generated → [hypothesis, ...]
experiment.method_id → method
experiment.data_id → data
experiment.strategy_id → strategy
figure.experiment_id → experiment
finding.experiment_ids → [experiment, ...]
paper.figure_ids → [figure, ...]
console.all_objects → reference to all
```

Relationships enable traversal:
- From finding, find all supporting experiments
- From experiment, find method and data
- From method, find all experiments that used it
- From problem, find hypotheses and source papers
- From console, navigate entire research trajectory
