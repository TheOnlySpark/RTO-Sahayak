# BRIEFING — 2026-10-10T06:16:00Z

## Mission
Survey the RTO Sahayak codebase to analyze how `lookup_rules`, `calc_fees`, and `build_checklist` are implemented, determine exact data schema/path expectations for rules and fees, and check consuming modules (`compare.py`, `pdf_tools.py`, `agent.py`, `guardrail.py`, `app.py`).

## 🔒 My Identity
- Archetype: explorer
- Roles: codebase investigation, schema & interface survey
- Working directory: e:\hackthon\.agents\teamwork\explorer_survey_1
- Original parent: 525f2e2d-7c79-4e1b-8b12-652bee744787
- Milestone: Survey & Codebase Interface Analysis

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Laptop 2 owns: data/, compare.py, pdf_tools.py, tests/
- Never edit app.py, agent.py, guardrail.py, tools.py
- Rule and fee content is PLACEHOLDER until verified
- Only write metadata in .agents/teamwork/explorer_survey_1/

## Current Parent
- Conversation ID: 525f2e2d-7c79-4e1b-8b12-652bee744787
- Updated: not yet

## Investigation State
- **Explored paths**:
  - `e:\hackthon\` root directory
  - `e:\hackthon\rto-sahayak\tools.py`
  - `e:\hackthon\rto-sahayak\app.py`, `agent.py`, `guardrail.py`
  - `e:\hackthon\rto-sahayak\compare.py`, `pdf_tools.py`
  - `e:\hackthon\rto-sahayak\data\` (`fees.json`, `rules/`, `open/`, `samples/`)
  - `e:\hackthon\rto-sahayak\tests\`
  - `e:\hackthon\rto-sahayak\HANDOFF_NOTES.md`, `README.md`, `requirements.txt`
  - `e:\hackthon\.agents\rules\project.md`, `ORIGINAL_REQUEST.md`
- **Key findings**:
  - All project files in `rto-sahayak/` (`tools.py`, `app.py`, `agent.py`, `guardrail.py`, `compare.py`, `pdf_tools.py`, `data/fees.json`) are currently 0 bytes (empty scaffolds).
  - `lookup_rules`, `calc_fees`, and `build_checklist` are not yet defined in `tools.py`.
  - Laptop 2 is forbidden from writing to `tools.py`, `app.py`, `agent.py`, `guardrail.py`. Laptop 2 owns `data/`, `compare.py`, `pdf_tools.py`, `tests/`.
  - We have specified complete interface signatures, schemas, error-handling contracts, and dual-location path resolution for `tools.py`, `data/`, and `tests/`.
- **Unexplored areas**: Implementation of the data and test files (delegated to Worker in Milestone 1 & 2).

## Key Decisions Made
- Define clear contract for `lookup_rules(topic: str)`, `calc_fees(service: str, vehicle_class: str)`, and `build_checklist(service_or_topic: str)`.
- Require `HANDOFF_NOTES.md` request for Laptop 1 regarding `tools.py`.
- Require tests in `tests/test_basic.py` to be self-sufficient with testable fallback stubs if `tools.py` remains empty.

## Artifact Index
- e:\hackthon\.agents\teamwork\explorer_survey_1\DISPATCH.md — incoming dispatch instructions
- e:\hackthon\.agents\teamwork\explorer_survey_1\progress.md — liveness and heartbeat
- e:\hackthon\.agents\teamwork\explorer_survey_1\handoff.md — 5-component survey report
