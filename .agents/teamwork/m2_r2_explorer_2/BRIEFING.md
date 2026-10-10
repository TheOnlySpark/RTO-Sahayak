# BRIEFING — 2026-10-10T14:37:45Z

## Mission
Investigate and remediate comparison engine bug (spurious issue_date/expiry_date mismatches) and evasive test assertion in tests/test_compare.py.

## 🔒 My Identity
- Archetype: explorer
- Roles: Comparison Engine & Tests Remediation Explorer
- Working directory: e:\hackthon\.agents\teamwork\m2_r2_explorer_2
- Original parent: e35c4cb9-e0bf-457f-8b67-5c1e9c1c606b
- Milestone: Remediation Round 2

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Laptop 2 owns: data/, compare.py, pdf_tools.py, tests/
- Strictly NEVER edit: app.py, agent.py, guardrail.py, tools.py
- Rule and fee content is PLACEHOLDER until Person 3 verifies it; never invent official figures.

## Current Parent
- Conversation ID: e35c4cb9-e0bf-457f-8b67-5c1e9c1c606b
- Updated: not yet

## Investigation State
- **Explored paths**:
  - `compare.py` & `rto-sahayak/compare.py` (lines 58-63, 280-333)
  - `tests/test_compare.py` & `rto-sahayak/tests/test_compare.py` (lines 250-305)
  - `tests/test_adversarial_compare.py` (lines 1-258)
  - `data/samples/*.json` (all 4 synthetic schema files)
  - `data/samples/*.png` (all 4 facade text files)
  - `generate_samples.py` (standalone Pillow generation pipeline)
  - Prior audit/review reports (`m2_auditor_1`, `m2_reviewer_1`, `m2_challenger_2`, `orchestrator_2/GATE_STATUS.md`)
- **Key findings**:
  1. `compare.py` omits `issue_date` and `expiry_date` from `METADATA_FIELDS`. Because `"date" in canonical` evaluates to True, `compare_documents` compares issue dates across documents, causing a false positive mismatch between matching pair `doc3` (2018-03-15) and `doc4` (2017-01-10), and adding a 2nd mismatch to `doc1` vs `doc2`.
  2. `tests/test_compare.py` lines 264-268 uses `os.path.getsize(fpath) > 0` instead of binary image validation. This allowed plain text stub files (~550 bytes) to pass as valid PNG images.
- **Unexplored areas**:
  - None. Both bug mechanism and evasive assertion root causes are fully identified with exact line numbers and proposed drop-in replacements.

## Key Decisions Made
- Exclude document lifecycle/validity attributes (`issue_date`, `expiry_date`, `valid_till`, etc.) in `METADATA_FIELDS` and normalize keys before lookup to ensure robust matching across case and delimiters.
- Formulate upgraded test assertions in `tests/test_compare.py` combining 8-byte PNG signature (`b"\x89PNG\r\n\x1a\n"`), Pillow `Image.open`, format check, (800, 500) dimension check, and raster data load check (`img.load()`).

## Artifact Index
- DISPATCH.md — Dispatch notification
- progress.md — Liveness heartbeat
- BRIEFING.md — Persistent context
- handoff.md — 5-component self-contained remediation report
