# NeuroForge Self Model

`neuroforge-self-model` NeuroForge ki **self-state representation layer** hai.

Iska purpose AI ko continuously ye samajhne dena hai ki:

- main abhi kya kar raha hoon;
- mera current task kya hai;
- main kya jaanta hoon;
- mujhe kya nahi pata;
- meri current capabilities kya hain;
- meri current limitations kya hain;
- maine recently kya attempt kiya;
- kaunse goals active hain;
- kaunse blockers mujhe rok rahe hain;
- meri current focus/state kya hai.

> **Self Model = NeuroForge ka structured internal answer to “main abhi kis state me hoon?”**

Ye consciousness, identity ya biological self-awareness ka claim nahi karta. Ye machine-readable operational self-state hai.

## Goal

NeuroForge ko ek lightweight, local-first self-model dena jo current internal state ko explicit aur inspectable form me maintain kare.

Example:

```text
Current Task       : Runtime acceptance testing
Current Focus      : Investigating failed test
Active Goal        : Complete Jarvis deployment
Known Capability   : Can run local test harness
Current Limitation : Human microphone evidence unavailable
Last Action        : Re-ran acceptance test
Last Result        : FAIL
Confidence         : High
State Freshness    : Recent
```

## Self Model Kyun Important Hai?

Self Model ke bina AI alag-alag modules se state le sakta hai, lekin uske paas apni current operational condition ka coherent view nahi hota.

Without Self Model:

```text
Planner knows current plan.
Goals knows active objective.
Attention knows focus.
Runtime knows active task.
Memory knows previous attempts.
```

With Self Model:

```text
I am currently working on Runtime acceptance.
My active goal is deployment.
My current focus is the failing test.
I already attempted a rerun.
I cannot complete microphone acceptance without human evidence.
```

Isse NeuroForge ko continuity aur self-consistency milti hai.

## Core Responsibilities

### 1. Current Operational State

Maintain:

- current task;
- current subtask;
- current focus;
- current mode;
- current active module/process;
- current session state.

### 2. Capability Awareness

Represent kare ki system currently kya kar sakta hai.

Example:

```text
can_read_desktop_state     : true
can_run_local_tests        : true
can_use_microphone         : unknown
can_send_external_message  : permission_required
```

Capability hard-coded claim nahi honi chahiye. Runtime/tool availability aur real evidence ke basis par update honi chahiye.

### 3. Limitation Awareness

NeuroForge ko apni active limitations pata honi chahiye.

Examples:

- required tool unavailable;
- permission missing;
- current context stale;
- network unavailable;
- human evidence required;
- unsupported capability;
- low confidence;
- resource limit reached.

### 4. Knowledge State

Self Model ko distinguish karna chahiye:

```text
known
unknown
uncertain
stale
conflicted
not_observed
```

Example:

```text
Current screen state : known
User's next intent   : unknown
Last test status     : known
Mic availability     : uncertain
```

### 5. Current Goals & Intent

`neuroforge-goals-drives` se:

- active goal;
- current subgoal;
- blocked goal;
- priority;
- unfinished commitment

consume kiya ja sakta hai.

Self Model goal own nahi karega; sirf current self-state me reflect karega.

### 6. Current Focus

`neuroforge-attention` se current focus consume karega.

Example:

```text
Current Focus : runtime_test_failure
Focus Reason  : blocks active deployment goal
Focus Age     : 2 minutes
```

### 7. Recent Actions & Outcomes

Track bounded recent action state:

```text
Last Action  : run_acceptance_test
Result       : failed
Occurred     : 45 seconds ago
Verified     : true
```

Long-term action history Memory ke paas jayegi.

### 8. Confidence & Provenance

Har important self-state ke saath source aur confidence hona chahiye.

Example:

```text
State      : current_task = runtime acceptance
Source     : runtime
Confidence : 1.0
```

### 9. Contradiction Detection

Agar modules conflicting state dein:

```text
Planner says task active
Runtime says task stopped
```

to Self Model silently ek ko true declare na kare.

Possible output:

```text
task_state : conflicted
resolution : request fresh runtime state
```

### 10. Self-State Queries

Queries jaise:

```text
Main abhi kya kar raha hoon?
Mera current goal kya hai?
Main kis cheez par focused hoon?
Mujhe kya nahi pata?
Meri current limitation kya hai?
Maine last kya attempt kiya?
Main is task ko abhi kyun continue nahi kar sakta?
```

## Self Model Kya Nahi Hai

Ye repo directly own nahi karega:

- personality;
- emotions;
- general memory;
- world/environment state;
- task planning;
- action execution;
- autonomy;
- language generation;
- reasoning.

Boundaries:

```text
Self Model       → main kis operational state me hoon
World Model      → environment kis state me hai
Memory           → past me kya retain hua
Goals & Drives   → kya accomplish karna hai
Attention        → abhi kis cheez par focus hai
Planner          → next steps kya hain
Autonomy         → proactive action consider karna hai ya nahi
Tools            → actual action execute karna
```

## Self Model vs World Model

```text
World Model:
  VS Code active hai
  test process running hai
  file modified hai

Self Model:
  main runtime test par kaam kar raha hoon
  mera current focus failed acceptance hai
  meri next capability test rerun karna hai
```

Dono connected hain, lekin duplicate nahi.

## Proposed Self State Model

```text
SelfState
├── current_task
├── current_focus
├── active_goals
├── capabilities
├── limitations
├── knowledge_state
├── recent_actions
├── recent_results
├── confidence
├── provenance
├── blockers
└── updated_at
```

## NeuroForge Integration

```text
Runtime / Goals / Attention / World Model / Memory
                    │
                    ▼
                Self Model
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
   Planner       Autonomy     Conversation
      │             │             │
      └─────────────┼─────────────┘
                    ▼
                  Runtime
```

## Key Integrations

### Runtime

Runtime actual current task/session/module state provide karega.

### Goals & Drives

Current objectives, blockers aur unfinished work provide karega.

### Attention

Current focus aur focus reason provide karega.

### World Model

Environment ke saath self relation provide karega.

### Temporal Awareness

State age, freshness, last-action timing aur duration provide karega.

### Memory

Relevant past attempts aur retained self-history provide kar sakta hai.

### Planner

Planner Self Model se current capability/limitations consume kar sakta hai.

### Autonomy

Autonomy ko pata ho sakta hai ki system currently kya kar raha hai, kya kar sakta hai, aur kya blocked hai.

## Alive-Like AI Direction

```text
Perception
   ↓
Attention
   ↓
World Model
   ↓
Memory ← Temporal Awareness → Self Model
   ↓
Language Model / Cognition
   ↓
Goals & Drives
   ↓
Planner
   ↓
Autonomy
   ↓
Tools
   ↓
Observe result
   ↓
Update Self Model
```

Self Model NeuroForge ko continuous operational identity deta hai — consciousness nahi, but persistent state coherence.

## Reliability Rules

```text
Verified capability    → known
Unavailable evidence   → unknown
Conflicting state      → conflicted
Old state              → stale
Unsupported capability → unavailable
Permission missing     → blocked
```

Self Model ko unsupported confidence generate nahi karna chahiye.

## Privacy

Self Model me personal context aa sakta hai, isliye:

- local-first;
- bounded state;
- minimal retention;
- sensitive content redaction;
- no hidden cloud sync;
- long-term retention Memory policy ke through.

## Design Principles

- CPU-first
- local-first
- low idle overhead
- event-driven updates
- explicit provenance
- explicit uncertainty
- bounded state
- stale-data protection
- capability claims evidence-based
- limitation awareness
- no consciousness claims
- no hidden authority
- no duplicated ownership from other repos

## Suggested Repository Structure

```text
neuroforge-self-model/
├── self_model/
│   ├── state/
│   ├── capabilities/
│   ├── limitations/
│   ├── knowledge/
│   ├── actions/
│   ├── conflicts/
│   └── queries/
├── integrations/
│   ├── runtime/
│   ├── goals_drives/
│   ├── attention/
│   ├── world_model/
│   ├── temporal_awareness/
│   ├── memory/
│   ├── planner/
│   └── autonomy/
├── schemas/
├── tests/
├── examples/
└── docs/
```

## Initial Capability Roadmap

```text
M0  Self-state contracts and foundation
M1  Current task/session state
M2  Capability and limitation model
M3  Knowledge-state and uncertainty
M4  Recent actions and verified outcomes
M5  Conflict detection and freshness
M6  Runtime + Temporal Awareness integration
M7  Goals & Drives + Attention integration
M8  World Model + Memory integration
M9  Planner + Autonomy integration
M10 Real-PC continuous self-model acceptance
```

Documentation alone milestone complete nahi karega. Har milestone ke liye implementation, tests aur evidence required hain.

## Long-Term Vision

NeuroForge ko continuously clear answer hona chahiye:

```text
Main abhi kya kar raha hoon?
Main kya accomplish karne ki koshish kar raha hoon?
Main kis cheez par focused hoon?
Main kya jaanta hoon?
Mujhe kya nahi pata?
Main kya kar sakta hoon?
Main kya nahi kar sakta?
Mujhe kya block kar raha hai?
Maine last kya kiya aur uska result kya tha?
```

Objective hai NeuroForge ko **continuous, evidence-based operational self-awareness** dena.

> **NeuroForge Self Model — AI ko apni current operational state, capabilities, limitations aur ongoing intent ka coherent model dena.**
