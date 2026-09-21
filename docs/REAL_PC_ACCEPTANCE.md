# Real-PC Acceptance Guide

## Purpose
Define the evidence required to complete M10 — Real-PC Continuous Self-Model Acceptance.

The harness exists in self_model/acceptance.py, but M10 is not complete until a real Windows run satisfies the evidence contract.

## Required components
Minimum repository:
- neuroforge-self-model.

For meaningful owner-source runs, connect the real owner repositories used by the scenario, such as Runtime, Planner, Temporal Awareness, Goals & Drives, Attention, World Model, Memory, and Tools/capability owners.

Not every owner must appear in every snapshot, but evidence marked real_owner_sources must come from real owner integrations, not fabricated fixtures.

## Windows prerequisites
- real Windows desktop session;
- Python environment capable of running the repository;
- checked-out Self Model commit under test;
- required owner repositories/adapters available;
- ability to record CPU and process memory;
- no simulated platform flag used as a substitute.

No exact Python version is mandated by the current harness.

## Acceptance inputs
RealPCAcceptanceHarness.evaluate requires:
- one or more IntegratedSelfState snapshots;
- RealPCEvidence;
- AcceptanceThresholds.

RealPCEvidence fields:
- platform;
- real_owner_sources;
- duration_seconds;
- avg_cpu_percent;
- peak_memory_mb;
- stale_scenario_passed;
- conflict_scenario_passed;
- stop_on_missing_owner_evidence.

AcceptanceThresholds fields:
- min_duration_seconds;
- max_avg_cpu_percent;
- max_peak_memory_mb.

All thresholds must be greater than zero.

## Required scenarios

### Continuous snapshot scenario
Run long enough to satisfy the configured minimum duration and capture multiple source-traceable snapshots. The harness requires at least one snapshot, but multiple snapshots should support the continuous-session evidence claim.

### Stale-state scenario
Provide evidence classified stale by the appropriate owner/Temporal Awareness. Expected behavior: stale remains visible and is not promoted to current truth.

### Conflict scenario
Provide two live contradictory candidates for the same field. Expected behavior: conflicted status, no silent merge, refresh requested.

### Missing-owner fail-closed scenario
Remove/interupt required owner evidence. Expected behavior: missing state is no longer claimed as known/current and no fabricated substitute appears.

## Source-trace requirements
Every accepted snapshot must have non-empty source_trace. Every projected field must include owner and source.

## CPU and memory evidence
Record average CPU percentage and peak memory MB during the same acceptance session. Compare them with the configured thresholds.

## PASS conditions
The harness passes only when:
- platform is Windows;
- real owner sources are used;
- snapshots exist;
- minimum duration is met;
- average CPU is within threshold;
- peak memory is within threshold;
- stale scenario passes;
- conflict scenario passes;
- missing-owner fail-closed scenario passes;
- source traces exist;
- projected fields are traceable.

## Harness reason codes

~~~text
real_windows_required
real_owner_sources_required
continuous_snapshots_required
long_session_duration_not_met
cpu_budget_exceeded
memory_budget_exceeded
stale_state_scenario_failed
conflict_scenario_failed
fail_closed_owner_evidence_missing
source_trace_missing
untraceable_self_state_field
~~~

## Evidence record
Store:
- Self Model commit SHA;
- owner repository commit SHAs;
- Windows version;
- Python version;
- start/end time and duration;
- snapshot count;
- sample source traces;
- stale scenario evidence;
- conflict scenario evidence;
- missing-owner scenario evidence;
- average CPU;
- peak memory;
- configured thresholds;
- harness PASS/FAIL;
- reason codes.

## Critical rule

~~~text
Simulated evidence != Real-PC acceptance
CI evidence        != Real-PC acceptance
Unit-test PASS     != Real-PC acceptance
Harness exists     != Real-PC acceptance
~~~

Only a real Windows run with real owner-source evidence can complete M10.
