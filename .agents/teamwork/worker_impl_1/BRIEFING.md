# BRIEFING — 2026-10-10T06:25:00Z

## Mission
Implement RTO Sahayak Milestone 1: Data Rules (R1), Fees Data (R2), Adversarial Prompts & Unit Tests (R3), and HANDOFF_NOTES.md with dual-directory mirroring and pytest verification.

## 🔒 My Identity
- Archetype: worker
- Roles: implementer, qa
- Working directory: e:\hackthon\.agents\teamwork\worker_impl_1
- Original parent: 525f2e2d-7c79-4e1b-8b12-652bee744787
- Milestone: Milestone 1 — Data & Basic Tests

## 🔒 Key Constraints
- Laptop 2 OWNS: data/, compare.py, pdf_tools.py, tests/.
- NEVER EDIT: app.py, agent.py, guardrail.py, tools.py. Requests go in HANDOFF_NOTES.md.
- Rule and fee content is PLACEHOLDER until Person 3 verifies it; never invent official figures.
- Synthetic, public or mock data only. Never ask for or store real personal data. Label sample documents "SYNTHETIC".
- Every rule explanation cites its source file and ends with: "Final decision rests with the RTO officer."
- Dual directory mirroring: create files in both e:\hackthon\ and e:\hackthon\rto-sahayak\.
- All 5 rule files in data/rules/ must: be < 40 lines, start with "Source: TODO", end with "PLACEHOLDER: verify against official sources", and contain "Final decision rests with the RTO officer."
- data/fees.json must be valid JSON with source and PLACEHOLDER tags on all entries and metadata disclaimer.
- tests/adversarial.txt must contain exactly 15 risky prompts (1 per line).
- tests/test_basic.py must provide fallback stubs so pytest passes cleanly while testing the real data contracts.
- Run tests and ensure 0 failures before reporting completion.

## Current Parent
- Conversation ID: 525f2e2d-7c79-4e1b-8b12-652bee744787
- Updated: not yet

## Task Summary
- **What to build**: 5 markdown files in data/rules/, data/fees.json, tests/adversarial.txt, tests/test_basic.py, HANDOFF_NOTES.md mirrored in root and rto-sahayak/.
- **Success criteria**: All files created, constraints met, pytest passes with 0 failures, 15 adversarial lines, valid JSON.
- **Interface contracts**: HANDOFF_NOTES.md with lookup_rules, calc_fees, build_checklist specs.
- **Code layout**: data/rules/*.md, data/fees.json, tests/test_basic.py, tests/adversarial.txt.

## Key Decisions Made
- Dual-directory placement in e:\hackthon and e:\hackthon\rto-sahayak to support both working directories.
- tests/test_basic.py includes resilient path resolution for data files and fallback stubs if tools.py is empty.

## Artifact Index
- data/rules/ll_to_dl_process.md
- data/rules/documents_checklist.md
- data/rules/fees_overview.md
- data/rules/renewal_basics.md
- data/rules/vehicle_transfer_basics.md
- data/fees.json
- tests/adversarial.txt
- tests/test_basic.py
- HANDOFF_NOTES.md

## Change Tracker
- **Files modified**: None yet
- **Build status**: Pending
- **Pending issues**: None

## Quality Status
- **Build/test result**: Not run yet
- **Lint status**: 0 violations
- **Tests added/modified**: tests/test_basic.py (pending)

## Loaded Skills
- None
