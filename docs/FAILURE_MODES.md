# Failure Modes

## Design goal
Self Model should fail explicitly and conservatively instead of inventing a coherent story from bad evidence.

## Missing owner evidence
No candidate evidence becomes unknown with no selected value and refresh requested. Self Model must not guess the value.

## Stale or expired evidence
If all evidence is stale or expired, status remains stale, no current value is selected, and refresh is requested.

## Conflicting evidence
If live values disagree, status becomes conflicted and refresh is requested. An expected-owner candidate may remain visible for traceability, but conflict remains explicit.

## Unsupported capability owner
CapabilityEvidence rejects unrecognized capability owners, preventing Self Model from silently becoming its own capability authority.

## General-knowledge drift
KnowledgeClaim accepts only bounded self-relevant categories. General knowledge belongs elsewhere.

## Malformed input
Core validation rejects:
- blank required text fields;
- confidence outside 0.0-1.0;
- unsupported freshness states;
- unsupported knowledge states;
- verified action result without verifier provenance;
- invalid projection sizes or acceptance thresholds.

## Unverified action outcome
If verified is false, projected result remains unverified even when a source reports a success string.

## Merge conflict
merge_states refuses incompatible values/owners for the same field instead of silently overwriting them.

## Missing source trace
Real-PC acceptance rejects snapshots with no source trace and fields with missing owner/source provenance.

## Resource-budget failure
M10 may fail if average CPU exceeds the configured limit, peak memory exceeds the configured limit, or session duration does not reach its configured minimum.

Threshold values are explicit inputs; this document does not invent universal performance limits.

## Wrong environment
M10 fails if evidence is not from Windows or real owner sources are absent. Unit tests and CI are not substitutes.

## Recovery boundary
A refresh request describes state. It does not authorize Self Model to restart owners, rerun tools, grant permissions, change goals, or execute recovery actions.

## Fail-closed summary

~~~text
missing       -> unknown
stale         -> stale
contradictory -> conflicted
unverified    -> unverified
malformed     -> validation error
wrong M10 env -> acceptance fail
~~~
