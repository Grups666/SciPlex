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
| data | Datasets | identified, acquired, validated, processed |
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

Object `file_path` attributes are relative to the `sciplex/` root. For example,
use `objects/paper/brief_001.md`, not `sciplex/objects/paper/brief_001.md`.

## Object Directory

```
sciplex/
├── .sciplex           # Workspace contract and path rules
├── context.md         # Brief context reloaded before file operations
├── config/            # Project-level SciPlex configuration
│   ├── .env.local     # Optional private overrides (never commit)
│   ├── config.yaml    # Optional non-secret project settings
│   └── resolved.json  # Optional redacted resolved config snapshot
├── state.json         # Object index
├── events.json        # Event log
└── objects/           # All research artifacts here
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

No research artifact directory should be created directly under `sciplex/`.
Allowed root entries are `.sciplex`, `context.md`, `config/`, `state.json`,
`events.json`, and `objects/`. Dataset manifests, raw-data pointers, downloads,
intermediate files, scripts, reports, figures, and console files belong under
the relevant `objects/<type>/` directory.

For acquired public datasets, prefer:

```
objects/data/data_001.json        # data object
objects/data/data_001/manifest.json
objects/data/data_001/raw/<downloaded files>
objects/data/data_001/processed/<derived files>
```

Data objects should distinguish `identified` (known source), `acquired`
(artifact downloaded with manifest/checksum), `validated` (schema/quality
checked), and `processed` (analysis-ready derivatives exist). A landing page,
API description, or dataset documentation record is not acquired raw data.

Before creating, reading, or updating files, load `.sciplex` and `context.md`
from the workspace. These files define the local path contract and any
project-level output target or evidence-mode constraints.

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
python scripts/sciplex_runtime.py --workspace <working-directory> remove-object \
  --id exp_bad \
  --reason "Incorrect object id prefix; retained file for audit and recreated with runtime id"
python scripts/sciplex_runtime.py --workspace <working-directory> artifact-path \
  --type data \
  --filename data_001.json
python scripts/sciplex_runtime.py --workspace <working-directory> validate-workspace
```

The helper handles IDs, object files, `state.json`, and `events.json`. It does
not decide scientific validity, evidence strength, method choice, or whether a
transition is epistemically justified. Those decisions remain with the agent.

Prefer runtime-assigned IDs. If you provide an explicit `--id`, it must use the
type prefix defined by the object system, such as `exp_001` for experiments and
`fig_001` for figures. Invalid IDs should be removed from the state index with
`remove-object` and recreated correctly; do not silently leave inconsistent
objects in active state.

`validate-workspace` checks the workspace contract, root-level path mistakes,
JSON parseability, required object directories, and whether object creation is
covered by events. It also checks basic output-target standards for final
papers/reports, whether cited literature has advanced beyond `identified`, and
whether final outputs have corresponding review and console/audit objects. It
also flags object-like JSON files under `objects/` that are not indexed in
`state.json`; scratch files and repair notes belong outside active object
directories unless they are real objects. For publication-style outputs, it
checks that the reference section is consistent with cited literature object
metadata and that final reviews cover the required critique dimensions.
Critical or major issues block `COMPLETE` unless the study scope is explicitly
downgraded and recorded.

Use `validate-workspace --require-complete` for final acceptance tests. Plain
`validate-workspace` is allowed for in-progress audits and may pass while a
paper is still draft or the workspace is still in `WRITING`.
Completion-required validation expects the research graph to be closed: a
problem/tension object exists, hypotheses are assessed beyond `formulated`,
methods are validated, cited literature is marked `cited` or `validated`, and
the final output records lineage to hypotheses, data/sources, methods,
findings, figures, and citations.
Publication-style outputs should also include a key-claim audit that maps core
claims to evidence links, evidence strength, and limitations.
It also expects the final console/audit summary to be current: object counts,
validator status, and final output metadata should match `state.json` and the
actual output files.

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
