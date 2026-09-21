# Testing & Evidence Guide

## Purpose
Define how Self Model milestones are verified without confusing code existence, local tests, CI, integration wiring, or real-PC acceptance.

## Verification levels
- Implemented: required code path exists.
- Locally tested: relevant local tests were executed and evidence was recorded.
- CI verified: repository CI executed successfully.
- Integrated: real owner repositories are wired through intended interfaces.
- Real-PC accepted: required real Windows acceptance passed with real owner evidence.

One level does not imply the next.

## Test files

### M1-M5
tests/test_m1_m5.py currently contains 11 test methods covering:
- operational projection and owner preservation;
- capability evidence ownership;
- rejection of unrecognized capability owners;
- self-relevant knowledge bounds and general-knowledge rejection;
- unverified-result and provenance behavior;
- bounded recent-action projection;
- conflict detection;
- stale freshness consumption;
- consistent evidence reconciliation.

### M6-M10 code paths
tests/test_m6_m10.py currently contains 8 test methods covering:
- Runtime + Temporal owner separation;
- Goals & Drives + Attention ownership;
- bounded World Model / Memory projection;
- Planner read-only view;
- Autonomy view without action decisions;
- merge-conflict rejection;
- M10 fail-closed behavior without real Windows evidence;
- M10 harness acceptance of a complete evidence contract.

The M10 positive unit test validates the harness contract, not a real-PC run.

## Local validation commands

~~~text
python -m unittest tests.test_m1_m5
python -m unittest tests.test_m6_m10
python -m unittest discover -s tests -p "test_*.py"
~~~

Future PASS counts must come from actual command output, not from counting methods in the files.

## Evidence requirements
For local verification record:
- commit SHA;
- Python version;
- platform;
- exact command;
- test count;
- PASS/FAIL output;
- date/time.

For integration verification also capture:
- owner repository commits;
- adapter/interface used;
- real vs fixture/simulated source;
- source_trace sample;
- failure-scenario evidence.

## Anti-drift checks
Important boundary checks include:
- no Runtime lifecycle mutation from Self Model;
- capability owner validation;
- no general-knowledge expansion;
- no silent conflict merge;
- no Self Model freshness calculation;
- bounded memory/action projections;
- read-only consumers;
- no permission/risk/action decision outputs;
- fail-closed real-PC acceptance.

## M10 distinction
Unit tests, simulated Windows evidence, CI, fabricated owner inputs, a single synthetic snapshot, or harness existence are not enough to mark M10 complete.

M10 requires real Windows plus real owner-source evidence.

## CI status
CI is currently HOLD. Local evidence must not be labeled CI verified.

## Recorded status caveat
At documentation time, tests/test_m6_m10.py contains 8 test methods while an older status note recorded "7 tests PASS". That old numeric claim is stale/inconsistent and must be replaced by a fresh test run before a new PASS count is claimed.
