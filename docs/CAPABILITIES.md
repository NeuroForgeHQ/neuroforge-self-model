# Self Model Capabilities

## Purpose

`neuroforge-self-model` NeuroForge ko **coherent operational self-state** provide karta hai.

Iska role AI ko ye samajhne me help karna hai:

> **"Main abhi kis state me hoon?"**

Self Model khud reasoning, planning, memory, perception, tools ya autonomy ka replacement nahi hai. Ye owner repositories se evidence consume karke AI ki current operational state ko structured form me represent karta hai.

---

# AI Ko Self Model Kya Capabilities Deta Hai

## 1. Current Task Awareness

AI represent kar sakta hai:

- current task;
- current subtask;
- current session;
- active module;
- active process;
- current execution state.

Example:

```text
Current Task    : Runtime acceptance
Current Subtask : Re-run failed tests
Active Module   : neuroforge-runtime
Session         : testing-session-21
```

**Important:** Self Model task lifecycle own nahi karta. Runtime/Planner authoritative owners rehte hain.

---

## 2. Current Focus Awareness

AI ko pata ho sakta hai ki abhi focus kis cheez par hai.

Example:

```text
Current Focus : failed acceptance test
Focus Reason  : blocks active deployment goal
```

Focus ka owner `neuroforge-attention` hai. Self Model sirf us state ko reflect karta hai.

---

## 3. Goal Awareness

AI apne current operational state me active goals reflect kar sakta hai:

- active goal;
- goal priority;
- blockers;
- unfinished objective context.

Example:

```text
Active Goal : Complete NeuroForge deployment
Priority    : High
Blocked By  : Real microphone acceptance
```

Goals create/prioritize karna `neuroforge-goals-drives` ka responsibility hai.

---

## 4. Capability Awareness

AI represent kar sakta hai ki currently kaunsi capability available, unavailable, unknown ya permission-dependent hai.

Example:

```text
run_local_tests        : available
read_desktop_context   : available
use_microphone         : unknown
send_external_message  : permission_required
```

Self Model capability implement nahi karta. Ye Runtime, Tools aur other owner modules ke evidence ko reflect karta hai.

---

## 5. Limitation Awareness

AI apni current limitations ko structured form me represent kar sakta hai.

Examples:

- required tool unavailable;
- permission missing;
- required owner evidence unavailable;
- context stale;
- low confidence;
- unsupported capability;
- resource limit reached;
- real-PC evidence required.

Example:

```text
Current Limitation : Human microphone evidence unavailable
Effect             : Voice acceptance cannot be marked complete
```

---

## 6. Self-Relevant Knowledge State

AI operationally relevant cheezon ko classify kar sakta hai:

```text
known
unknown
uncertain
stale
conflicted
not_observed
```

Examples:

```text
Current task        : known
Mic availability    : uncertain
Current screen      : stale
Last action result  : known
User next intent    : unknown
```

Self Model general knowledge base nahi hai.

---

## 7. Uncertainty Awareness

AI ko pata ho sakta hai ki uske paas reliable evidence hai ya nahi.

Self Model confidence, source aur provenance retain kar sakta hai.

Example:

```text
Field      : current_task
Value      : Runtime acceptance
Owner      : runtime
Source     : runtime.current_task
Confidence : 1.0
Freshness  : fresh
```

Isse AI unsupported certainty avoid kar sakta hai.

---

## 8. Conflict Awareness

Agar do owner modules contradictory state dein, Self Model conflict expose kar sakta hai.

Example:

```text
Runtime : task stopped
Planner : task active

Self Model:
task_state = conflicted
refresh_required = true
```

Self Model ko silently ek source ko fact declare nahi karna chahiye.

---

## 9. Freshness Awareness

Self Model Temporal Awareness se freshness metadata consume kar sakta hai:

- fresh;
- recent;
- aging;
- stale;
- expired;
- unknown.

Example:

```text
Current screen state : stale
Current task state   : fresh
```

Freshness calculate karna `neuroforge-temporal-awareness` ka responsibility hai.

---

## 10. Recent Action Awareness

AI represent kar sakta hai:

- recent action;
- action owner;
- attempted result;
- verified/unverified outcome;
- source evidence.

Example:

```text
Last Action : run acceptance test
Result      : failed
Verified    : true
Source      : runtime test result
```

Self Model action execute ya verify khud nahi karta.

---

## 11. Outcome Awareness

Self Model action request aur verified result me difference preserve kar sakta hai.

```text
Action requested != Action succeeded
```

Agar success verify nahi hui:

```text
Result : unverified
```

Ye false success claims ko reduce karta hai.

---

## 12. Environment-to-Self Relation

World Model se AI apne current environment ke saath relation represent kar sakta hai.

Example:

```text
World Model:
VS Code open
python process running
test failed

Self Model:
I am currently working on the failed Runtime acceptance test.
```

World/environment state ka owner `neuroforge-world-model` hai.

---

## 13. Relevant Memory Context Awareness

Memory se selected relevant past context Self Model me reflect ho sakta hai.

Example:

```text
Relevant Previous Attempt:
- same acceptance test failed earlier
- previous fix was applied
```

Long-term history ka owner `neuroforge-memory` hai.

---

## 14. Blocker Awareness

AI ko pata ho sakta hai ki current task kyun continue nahi ho raha.

Example:

```text
Current Goal : Complete voice acceptance
Blocked By   : Real human microphone evidence missing
```

Ye Planner aur Autonomy ko useful operational context provide karta hai.

---

## 15. Read-Only Planner Context

Planner Self Model se consume kar sakta hai:

- current task;
- capabilities;
- limitations;
- blockers;
- current goal/focus;
- verified recent result;
- uncertainty.

Self Model plan create nahi karta.

---

## 16. Read-Only Autonomy Context

Autonomy Self Model se current operational state consume kar sakti hai.

Example:

```text
Current Task      : test validation
Current Limitation: required evidence missing
Current State     : blocked
```

Self Model ye decide nahi karta:

```text
may_execute
authorized
risk_decision
permission_decision
```

Ye `neuroforge-autonomy` aur permission/action owners ke paas rehta hai.

---

# Self Model AI Ko Kya Nahi Deta

Self Model directly ye capabilities provide nahi karta:

| Capability | Actual Owner |
| --- | --- |
| Language understanding | NLP / Language Model |
| Reasoning | Reasoning Core |
| Long-term memory | Memory |
| Current environment model | World Model |
| PC sensing | Desktop Context / Vision |
| Time calculation | Temporal Awareness |
| Goal creation/prioritization | Goals & Drives |
| Focus selection | Attention |
| Planning | Planner |
| Proactive action decision | Autonomy |
| Permission/authorization | Autonomy / Tools policy |
| Mouse/keyboard/file actions | Tools |
| Conversation generation | Conversation Core |
| Emotions/personality | Companion |
| Consciousness | Not claimed |

---

# Important Architectural Rule

Self Model ka role:

```text
Owner repositories
      ↓
verified evidence
      ↓
Self Model
      ↓
coherent operational self-state
      ↓
Planner / Autonomy / Conversation
```

Self Model ka role **state ko own karna nahi**, balki:

```text
PROJECT
RECONCILE
TRACE
EXPOSE
```

karna hai.

---

# Current Implementation Status

Current repository me following code-level capabilities present hain:

- operational-state projection;
- capability evidence projection;
- self-relevant knowledge/uncertainty representation;
- recent action/outcome projection;
- conflict/stale state handling;
- Runtime/Temporal integration interfaces;
- Goals/Attention integration interfaces;
- World Model/Memory integration interfaces;
- Planner/Autonomy read-only consumer views;
- M10 real-PC acceptance harness.

However, important distinction:

> **Integration interfaces implemented hone ka matlab real NeuroForge owner repositories ke saath live continuous wiring complete hona nahi hai.**

Current missing/unfinished capabilities include:

- real cross-repository event/API wiring;
- continuous long-running SelfState engine;
- real owner-source stream consumption;
- real Windows long-session validation;
- M10 real-PC acceptance.

---

# Target Runtime Behavior

Final NeuroForge me expected flow:

```text
Runtime ───────────────┐
Temporal Awareness ────┤
Goals & Drives ────────┤
Attention ─────────────┤
World Model ───────────┤
Memory ────────────────┤
Tools / Results ───────┤
                       ▼
                  Self Model
                       ▼
              Continuous SelfState
                       ▼
        Planner / Autonomy / Conversation
```

Expected AI-visible state:

```text
What am I doing?
What am I focused on?
What goal am I pursuing?
What do I know?
What do I not know?
What can I currently do?
What can I not do?
What is blocking me?
What did I recently attempt?
Was the result verified?
Is my current information fresh?
Are my sources conflicting?
```

---

# Core Capability Summary

```text
Self Model gives NeuroForge:

✓ current operational self-state
✓ task awareness
✓ focus awareness
✓ goal awareness
✓ capability awareness
✓ limitation awareness
✓ self-relevant uncertainty awareness
✓ conflict awareness
✓ freshness awareness
✓ recent action/result awareness
✓ blocker awareness
✓ source/provenance awareness
✓ coherent state for Planner/Autonomy/Conversation

Self Model does NOT give NeuroForge:

✗ reasoning
✗ planning
✗ memory ownership
✗ world sensing
✗ tool execution
✗ permission authority
✗ autonomy decisions
✗ emotions
✗ consciousness
```

> **Self Model = NeuroForge ka evidence-based operational answer to “main abhi kis state me hoon?”**
