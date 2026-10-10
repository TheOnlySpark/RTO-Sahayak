# Orchestration Plan: RTO Sahayak (Laptop 2)

## Mission
Deliver Requirements R1, R2, and R3 for RTO Sahayak according to Laptop 2 ownership rules.

## File Ownership
- Owned by Laptop 2: `data/`, `compare.py`, `pdf_tools.py`, `tests/`.
- Restricted: NEVER edit `app.py`, `agent.py`, `guardrail.py`, `tools.py`. If changes are needed, note in `HANDOFF_NOTES.md`.
- Target Locations: Both `e:\hackthon\` and `e:\hackthon\rto-sahayak\` for `data/` and `tests/`.

## Milestones

### Milestone 0: Survey & Codebase Investigation
- Spawn 3 Explorers to investigate:
  - Existing files in `e:\hackthon\` and `e:\hackthon\rto-sahayak\`.
  - How `lookup_rules`, `calc_fees`, and `build_checklist` are implemented in `tools.py` (to ensure data schema and test compatibility).
  - Structure of existing tests and data.
  - Verify exact paths and formats expected.

### Milestone 1: Implement R1 & R2 (Data & Rules)
- Worker creates plain language markdown files in `data/rules/`:
  - `ll_to_dl_process.md`
  - `documents_checklist.md`
  - `fees_overview.md`
  - `renewal_basics.md`
  - `vehicle_transfer_basics.md`
  - Each under 40 lines, starting with "Source: TODO", ending with "PLACEHOLDER: verify against official sources".
- Worker creates `data/fees.json`:
  - Placeholder fees by service and vehicle class.
  - Each including "source" field and "PLACEHOLDER".
- Files placed in both `e:\hackthon\data\` and `e:\hackthon\rto-sahayak\data\`.

### Milestone 2: Implement R3 (Tests)
- Worker creates `tests/adversarial.txt`:
  - Exactly 15 risky prompts testing eligibility claims.
- Worker creates `tests/test_basic.py`:
  - Unit tests for `lookup_rules`, `calc_fees`, `build_checklist`.
  - Must run cleanly with pytest and verify functionality without modifying `tools.py`.
- Files placed in both `e:\hackthon\tests\` and `e:\hackthon\rto-sahayak\tests\`.

### Milestone 3: Verification, Review & Audit
- Reviewers (2) verify code and test execution.
- Challengers (2) stress test and verify edge cases.
- Auditor (`teamwork_preview_auditor`) performs integrity forensics check.
- Run tests in both directories.

### Milestone 4: Final Victory Claim & Reporting
- Synthesize all findings and verification logs.
- Report back to parent orchestrator with full evidence.
