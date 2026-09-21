# Integration Contracts

## Contract Rule

Every integration is **projection-only**. Owner repositories stay authoritative.

## Runtime + Planner

Handled by `RuntimeTemporalIntegrator` through `OperationalStateProjector`.

Inputs may include:

Runtime:
- current_task
- session
- active_module
- active_process

Planner:
- current_subtask
- execution_state

Self Model may project these fields but may not modify lifecycle state.

## Temporal Awareness

Input is per-field temporal metadata.

Recognized metadata includes:

- age_seconds
- duration_seconds
- freshness
- observed_at

Self Model consumes this metadata. It must not independently calculate freshness/duration.

## Goals & Drives

Handled by `GoalsAttentionIntegrator`.

Owner fields:

```text
active_goal -> active_goal
blockers    -> goal_blockers
priority    -> goal_priority
```

Self Model must not create, rank or mutate goals.

## Attention

Owner fields:

```text
current_focus -> current_focus
focus_reason  -> focus_reason
```

Self Model must not choose the focus target.

## World Model

Handled by `WorldMemoryIntegrator`.

Current implemented projection:

```text
world_state.self_relation -> world_relation
```

World Model remains owner of live environment state.

## Memory

Self Model accepts a bounded sequence of selected memory items.

Projected memory fields are limited to:

- memory_id
- summary
- source
- relevance

Default maximum selected context: 5 items.

Memory remains owner of long-term history.

## Capability Owners / Tools

`CapabilityEvidence` may originate from recognized capability owners such as Runtime, Tools, Voice, Vision, Desktop Context and other feature repositories.

Self Model groups/exposes evidence only.

## Failure Behavior

For integrations:

- missing optional owner fields are omitted or marked missing;
- malformed core records raise validation errors;
- conflicting merged field projections are not silently overwritten;
- stale/expired evidence should be handled by reconciliation;
- unavailable owner data must not be replaced with fabricated values.

## Current Limitation

These contracts document the implemented adapter/interface behavior. They do **not** claim that every NeuroForge repository is already connected through a live continuous event stream.

Real cross-repository wiring is separate integration work.
