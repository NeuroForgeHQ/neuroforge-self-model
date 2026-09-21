# Self-State Schema

## Core Evidence Record

The base source-tagged field is `SourceValue`.

```text
field
value
owner
source
observed_at
confidence
freshness
```

Constraints:

- `field`, `owner`, `source` are non-empty strings;
- confidence is between `0.0` and `1.0`;
- freshness is one of:
  - fresh
  - recent
  - aging
  - stale
  - expired
  - unknown

## Operational State

Authoritative mapping:

| Field | Owner |
| --- | --- |
| current_task | runtime |
| session | runtime |
| active_module | runtime |
| active_process | runtime |
| current_subtask | planner |
| execution_state | planner |

Missing fields are explicitly tracked by `OperationalProjection.missing_fields`.

## Capability Evidence

`CapabilityEvidence` fields:

```text
capability
state
owner
source
confidence
permission_requirement
blocker
resource_limit
observed_at
freshness
```

Capability state is evidence, not Self Model authority.

Recognized capability owners currently include Runtime, Tools, Voice, Vision, Desktop Context, Planner, Memory, World Model, Temporal Awareness, Attention, Goals & Drives, Autonomy and Self Recovery.

## Self-Relevant Knowledge

`KnowledgeClaim` supports bounded categories:

- current_task
- current_subtask
- active_goal
- current_focus
- required_tool
- current_screen_state
- last_action_result
- capability
- limitation
- blocker
- permission

Knowledge states:

- known
- unknown
- uncertain
- stale
- conflicted
- not_observed

Self Model is not a general-purpose knowledge base.

## Recent Action / Outcome

`ActionOutcome` fields:

```text
action_id
action
owner
source
result
verified
verified_by
observed_at
confidence
```

If `verified == false`, projected result is `unverified`.

Verified outcomes require `verified_by` provenance.

Recent action projection is bounded; default projector capacity is 8 items.

## Integrated Self State

`IntegratedSelfState` exposes:

```text
fields       -> Mapping[str, SourceValue]
context      -> bounded auxiliary context
source_trace -> tuple[str, ...]
```

The mapping is read-only at the consumer surface.

## Unknown, Stale and Conflict Representation

Do not encode missing evidence as a guessed value.

Use:

```text
unknown
stale
conflicted
not_observed
```

or explicit missing-field metadata depending on the projection type.

## Example

```text
field       : current_task
value       : Runtime acceptance
owner       : runtime
source      : runtime.current_task
observed_at : 2026-09-21T18:00:00+05:30
confidence  : 1.0
freshness   : fresh
```

The value is useful because its source and owner remain inspectable.
