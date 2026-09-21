# Self Model API

## Public Exports

The package currently exports core projection types plus integration and acceptance helpers.

### Core

- `SourceValue`
- `OperationalProjection`
- `OperationalStateProjector`
- `CapabilityEvidence`
- `CapabilityProjection`
- `CapabilityProjector`
- `KnowledgeClaim`
- `KnowledgeProjection`
- `KnowledgeProjector`
- `ActionOutcome`
- `ActionOutcomeProjector`
- `ReconciliationOutcome`
- `SelfStateReconciler`

### Integration

- `IntegratedSelfState`
- `RuntimeTemporalIntegrator`
- `GoalsAttentionIntegrator`
- `WorldMemoryIntegrator`
- `merge_states`
- `ConsumerViews`

### Acceptance

- `AcceptanceResult`
- `AcceptanceThresholds`
- `RealPCAcceptanceHarness`
- `RealPCEvidence`

## Basic Projection Example

```python
from self_model import OperationalStateProjector

projection = OperationalStateProjector().project(
    runtime_state={
        "current_task": "runtime acceptance",
        "session": "local-test",
        "freshness": "fresh",
    },
    planner_state={
        "current_subtask": "rerun failed tests",
    },
)

print(projection.snapshot())
```

## Reconciliation Example

```python
from self_model import SourceValue, SelfStateReconciler

item = SourceValue(
    field="current_task",
    value="runtime acceptance",
    owner="runtime",
    source="runtime.current_task",
    freshness="fresh",
)

result = SelfStateReconciler().reconcile(
    "current_task",
    [item],
    expected_owner="runtime",
)
```

## Consumer Views

`ConsumerViews.planner_view()` exposes:

- self_state
- capabilities
- source_trace

`ConsumerViews.autonomy_view()` exposes:

- self_state
- blockers
- limitations
- source_trace

## Read-Only Guarantee

API output is context, not authorization.

Self Model API must not produce decisions such as:

- authorized
- authorization
- permission_decision
- risk_decision
- may_execute
- execute
- action_decision

## Stability Note

Current API represents the repository's present implementation. Cross-repository transport/event mechanisms are not defined as completed by this document.
