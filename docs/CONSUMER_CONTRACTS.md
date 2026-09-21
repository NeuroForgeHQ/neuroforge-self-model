# Consumer Contracts

## Purpose

Self Model downstream systems ko **read-only operational context** deta hai.

Primary implemented consumers:

- Planner
- Autonomy

Conversation systems may later consume equivalent state, but this document only claims implemented consumer contracts.

## Planner Contract

`ConsumerViews.planner_view(state, capability_evidence=...)`

Returns:

```text
self_state
capabilities
source_trace
```

Planner may use this to understand:

- current operational state;
- capability availability evidence;
- source trace.

Planner remains responsible for planning.

## Autonomy Contract

`ConsumerViews.autonomy_view(state, blockers=..., limitations=...)`

Returns:

```text
self_state
blockers
limitations
source_trace
```

Autonomy may use this as decision context.

Self Model remains non-authoritative.

## Forbidden Outputs

Self Model must never claim ownership of:

```text
authorized
authorization
permission_decision
risk_decision
may_execute
execute
action_decision
```

These are explicitly guarded in the consumer implementation.

## Capability Exposure

Capability information means:

> owner-sourced evidence says the capability is in a particular state.

It does not mean:

> Self Model granted or implemented the capability.

## Blockers and Limitations

Blockers/limitations are context values.

They may explain why a task is blocked, but Self Model does not decide the recovery action.

## Source Trace Requirement

Consumers should preserve `source_trace` when the context is used for downstream reasoning, logging or debugging.

This allows later inspection of where the self-state came from.

## Read-Only Expectation

Consumers must treat returned state as input context and must not mutate it as if it were the authoritative owner store.

## Safe Interpretation

Correct:

```text
Self Model says runtime reports task X and capability Y is unavailable.
```

Incorrect:

```text
Self Model authorized action Z.
Self Model changed the active goal.
Self Model decided the risk is acceptable.
```

## Contract Summary

Self Model provides:

```text
state + evidence + provenance
```

Consumers provide:

```text
planning / policy / autonomous decision behavior
```

The boundary must remain explicit.
