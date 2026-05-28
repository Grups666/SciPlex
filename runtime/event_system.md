# Event System

## Event Philosophy

Every action creates an event. Events are the audit trail of research.

Events enable:
- Traceability: Why was this decision made?
- Reproducibility: What sequence of actions led here?
- Debugging: Where did things go wrong?
- Learning: What patterns in research process?

## Event Structure

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "action": "create|update|validate|fail|iterate",
  "object_id": "meth_001",
  "object_type": "method",
  "state_before": "designed",
  "state_after": "implemented",
  "reason": "Implementation complete, ready for validation",
  "details": {
    "implementation_file": "meth_001.py",
    "lines_of_code": 45
  }
}
```

## Event Types

| Action | Meaning | When |
|--------|---------|------|
| create | New object created | First instantiation |
| update | Object modified | Attribute change |
| validate | Object validated | Quality check passed |
| fail | Attempt failed | Error or rejection |
| iterate | Iteration on object | Refinement cycle |
| transition | State changed | Lifecycle progression |

## Event Log

`events.json` contains all events:

```json
{
  "events": [
    {
      "timestamp": "2024-01-15T09:00:00",
      "action": "create",
      "object_id": "orch_001",
      "object_type": "orchestrator",
      "state_after": "formulating",
      "reason": "Research initiated"
    },
    {
      "timestamp": "2024-01-15T09:15:00",
      "action": "create",
      "object_id": "hyp_001",
      "object_type": "hypothesis",
      "reason": "First hypothesis generated"
    },
    {
      "timestamp": "2024-01-15T10:30:00",
      "action": "transition",
      "object_id": "orch_001",
      "state_before": "formulating",
      "state_after": "designing",
      "reason": "Hypotheses complete, proceeding to method design"
    }
  ]
}
```

## Event Queries

**Trace object history:**
```
events where object_id = "meth_001"
→ All events affecting this method
```

**Find decision points:**
```
events where action = "iterate"
→ All iterations and why
```

**Debug failure:**
```
events where action = "fail"
→ All failures and reasons
```

**Reconstruct timeline:**
```
events ordered by timestamp
→ Full research process
```

## State Transitions

Valid transitions are enforced:

```
orchestrator:
  formulating → designing (hypotheses complete)
  designing → executing (methods designed)
  executing → synthesizing (experiments complete)
  synthesizing → writing (findings validated)
  writing → complete (manuscript done)

method:
  designed → implemented (code written)
  implemented → validated (tests pass)

experiment:
  running → completed (success)
  running → failed (error)

figure:
  draft → finalized (validated)
```

Invalid transition example:
```
orchestrator: formulating → executing
→ ERROR: Must go through designing first
```

## Event-Driven Reasoning

Events support meta-reasoning:

**"Why did I iterate on this method 3 times?"**
→ Check events for method, find iteration reasons

**"What led to this finding?"**
→ Trace events backward from finding to experiments to methods

**"Where did I waste time?"**
→ Find events with long gaps, analyze what happened
