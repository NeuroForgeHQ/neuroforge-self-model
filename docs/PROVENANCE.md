# Provenance

## Principle

Every important self-state fact should answer:

> **Who owns this value, where did it come from, and how reliable/current is the evidence?**

## Required Provenance

For normal source values:

- `owner`
- `source`
- `confidence`
- optional `observed_at`
- `freshness`

For verified action results:

- action owner;
- action source;
- `verified=true`;
- non-empty `verified_by`.

## Owner vs Source

`owner` identifies the authoritative subsystem.

Example:

```text
owner  = runtime
source = runtime.current_task
```

`source` is more specific and should make tracing/debugging possible.

## Confidence

Confidence range:

```text
0.0 <= confidence <= 1.0
```

Confidence does not override ownership. A high-confidence non-owner source must not silently replace authoritative ownership rules.

## Freshness

Self Model stores/consumes freshness but does not calculate it.

Accepted values:

```text
fresh
recent
aging
stale
expired
unknown
```

Temporal Awareness remains the freshness/duration owner when temporal integration is used.

## Source Trace

Integrated projections accumulate `source_trace`.

Example:

```text
runtime.current_task
planner.current_subtask
temporal_awareness.current_task
goals_drives.active_goal
attention.current_focus
```

Duplicates are removed when states are merged.

## Conflict Provenance

For self-relevant knowledge conflicts, the implementation may produce a conflict source such as:

```text
conflict:source_a|source_b
```

The value becomes unavailable rather than inventing a reconciliation result.

## Missing Provenance

If there is no evidence:

- state should become unknown/missing;
- refresh may be requested;
- no source should be fabricated.

## Provenance Acceptance Rules

A projected fact is traceable when:

1. its owner is named;
2. its source is named;
3. confidence is valid;
4. freshness value is valid;
5. verified outcomes have verifier provenance;
6. consumer output preserves a source trace where relevant.

These rules make Self Model auditable instead of relying on opaque internal claims.
