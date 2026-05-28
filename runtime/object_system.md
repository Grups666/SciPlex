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
| data | Datasets | identified, validated, processed |
| method | Analysis methods | designed, implemented, validated |
| experiment | Analysis runs | running, completed, failed |
| figure | Visualizations | draft, finalized |
| finding | Conclusions | draft, validated |
| failed | Failed attempts | recorded |
| paper | Manuscript | draft, reviewed, final |

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

```
sciplex/
├── state.json         # Object index
├── events.json        # Event log
└── objects/
    ├── orchestrator/
    │   └── orch_001.json
    ├── literature/
    │   ├── lit_001.json
    │   └── lit_001.pdf
    ├── data/
    │   ├── data_001.json
    │   └── data_001.csv
    ├── method/
    │   ├── meth_001.json
    │   └── meth_001.py
    ├── experiment/
    │   └── exp_001/
    │       ├── exp_001.json
    │       └── outputs/
    ├── figure/
    │   ├── fig_001.json
    │   └── fig_001.png
    ├── finding/
    │   └── find_001.json
    ├── failed/
    │   └── fail_001.json
    └── paper/
        ├── paper_001.json
        └── paper_001.md
```

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
experiment.method_id → method
experiment.data_id → data
figure.experiment_id → experiment
finding.experiment_ids → [experiment, ...]
paper.figure_ids → [figure, ...]
```

Relationships enable traversal:
- From finding, find all supporting experiments
- From experiment, find method and data
- From method, find all experiments that used it
