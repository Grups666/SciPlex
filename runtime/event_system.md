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
  "timestamp": "ISO-8601",
  "action": "create|update|validate|fail|iterate|transition",
  "object_id": "obj_XXX",
  "object_type": "method|experiment|finding|...",
  "state_before": "previous_state",
  "state_after": "new_state",
  "reason": "Why this action occurred",
  "details": {
    "relevant_attributes": "key information"
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
      "timestamp": "ISO-8601",
      "action": "create",
      "object_id": "orch_XXX",
      "object_type": "orchestrator",
      "state_after": "formulating",
      "reason": "Research initiated"
    },
    {
      "timestamp": "ISO-8601",
      "action": "create",
      "object_id": "hyp_XXX",
      "object_type": "hypothesis",
      "reason": "Hypothesis generated"
    },
    {
      "timestamp": "ISO-8601",
      "action": "transition",
      "object_id": "orch_XXX",
      "state_before": "formulating",
      "state_after": "designing",
      "reason": "Phase complete, proceeding to next"
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

Valid transitions are enforced by state machine. See `runtime/state_machine.md` for full specification.

Invalid transition example:
```
orchestrator: formulating → executing
→ ERROR: Must go through designing first
```

## Event-Driven Reasoning

Events support meta-reasoning:

**"Why did I iterate on this method?"**
→ Check events for method, find iteration reasons

**"What led to this finding?"**
→ Trace events backward from finding to experiments to methods

**"Where did I waste time?"**
→ Find events with long gaps, analyze what happened

## Implementation

Events are written to `events.json` on every state transition. Empty events file indicates execution did not follow state machine protocol.
