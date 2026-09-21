# Privacy & Retention Boundaries

## Principle
Self Model should retain only the minimum operational self-state needed for current behavior. It must not become a hidden personal-history database.

## Retention ownership
Long-term retained history belongs to neuroforge-memory.

Self Model may consume a bounded projection of selected relevant memory, but it must not silently copy the full Memory store.

Current WorldMemoryIntegrator behavior:
- accepts selected memory items;
- projects only a bounded subset;
- exposes limited fields such as memory_id, summary, source, and relevance;
- does not create an independent long-term memory archive.

## Recent-action retention
ActionOutcomeProjector is bounded. Its default projection window is 8 recent outcomes. This is not a permanent action ledger.

## Sensitive state
When owner repositories provide sensitive state, Self Model should:
- project only fields needed by the current consumer;
- preserve source ownership;
- avoid unnecessary duplication;
- avoid turning transient state into long-term history;
- defer persistence policy to the actual storage owner.

This repository is not a complete privacy-policy or secrets-management subsystem.

## No hidden archive
Self Model must not independently accumulate full conversation history, private files, credentials, raw desktop history, raw sensor streams, permanent behavioral logs, or a full user-profile history.

## Source trace
Source trace should identify provenance without unnecessarily duplicating full source payloads.

## Persistence rule
Current Self Model code is projection-oriented. Documentation must not claim durable persistence unless future code explicitly adds it together with ownership, retention duration, deletion behavior, sensitivity classification, and tests.

## Boundary summary

~~~text
Memory owns long-term history.
World Model owns live environment state.
Self Model owns bounded operational projection.
~~~
