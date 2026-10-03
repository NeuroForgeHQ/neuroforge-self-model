# NeuroForge Self Model — Isolated Acceptance

Date: 2026-10-04 IST  
Current tested commit: `247c36ce6e052c2637eb4d9cb3836c1a15bc8257`  
Branch: `main`

## Verdict

**ISOLATED ACCEPTANCE: PASS**

```text
[████████████████████] 100% — ISOLATED PASS
```

## Fresh isolated verification

- Full standalone unittest suite: **25 / 25 PASS**
- Dedicated M0 contract tests: **6 / 6 PASS**
- Python compile/import integrity: **PASS**
- `git diff --check`: **PASS**
- Origin sync before evidence freeze: **0 behind / 0 ahead**
- M0–M10 implementation register: **11 / 11 VERIFIED**
- Source-code bugs found in this isolated run: **0**

## Verified isolated behavior

The fresh suite verifies projection-only ownership, provenance, bounded operational
state, capability/limitation projection, uncertainty handling, recent action outcome
projection, conflict reconciliation and safe downstream consumer views.

Important checks:

- blank provenance is rejected
- invalid confidence/freshness is rejected
- snapshot surface is read-only and owner traceable
- Self Model does not mutate Runtime/Planner lifecycle
- unsupported capability owners are rejected
- general knowledge is not admitted as operational self-state
- recent action history is bounded
- unverified action success **is not success**
- verified results require provenance
- conflicts are **not silently merged**
- stale state is consumed from Temporal Awareness, not recomputed locally
- Runtime and Temporal ownership remain separate
- Goals and Attention ownership remains explicit
- Memory projection is bounded
- Planner view remains projection-only
- Autonomy view contains **no action decision**

## M10 evidence recheck

The local M10 evaluator was freshly run against the repository's already-committed
real-PC evidence and returned **PASS**.

Recorded live evidence:

- duration: **600.000335 s**
- average Self Model CPU: **0.0045573%**
- peak memory: **40.8594 MB**
- continuous snapshots: **121**
- stale scenario: **PASS**
- conflict scenario: **PASS**
- missing-owner fail-closed: **PASS**
- recorded Self Model implementation SHA:
  `6315d64bb1a87974ff1116c1bd5de73ecfd85b69`

This was **not a new 10-minute live-PC run**. Current commit `247c36c` was freshly
verified by the isolated 25-test suite; the committed M10 live evidence belongs to
the earlier accepted implementation SHA shown above.

## Scope boundary

Fresh cross-repository M6–M9 owner execution and fresh M10 live-PC collection are
outside this isolated-repo gate and were deliberately not rerun here.
