# Self Model Architecture

## Purpose

`neuroforge-self-model` NeuroForge ka **projection, reconciliation aur exposure layer** hai. Iska kaam owner repositories se self-relevant evidence lena aur ek bounded, source-traceable operational self-state expose karna hai.

Self Model ka central question:

> **Main abhi kis operational state me hoon?**

## Architectural Position

```text
Runtime / Planner / Goals / Attention / World Model / Memory / Tools
                              |
                              v
                        Self Model
               project + reconcile + trace
                              |
                              v
              Planner / Autonomy / Conversation
```

Self Model authoritative owner repositories ko replace nahi karta.

## Core Responsibilities

Self Model:

- current task/session/module/process project karta hai;
- current subtask aur execution state reflect karta hai;
- capability/limitation evidence expose karta hai;
- self-relevant known/unknown/uncertain state represent karta hai;
- recent action/outcome ko bounded form me project karta hai;
- conflicting/stale evidence ko fail-closed form me surface karta hai;
- provenance, confidence aur freshness preserve karta hai;
- downstream consumers ko read-only views deta hai.

## Main Implementation Layers

### Core projection layer

`self_model/core.py`

Contains:

- `SourceValue`
- `OperationalStateProjector`
- `CapabilityEvidence` / `CapabilityProjector`
- `KnowledgeClaim` / `KnowledgeProjector`
- `ActionOutcome` / `ActionOutcomeProjector`
- `SelfStateReconciler`

### Integration layer

`self_model/integration.py`

Contains:

- `IntegratedSelfState`
- `RuntimeTemporalIntegrator`
- `GoalsAttentionIntegrator`
- `WorldMemoryIntegrator`
- `merge_states`
- `ConsumerViews`

### Acceptance layer

`self_model/acceptance.py`

Contains the real-PC acceptance harness. Harness existence does not mean real-PC acceptance has passed.

## Data Flow

1. Owner repository produces state/evidence.
2. Self Model receives only self-relevant fields.
3. Evidence keeps owner/source/confidence/freshness metadata.
4. Projection layer converts evidence into bounded self-state.
5. Reconciliation detects missing, stale or conflicting evidence.
6. Integration layer combines compatible projections.
7. Consumer layer exposes read-only views.

## Read-Only Rule

Self Model must not mutate:

- Runtime task lifecycle;
- Planner lifecycle;
- Goals & Drives priorities;
- Attention focus selection;
- World Model environment state;
- Memory history;
- tool permissions;
- Autonomy decisions.

## Failure Philosophy

When evidence is missing, stale or contradictory, Self Model must prefer:

```text
unknown / stale / conflicted / refresh_required
```

over fabricated certainty.

## Non-Goals

Self Model is not:

- consciousness;
- an emotion system;
- a planner;
- a memory database;
- a world simulator;
- a capability authority;
- a permission system;
- an action executor;
- an autonomous decision maker.

## Current Reality

M1-M9 code paths exist and have local validation according to repository status documentation. Real cross-repository continuous wiring and M10 real-Windows acceptance remain separate work.

This architecture deliberately keeps Self Model small: **project, reconcile, trace, expose.**
