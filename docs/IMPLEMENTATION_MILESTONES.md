# Implementation Milestones

## Purpose

NeuroForge ko coherent, evidence-based operational self-state dena: current task, focus, goals, capabilities, limitations, knowledge state aur recent outcomes.

## Truthful Status

**0 / 11 milestones complete — 0% implementation.**

```text
[░░░░░░░░░░░░░░░░░░░░] 0%
```

README/documentation ko implementation completion nahi maana jayega. Milestone tabhi complete hoga jab required code, tests aur evidence available hon.

## Rules

- `[x]` sirf verified implementation + tests/evidence ke baad.
- Mock-only integration ko real integration PASS nahi maana jayega.
- M10 ke liye real Windows/PC evidence required hai.
- CPU-first, local-first aur bounded-resource direction maintain rahegi.
- Missing evidence ko PASS claim nahi kiya jayega.

## Milestones

### [ ] M0 — Self-State Contracts & Foundation

**Scope:** SelfState schema, state IDs, provenance, confidence, timestamps aur update contracts.

**Deliverables:** Core models, validators, snapshot API, unit tests.

**Acceptance gate:** Invalid state reject ho; every critical field inspectable aur source-tagged ho.

### [ ] M1 — Current Task & Session State

**Scope:** Current task, subtask, session, active module/process aur task lifecycle.

**Deliverables:** Task/session state engine, transitions, bounded history, tests.

**Acceptance gate:** Start/pause/block/complete transitions deterministic aur evidence-based hon.

### [ ] M2 — Capability & Limitation Model

**Scope:** Available capabilities, unavailable capabilities, permissions, blockers aur resource limitations.

**Deliverables:** Capability registry, limitation model, source adapters, tests.

**Acceptance gate:** Unsupported capability available claim na ho; unknown state explicit rahe.

### [ ] M3 — Knowledge State & Uncertainty

**Scope:** known/unknown/uncertain/stale/conflicted/not_observed states.

**Deliverables:** Knowledge-state model, confidence rules, uncertainty queries, tests.

**Acceptance gate:** Missing ya stale evidence ko known fact ke roop me expose na kiya jaye.

### [ ] M4 — Recent Actions & Verified Outcomes

**Scope:** Recent actions, attempt state, verified result, failure/success outcome.

**Deliverables:** Bounded action history, result model, verification hooks, tests.

**Acceptance gate:** Action request ko success na maana jaye jab tak verified result na mile.

### [ ] M5 — Conflict Detection & Freshness

**Scope:** Conflicting module state, stale self-state detection, resolution requests.

**Deliverables:** Conflict engine, freshness guards, resolution status, tests.

**Acceptance gate:** Conflicting sources silently merge na hon; stale state explicitly marked ho.

### [ ] M6 — Runtime + Temporal Awareness Integration

**Scope:** Runtime se live task/session state aur Temporal Awareness se age/freshness/duration.

**Deliverables:** Adapters, event hooks, integration tests.

**Acceptance gate:** Self Model duplicate runtime/temporal owner logic na banaye.

### [ ] M7 — Goals & Drives + Attention Integration

**Scope:** Active goals, blockers, current focus aur focus reason.

**Deliverables:** Goal/attention adapters, self-state projection, integration tests.

**Acceptance gate:** Current goal aur current focus independently traceable hon.

### [ ] M8 — World Model + Memory Integration

**Scope:** Environment relation aur selected historical self-state context.

**Deliverables:** World/Memory adapters, retention boundary, integration tests.

**Acceptance gate:** Full live self-state blindly long-term Memory me persist na ho.

### [ ] M9 — Planner + Autonomy Integration

**Scope:** Planner ko capability/limitation context aur Autonomy ko current operational state.

**Deliverables:** Planner/Autonomy adapters, policy guards, end-to-end tests.

**Acceptance gate:** Self Model action authorization na de; sirf state provide kare.

### [ ] M10 — Real-PC Continuous Self-Model Acceptance

**Scope:** Real Windows session me task/focus/capability/limitation/action-result state continuously maintain karna.

**Deliverables:** Acceptance harness, long-session evidence, CPU/memory measurements, failure scenarios.

**Acceptance gate:** Real PC par coherent, fresh, bounded aur low-overhead self-state; contradictions/stale states fail closed.

## Final Completion Gate

Repo tab implementation-complete maana jayega jab **M0–M10 sab verified**, regressions PASS, integrations evidence-backed aur M10 real-PC acceptance PASS ho.
