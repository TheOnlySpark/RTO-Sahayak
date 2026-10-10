# BRIEFING — 2026-10-10T07:45:00Z

## Mission
Investigate and design the document comparison engine for compare.py and test strategy for tests/test_compare.py.

## 🔒 My Identity
- Archetype: explorer
- Roles: Comparison Algorithm Explorer
- Working directory: e:\hackthon\.agents\teamwork\m2_explorer_2
- Original parent: e35c4cb9-e0bf-457f-8b67-5c1e9c1c606b
- Milestone: M2 - Document Comparison Engine Design

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Laptop 2 owns: data/, compare.py, pdf_tools.py, tests/
- Strictly NEVER edit: app.py, agent.py, guardrail.py, tools.py
- Stdlib only for compare.py (re, datetime, difflib, etc.)
- Strictly NO judgmental words like "rejected", "invalid", "fake", "forged", "fraudulent", etc. Only factual comparison!
- Student-explainable plain Python design

## Current Parent
- Conversation ID: e35c4cb9-e0bf-457f-8b67-5c1e9c1c606b
- Updated: 2026-10-10T07:45:00Z

## Investigation State
- **Explored paths**:
  - `ORIGINAL_REQUEST.md` (requirements R1, R2, R3)
  - `orchestrator_2/plan.md` (Milestone 2 roadmap & roles)
  - `rto-sahayak/compare.py` (verified currently empty 0-byte stub)
  - `tests/test_basic.py` (style, conventions, path resolution)
  - `rto-sahayak/tools.py` & `rto-sahayak/agent.py` (integration context)
  - `.agents/teamwork/m2_explorer_3/analysis.md` (synthetic samples schema, field names, matching/mismatched pairs)
- **Key findings**:
  - `compare.py` requires plain Python stdlib (`re`, `datetime`, `difflib`, `itertools`).
  - Dates require normalization across ISO, DMY, 2-digit years, and textual months to `YYYY-MM-DD`.
  - Names require case/whitespace normalization, honorifics stripping, token initials matching, and fuzzy SequenceMatcher ratio >= 0.85.
  - Multi-document comparison should use all-pairs combinations (`itertools.combinations`).
  - Output schema strictly: `{"mismatches": [{"field": ..., "doc_a": ..., "value_a": ..., "doc_b": ..., "value_b": ...}]}`.
  - Strictly non-judgmental language: no words like "rejected", "invalid", "fake", "forged", "fraudulent".
  - Alignment confirmed with `m2_explorer_3`'s 4 synthetic documents: (doc1, doc2) has DOB mismatch; (doc3, doc4) has matching identity with initials and different date formats.
- **Unexplored areas**:
  - None within explorer scope. Ready to compile handoff report.

## Key Decisions Made
- Use regex + datetime validation with explicit month dictionary for locale-independent cross-platform date normalization.
- Implement token-level initials matching (`Priya S. Patel` vs `Priya Sanjay Patel`) alongside `difflib.SequenceMatcher` at 0.85 threshold.
- Support canonical identity field aliasing (`name`/`full_name`, `dob`/`date_of_birth`).
- Exclude metadata fields (`doc_type`, `document_number`, `disclaimer`) from citizen identity comparison to prevent false positives.
- Designed comprehensive test suite for `tests/test_compare.py`.

## Artifact Index
- e:\hackthon\.agents\teamwork\m2_explorer_2\BRIEFING.md — Persistent working memory
- e:\hackthon\.agents\teamwork\m2_explorer_2\DISPATCH.md — Dispatch log
- e:\hackthon\.agents\teamwork\m2_explorer_2\progress.md — Progress and heartbeat
- e:\hackthon\.agents\teamwork\m2_explorer_2\handoff.md — Comprehensive handoff report
