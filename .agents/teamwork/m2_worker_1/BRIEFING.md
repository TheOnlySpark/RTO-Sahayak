# BRIEFING — 2026-10-10T07:49:00Z

## Mission
Implement Milestone 2 deliverables: synthetic sample documents & JSONs, robust document comparison engine in compare.py, comprehensive unit tests in tests/test_compare.py, mirrored to rto-sahayak/, adhering strictly to non-judgmental wording and integrity mandates.

## 🔒 My Identity
- Archetype: implementer / qa
- Roles: implementer, qa
- Working directory: e:\hackthon\.agents\teamwork\m2_worker_1
- Original parent: e35c4cb9-e0bf-457f-8b67-5c1e9c1c606b
- Milestone: Milestone 2 (Document Comparison & Synthetic Data)

## 🔒 Key Constraints
- Genuine implementation only: DO NOT hardcode test results, dummy facades, or shortcuts.
- File ownership: I OWN data/samples/, compare.py, tests/test_compare.py, HANDOFF_NOTES.md, generator script.
- STRICTLY NEVER EDIT: app.py, agent.py, guardrail.py, tools.py. Requests go in HANDOFF_NOTES.md.
- Mirror deliverables in both root `e:\hackthon\` and subproject `e:\hackthon\rto-sahayak\`.
- Synthetic images must be clearly marked "SYNTHETIC" and "DRAFT - for citizen review and officer verification" with clear fake ID patterns.
- Strictly NO judgmental words anywhere in code, docstrings, or return values (no "rejected", "invalid", "fake", "forged", "fraudulent", etc.).
- Output format for mismatches: `{"mismatches": [{"field": ..., "doc_a": ..., "value_a": ..., "doc_b": ..., "value_b": ...}]}`.
- Rule & fee content: placeholder until verified.

## Current Parent
- Conversation ID: e35c4cb9-e0bf-457f-8b67-5c1e9c1c606b
- Updated: not yet

## Task Summary
- **What to build**:
  1. Synthetic images (4 PNGs) + 4 extracted JSONs in `data/samples/` and `rto-sahayak/data/samples/`.
  2. `compare_documents` in `compare.py` and `rto-sahayak/compare.py` with multi-format date normalization, fuzzy name matching, factual mismatch reporting.
  3. Comprehensive unit tests in `tests/test_compare.py` and `rto-sahayak/tests/test_compare.py` covering all features and non-judgmental vocabulary assertion.
  4. Handoff report and HANDOFF_NOTES.md.
- **Success criteria**: All tests pass under pytest/unittest, 0 forbidden words in compare.py, valid synthetic assets, full test coverage.
- **Interface contracts**: `compare_documents(docs: list[dict]) -> dict` returning `{"mismatches": [...]}`.
- **Code layout**: Root repo and mirrored in rto-sahayak/.

## Change Tracker
- **Files modified**: None yet
- **Build status**: Pending
- **Pending issues**: None

## Quality Status
- **Build/test result**: Not run yet
- **Lint status**: Clean
- **Tests added/modified**: Pending

## Loaded Skills
- None specified in dispatch.

## Key Decisions Made
- [Initial]: Will generate high-clarity synthetic document PNGs using Pillow script and pair them with exact JSON representations.
- [Initial]: compare.py will use stdlib only (re, difflib, datetime) to ensure zero heavyweight dependency and maximum robustness.

## Artifact Index
- e:\hackthon\.agents\teamwork\m2_worker_1\DISPATCH.md
- e:\hackthon\.agents\teamwork\m2_worker_1\BRIEFING.md
- e:\hackthon\.agents\teamwork\m2_worker_1\progress.md
