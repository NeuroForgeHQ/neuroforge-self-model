# Ownership Boundaries

## Rule

Self Model may **represent** owner state, but it must not silently become the owner of that state.

| State | Authoritative owner | Self Model role |
| --- | --- | --- |
| current task/session/module/process | Runtime | project |
| current subtask/execution state | Planner | project |
| freshness/duration | Temporal Awareness | consume metadata |
| goals/priorities/blockers | Goals & Drives | project |
| focus/focus reason | Attention | project |
| live environment | World Model | project self-relation |
| long-term history | Memory | bounded context only |
| capability evidence | Runtime/Tools/feature owner | aggregate/project |
| permissions/authorization | policy/tool/autonomy owner | never decide |
| action execution | Tools/Runtime | never execute |
| risk/action decision | Autonomy/policy owner | never decide |

## Self Model Owns

Self Model owns only the mechanics needed to construct a coherent self-view:

- projection formats;
- bounded aggregation;
- source/provenance preservation;
- conflict detection;
- missing-evidence representation;
- stale-evidence handling based on supplied freshness;
- read-only consumer views;
- boundary validation.

## Self Model Does Not Own

### Runtime

Self Model must not start, stop, resume or mark tasks complete.

### Planner

Self Model must not create plans or change planner lifecycle state.

### Temporal Awareness

Self Model must not calculate freshness or duration. It consumes owner-provided freshness classifications.

### Goals & Drives

Self Model must not create or prioritize goals.

### Attention

Self Model must not decide what should receive focus.

### World Model

Self Model must not maintain the full live environment model.

### Memory

Self Model must not become long-term action history or personal-history storage.

### Tools / Permissions

Self Model must not grant permissions or claim that an action may execute.

### Autonomy

Self Model may provide context to Autonomy, but may not output autonomous action decisions.

## Boundary-Safe Vocabulary

Preferred:

- "owner reports"
- "Self Model projects"
- "evidence indicates"
- "state is unknown"
- "refresh required"
- "consumer may use this context"

Avoid:

- "Self Model decided"
- "Self Model authorized"
- "Self Model executed"
- "Self Model knows because it inferred it without evidence"
- "Self Model owns the goal"

## Conflict Rule

If two owner-sourced candidates disagree, Self Model does not silently overwrite one. It exposes a conflict and may retain an expected-owner candidate only as traceable evidence, not as unquestioned truth.

## Duplication Test

Before adding logic, ask:

> Is this logic necessary to project/reconcile/expose self-state, or does another NeuroForge repository already own it?

If another repository owns it, Self Model should consume an interface rather than duplicate the subsystem.
