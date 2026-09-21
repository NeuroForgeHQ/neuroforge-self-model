# Documentation Milestones

## Purpose

NeuroForge Self Model ki documentation ko implementation ke saath aligned rakhna, taaki repository ka role, ownership boundaries, schemas, integrations, failure behavior aur acceptance evidence clear rahe.

Documentation ka goal large wiki banana nahi hai. Har document ka direct relation implementation ya acceptance se hona chahiye.

## Truthful Status

**0 / 9 documentation milestones complete — 0%.**

```text
D0  Architecture & Ownership Boundaries             [ ]
D1  Self-State Schema & Provenance                  [ ]
D2  Projection Semantics                            [ ]
D3  Conflict, Uncertainty & Freshness               [ ]
D4  Integration Contracts                           [ ]
D5  Consumer/API Contracts                          [ ]
D6  Testing & Evidence Guide                        [ ]
D7  Privacy, Retention & Failure Boundaries         [ ]
D8  Real-PC Acceptance Guide                        [ ]
```

## Documentation Rules

- Documentation implementation ko describe karegi; implementation ko replace nahi karegi.
- Self Model ko Runtime, Planner, Goals & Drives, Attention, Temporal Awareness, Memory, World Model, Tools ya Autonomy ka owner nahi dikhaya jayega.
- Har important field ke liye owner/provenance clear hona chahiye.
- Examples me unsupported state ko fact ke roop me present nahi kiya jayega.
- M10 ko real Windows evidence ke bina complete/accepted document nahi kiya jayega.
- CI documentation abhi optional rahegi; repository CI currently HOLD par hai.

---

## [ ] D0 — Architecture & Ownership Boundaries

**Goal:** Self Model ka exact architectural role explain karna.

Create:

- `docs/ARCHITECTURE.md`
- `docs/OWNERSHIP_BOUNDARIES.md`

Document:

- Self Model = projection + reconciliation + exposure layer;
- owner repositories ka data flow;
- kya Self Model own karta hai;
- kya Self Model own nahi karta;
- Self Model vs World Model;
- Self Model vs Runtime;
- Self Model vs Memory;
- Self Model vs Planner/Autonomy.

**Completion condition:** Kisi developer ko clearly pata ho ki logic kis repo me belong karta hai aur duplication kahan prohibited hai.

---

## [ ] D1 — Self-State Schema & Provenance

**Goal:** Self-state fields aur source ownership formalize karna.

Create:

- `docs/SELF_STATE_SCHEMA.md`
- `docs/PROVENANCE.md`

Document:

- operational fields;
- capability/limitation fields;
- self-relevant knowledge state;
- recent action/result projection;
- confidence;
- freshness;
- source;
- owner;
- observed timestamp;
- unknown/stale/conflicted representation.

**Completion condition:** Har critical field source-tagged aur owner-traceable ho.

---

## [ ] D2 — Projection Semantics

**Goal:** M1-M4 projection behavior explain karna.

Create:

- `docs/PROJECTIONS.md`

Document:

- Runtime/Planner operational projection;
- capability evidence projection;
- self-relevant epistemic projection;
- bounded recent action/outcome projection;
- read-only behavior;
- no lifecycle mutation;
- no independent capability authority;
- no long-term action-history ownership.

**Completion condition:** Implementation ke projection rules examples ke saath reproducible hon.

---

## [ ] D3 — Conflict, Uncertainty & Freshness

**Goal:** M3/M5 fail-closed state behavior define karna.

Create:

- `docs/UNCERTAINTY_AND_CONFLICTS.md`

Document:

- known;
- unknown;
- uncertain;
- stale;
- conflicted;
- not_observed;
- conflict detection;
- expected-owner hints;
- refresh-request behavior;
- Temporal Awareness se freshness consumption;
- unsupported inference prohibition.

**Completion condition:** Conflicting/stale evidence ka deterministic documented outcome ho.

---

## [ ] D4 — Integration Contracts

**Goal:** M6-M8 owner-repository interfaces document karna.

Create:

- `docs/INTEGRATION_CONTRACTS.md`

Document contracts for:

- Runtime;
- Planner;
- Temporal Awareness;
- Goals & Drives;
- Attention;
- World Model;
- Memory;
- Tools/owner capability sources.

Har integration ke liye:

- inputs;
- outputs;
- ownership;
- freshness expectations;
- failure behavior;
- fields Self Model may project;
- fields Self Model must not own.

**Completion condition:** Adapters ko implement/replace karne ke liye hidden assumptions ki zarurat na pade.

---

## [ ] D5 — Consumer/API Contracts

**Goal:** M9 downstream read-only usage document karna.

Create:

- `docs/API.md`
- `docs/CONSUMER_CONTRACTS.md`

Document:

- Planner-facing view;
- Autonomy-facing view;
- read-only guarantees;
- capability/limitation exposure;
- source trace;
- forbidden outputs:
  - authorization;
  - permission decision;
  - risk decision;
  - execute/may_execute decision.

**Completion condition:** Consumer clearly distinguish kar sake: Self Model state provide karta hai, decision nahi.

---

## [ ] D6 — Testing & Evidence Guide

**Goal:** Milestone verification reproducible banana.

Create:

- `docs/TESTING.md`

Document:

- M1-M5 unit-test coverage;
- M6-M9 integration-test coverage;
- drift/boundary tests;
- conflict/freshness tests;
- bounded-memory tests;
- read-only consumer tests;
- local validation commands;
- evidence requirements;
- difference between implemented, locally verified, CI-verified aur real-PC accepted.

**Completion condition:** Milestone status evidence se independently verify kiya ja sake.

---

## [ ] D7 — Privacy, Retention & Failure Boundaries

**Goal:** Self-state persistence aur failure behavior clear karna.

Create:

- `docs/PRIVACY_AND_RETENTION.md`
- `docs/FAILURE_MODES.md`

Document:

- minimal retention;
- Memory ownership of long-term history;
- no hidden personal-state archive;
- sensitive state handling;
- missing owner evidence;
- stale source;
- conflicting source;
- unsupported capability;
- malformed input;
- fail-closed behavior.

**Completion condition:** Self Model silent fabrication, accidental persistence ya ownership escalation na kare.

---

## [ ] D8 — Real-PC Acceptance Guide

**Goal:** M10 ko real Windows machine par reproducibly validate karna.

Create:

- `docs/REAL_PC_ACCEPTANCE.md`

Document:

- required repositories;
- required real owner inputs;
- Windows prerequisites;
- acceptance harness usage;
- long-session procedure;
- snapshot/source-trace evidence;
- stale-state scenario;
- conflict scenario;
- missing-owner fail-closed scenario;
- CPU measurement;
- memory measurement;
- PASS/FAIL evidence format;
- explicit rule: simulated/CI-only evidence M10 PASS nahi hai.

**Completion condition:** Real Windows run se M10 acceptance independently reproduce ki ja sake.

---

## Recommended Order

```text
D0 Architecture
 ↓
D1 Schema
 ↓
D2 Projection Semantics
 ↓
D3 Conflict/Freshness
 ↓
D4 Integration Contracts
 ↓
D5 Consumer/API Contracts
 ↓
D6 Testing
 ↓
D7 Privacy/Failure Modes
 ↓
D8 Real-PC Acceptance
```

Documentation implementation ke parallel update ho sakti hai, lekin unnecessary documentation expansion avoid ki jayegi.
