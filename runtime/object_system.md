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
| orchestrator | Research question, progress | formulating, designing, executing, synthesizing, writing, complete |
| hypothesis | Testable predictions | formulated, tested, supported, refuted, inconclusive |
| problem | Identified research problems | identified, resolved |
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
| review | Quality review records | completed |

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
├── config/            # Project-level SciPlex configuration
│   ├── .env.local     # Optional private overrides (never commit)
│   ├── config.yaml    # Optional non-secret project settings
│   └── resolved.json  # Optional redacted resolved config snapshot
├── state.json         # Object index
├── events.json        # Event log
└── objects/           # All research content here
    ├── orchestrator/  # Research question, progress tracking
    ├── hypothesis/    # Hypotheses (can also be in orchestrator/)
    ├── problem/       # Identified problems
    ├── literature/    # Papers, notes
    ├── data/          # Datasets
    ├── method/        # Methods + analysis scripts
    ├── strategy/      # Method evaluation
    ├── experiment/    # Analysis outputs
    ├── figure/        # Visualizations
    ├── finding/       # Conclusions
    ├── failed/        # Failures + lessons
    ├── paper/         # Manuscript
    └── console/       # Trajectory visualization
```

Hypotheses can be stored in `orchestrator/` or `hypothesis/`. All other types have dedicated directories.

`config/` is not an object directory. It contains project-level settings that
control provider selection, model profiles, timeouts, output preferences, and
other runtime options for this research workspace.

Configuration precedence is:

1. `sciplex/config/.env.local`
2. `sciplex/config/config.yaml`
3. skill-level `config/.env.local`
4. skill-level `config/config.yaml`
5. driver agent environment
6. built-in defaults

Project-level config should override skill-level defaults. Skill-level config
should provide reusable user or machine defaults. Driver-level fallback should
only be used when SciPlex config is silent. Secrets must not be copied into
objects, events, manuscripts, or console data; `resolved.json`, if written,
should record only redacted values and provider status.

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

## Runtime Helper

Use `scripts/sciplex_runtime.py` for deterministic bookkeeping:

```bash
python scripts/sciplex_runtime.py --workspace <working-directory> init
python scripts/sciplex_runtime.py --workspace <working-directory> create-object \
  --type literature \
  --state identified \
  --attributes path/to/literature_attributes.json \
  --reason "Paper identified during OpenAlex search"
python scripts/sciplex_runtime.py --workspace <working-directory> transition-object \
  --id lit_001 \
  --state read \
  --reason "Key claims extracted"
```

The helper handles IDs, object files, `state.json`, and `events.json`. It does
not decide scientific validity, evidence strength, method choice, or whether a
transition is epistemically justified. Those decisions remain with the agent.

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
