# Uncertainty, Conflicts & Freshness

## Knowledge States

Self-relevant claims may be:

- `known`
- `unknown`
- `uncertain`
- `stale`
- `conflicted`
- `not_observed`

These states exist so Self Model can avoid false certainty.

## Reconciliation

`SelfStateReconciler.reconcile(field_name, candidates, expected_owner=None)` handles source values for one field.

### No evidence

Output:

```text
status = unknown
selected = None
refresh_requested = true
reason = no_evidence
```

### All evidence stale or expired

Output:

```text
status = stale
selected = None
refresh_requested = true
reason = all_evidence_stale_or_expired
```

### Conflicting live values

Output:

```text
status = conflicted
refresh_requested = true
reason includes conflicting_values
```

If exactly one expected-owner candidate exists, it may be surfaced as a candidate, but the overall status remains conflicted.

### Consistent live evidence

Highest-confidence live item is selected.

Status:

- `known` for fresh/recent/unknown freshness;
- `aging` for aging evidence.

## Freshness Ownership

Self Model does not derive freshness from timestamps.

Temporal Awareness or another explicit owner provides:

- observed time;
- age/duration metadata;
- freshness classification.

Self Model consumes those values.

## Unsupported Inference Rule

Self Model must not convert:

```text
missing evidence -> probably true
stale evidence   -> current fact
conflict         -> silent winner
request sent     -> action succeeded
```

## Refresh Requests

`refresh_requested=true` means evidence should be reacquired by the appropriate owner/integration layer.

It does not authorize Self Model to perform the refresh action itself.

## Merge Conflicts

`merge_states()` refuses to silently overwrite a field when different owners/values project incompatible content.

This produces an explicit error rather than hidden drift.

## Fail-Closed Summary

```text
No evidence   -> unknown
Old evidence  -> stale
Disagreement  -> conflicted
No proof      -> unverified
```

This is the expected Self Model behavior.
