# Implementation Milestones

## Purpose

NeuroForge ko coherent, evidence-based operational self-state dena: current task, focus, goals, capabilities, limitations, self-relevant knowledge state aur recent verified outcomes.

Self Model ka role **owner systems ki state ko duplicate karna nahi**, balki unki verified state ko ek bounded, inspectable aur internally consistent self-state projection me combine karna hai.

## Truthful Status

**0 / 11 milestones complete — 0% implementation.**

```text
[░░░░░░░░░░░░░░░░░░░░] 0%
```

README/documentation ko implementation completion nahi maana jayega. Milestone tabhi complete hoga jab required code, tests aur evidence available hon.

## Ownership Rules

Self Model:

- Runtime ka task/session lifecycle own nahi karega.
- Planner ka task decomposition, execution-state planning ya scheduling own nahi karega.
- Goals & Drives ke goals, priorities ya blockers own nahi karega.
- Attention ka focus-selection engine own nahi karega.
- Temporal Awareness ka freshness/duration engine own nahi karega.
- Memory ka long-term history own nahi karega.
- World Model ka environment state own nahi karega.
- Tools/Autonomy ka action execution, permission ya authorization own nahi karega.
- Owner modules ki verified state ko project, reconcile aur expose karega.

## Milestone Rules

- `[x]` sirf verified implementation + tests/evidence ke baad.
- Mock-only integration ko real integration PASS nahi maana jayega.
- M10 ke liye real Windows/PC evidence required hai.
- CPU-first, local-first aur bounded-resource direction maintain rahegi.
- Missing evidence ko PASS claim nahi kiya jayega.
- Self Model owner data ko silently rewrite ya fabricate nahi karega.

## Milestones

### [ ] M0 — Self-State Contracts & Projection Foundation

**Scope:** SelfState schema, field ownership metadata, provenance, confidence, timestamps, source references aur projection/update contracts.

**Deliverables:** Core models, validators, source-owner metadata, snapshot API, unit tests.

**Acceptance gate:** Invalid state reject ho; every critical field inspectable, source-tagged aur owner-traceable ho.

---

### [ ] M1 — Current Operational-State Projection

**Scope:** Runtime/Planner se current task, subtask, session, active module/process aur execution-state ko read-only/self-state projection ke roop me represent karna.

**Deliverables:** Runtime/Planner adapters, operational-state projector, bounded current snapshot, tests.

**Acceptance gate:** Self Model start/pause/block/complete task lifecycle independently own ya mutate na kare; owner state traceable rahe.

---

### [ ] M2 — Capability & Limitation Projection

**Scope:** Tools, Runtime aur relevant owner modules se evidence-backed capabilities, unavailable capabilities, permission requirements, blockers aur resource limitations ko self-state me represent karna.

**Deliverables:** Capability/limitation projection model, source adapters, evidence references, tests.

**Acceptance gate:** Self Model independent capability authority/registry na bane; unsupported capability available claim na ho; unknown state explicit rahe.

---

### [ ] M3 — Self-Relevant Knowledge State & Uncertainty

**Scope:** Sirf operationally self-relevant facts ke liye known/unknown/uncertain/stale/conflicted/not_observed state represent karna.

Examples:

- current task known hai ya nahi;
- required tool available hai ya nahi;
- current screen state fresh hai ya nahi;
- last action result verified hai ya nahi.

**Deliverables:** Self-knowledge projection model, confidence/provenance mapping, uncertainty queries, tests.

**Acceptance gate:** Self Model general knowledge base ya reasoning engine na bane; missing/stale evidence ko known fact ke roop me expose na kare.

---

### [ ] M4 — Recent Action & Outcome Projection

**Scope:** Runtime/Tools/Autonomy se bounded recent verified action/result state consume karke current self-state me last/recent action context expose karna.

**Deliverables:** Action-result adapters, bounded recent projection, verification-state mapping, tests.

**Acceptance gate:** Self Model action execute, verify ya long-term history own na kare; action request ko verified success na maana jaye.

---

### [ ] M5 — Self-State Conflict Reconciliation & Freshness Consumption

**Scope:** Multiple owner modules se conflicting self-state detect karna; Temporal Awareness ke age/freshness signals consume karke stale/conflicted state expose karna.

**Deliverables:** Conflict detector, reconciliation status, temporal adapter, refresh-request signals, tests.

**Acceptance gate:** Self Model apna separate freshness engine na banaye; conflicting sources silently merge na hon; source conflict inspectable rahe.

---

### [ ] M6 — Runtime + Temporal Awareness Integration

**Scope:** Runtime se live operational state aur Temporal Awareness se age/freshness/duration consume karke coherent self snapshot banana.

**Deliverables:** Adapters, event hooks, integration tests.

**Acceptance gate:** Self Model duplicate Runtime lifecycle ya Temporal calculations own na kare.

---

### [ ] M7 — Goals & Drives + Attention Integration

**Scope:** Goals & Drives se active objectives/blockers aur Attention se current focus/focus reason ko self-state projection me include karna.

**Deliverables:** Goal/attention adapters, projection mapping, integration tests.

**Acceptance gate:** Goal ownership Goals & Drives ke paas aur focus ownership Attention ke paas rahe; Self Model sirf reflect kare.

---

### [ ] M8 — World Model + Memory Integration

**Scope:** World Model se current environment/self relation aur Memory se selected relevant historical self-context consume karna.

**Deliverables:** World/Memory adapters, bounded context selection, retention boundary, integration tests.

**Acceptance gate:** Self Model environment model ya long-term memory store na bane; full live self-state blindly persist na ho.

---

### [ ] M9 — Planner + Autonomy Consumer Integration

**Scope:** Planner ko current capability/limitation/self-state context dena aur Autonomy ko current operational self-state expose karna.

**Deliverables:** Read-only consumer adapters, contracts, end-to-end tests.

**Acceptance gate:** Self Model planning, permission, risk policy, authorization ya action decision own na kare; sirf evidence-backed state provide kare.

---

### [ ] M10 — Real-PC Continuous Self-Model Acceptance

**Scope:** Real Windows session me multi-owner inputs se task/focus/capability/limitation/knowledge/action-result self-state continuously project aur reconcile karna.

**Deliverables:** Acceptance harness, long-session evidence, source-trace report, CPU/memory measurements, conflict/stale-state scenarios.

**Acceptance gate:** Real PC par coherent, fresh, bounded, low-overhead aur owner-traceable self-state maintain ho; contradictions/stale states explicit fail-closed form me surface hon.

## Final Completion Gate

Repo tab implementation-complete maana jayega jab:

- **M0–M10 sab verified** hon;
- Self Model kisi owner repository ki responsibility duplicate na kare;
- every critical self-state field ka provenance/owner traceable ho;
- stale/conflicted/unknown state explicitly represent ho;
- integrations evidence-backed hon;
- M10 real-PC acceptance PASS ho.
