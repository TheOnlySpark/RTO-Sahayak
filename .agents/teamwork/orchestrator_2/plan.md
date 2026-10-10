# Orchestration Plan: RTO Sahayak Milestone 2 (Laptop 2)

## Mission
Deliver Requirements R1, R2, and R3 for RTO Sahayak Milestone 2 according to Laptop 2 ownership rules.

## File Ownership
- Owned by Laptop 2: `data/`, `compare.py`, `pdf_tools.py`, `tests/`.
- Restricted: NEVER edit `app.py`, `agent.py`, `guardrail.py`, `tools.py`. If changes or requests are needed for other laptops, note in `HANDOFF_NOTES.md`.
- Target Locations: Both `e:\hackthon\` and `e:\hackthon\rto-sahayak\` for owned deliverables (`data/samples/`, `compare.py`, `tests/`).

## Milestones & Phases

### Phase 0: Survey & Architecture (3 Explorers in parallel)
- Explorer 1 (`survey_explorer_1`): Map current workspace files, check for existing `compare.py`, check `data/` and `tests/` structure, and check Pillow availability.
- Explorer 2 (`survey_explorer_2`): Analyze date normalization formats, fuzzy name matching algorithms (plain Python stdlib `difflib`, `re`, `datetime`), and mismatch schema `{"mismatches": [{"field", "doc_a", "value_a", "doc_b", "value_b"}]}` without judgmental words.
- Explorer 3 (`survey_explorer_3`): Analyze Pillow synthetic image design: 4 fake ID/certificate PNGs in `data/samples/`, "SYNTHETIC" banner, fake ID patterns (e.g. DL, Aadhaar/Voter ID mock), 2 sharing name but differing in DOB, corresponding JSON expected extracted fields.

### Phase 1: Implementation (Worker)
- Generate script and execute to create 4 fake ID PNGs and 4 JSON files in `data/samples/`.
- Implement `compare_documents(docs: list[dict])` in `compare.py`.
- Implement unit tests in `tests/test_compare.py` covering matching and mismatched pairs.
- Run tests and verify 100% pass rate.
- Update `HANDOFF_NOTES.md` if necessary.

### Phase 2: Multi-Agent Verification & Audit
- Reviewers (2): Verify adherence to all user rules, non-judgmental wording, file ownership, test passes.
- Challengers (2): Stress test `compare_documents` with edge cases (varied date formats, subtle name variations, empty/missing fields, multi-document comparison).
- Forensic Auditor (1): Audit code for genuine implementation (no hardcoded test bypasses, authentic Pillow generation, authentic comparison logic).

### Phase 3: Gate Evaluation & Sentinel Reporting
- Gate check across all agent reports in `GATE_STATUS.md`.
- Synthesize findings and report completion to Sentinel.
