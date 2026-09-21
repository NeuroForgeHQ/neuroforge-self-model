# Projection Semantics

## Definition

Projection means:

> take owner-provided evidence and expose only the bounded self-relevant part without taking ownership of the source subsystem.

## M1 — Operational Projection

`OperationalStateProjector.project()` consumes Runtime and Planner mappings.

Runtime-owned fields:

- current_task
- session
- active_module
- active_process

Planner-owned fields:

- current_subtask
- execution_state

Missing values are listed rather than guessed.

## M2 — Capability Projection

`CapabilityProjector.project()` groups `CapabilityEvidence` by capability.

`state_of(capability)`:

- returns `unknown` when no evidence exists;
- returns the common state when all evidence agrees;
- returns `conflicted` when evidence states disagree.

Self Model does not implement the capability itself.

## M3 — Knowledge Projection

`KnowledgeProjector` accepts only predefined self-relevant categories.

For the same key:

- higher-confidence evidence can replace lower-confidence evidence;
- contradictory equal/lower-priority evidence produces a conflicted claim;
- conflict value becomes `None`;
- conflict provenance is retained.

This projection must not expand into a general knowledge store.

## M4 — Recent Action / Outcome Projection

`ActionOutcomeProjector` keeps only the most recent bounded sequence.

Default maximum:

```text
8 outcomes
```

Rules:

- input order comes from the owner;
- Self Model does not execute actions;
- Self Model does not create a historical event store;
- unverified outcomes project as `unverified`.

## Read-Only Semantics

Projection never grants permission to mutate the owner.

Examples:

```text
project current_task != change current_task
project capability  != implement capability
project goal        != prioritize goal
project result      != verify result
```

## Projection Quality

A good projection is:

- bounded;
- owner-tagged;
- source-tagged;
- confidence-aware;
- freshness-aware;
- explicit about missing evidence;
- free from unsupported inference.

## Example

Owner evidence:

```text
runtime.current_task = "voice acceptance"
runtime.freshness    = "fresh"
```

Projection:

```text
field     = current_task
value     = voice acceptance
owner     = runtime
source    = runtime.current_task
freshness = fresh
```

No new task state is invented by Self Model.
