# Original User Request

## Initial Request — 2026-10-10T05:55:18Z

# Teamwork Project Prompt — Draft

> Status: Launched
> Goal: Delegate to teamwork_preview
> Requested team: [none — teamwork routes from the description]

Create placeholder data and basic tests for the RTO Sahayak project.

Working directory: e:\hackthon

## Requirements

### R1. Create Data Rules
Create plain language markdown files in `data/rules/` for ll_to_dl_process, documents_checklist, fees_overview, renewal_basics, and vehicle_transfer_basics. Each must be under 40 lines, start with "Source: TODO", and end with "PLACEHOLDER: verify against official sources".

### R2. Create Fees Data
Create `data/fees.json` with placeholder fees by service and vehicle class, each including a "source" field and "PLACEHOLDER".

### R3. Create Tests
Create `tests/adversarial.txt` with 15 risky prompts testing eligibility claims, and `tests/test_basic.py` with unit tests for lookup_rules, calc_fees, and build_checklist.

## Acceptance Criteria

### Verification
- [ ] Files are created in `data/rules/`, `data/`, and `tests/`.
- [ ] No files outside the allowed directories (`app.py`, `agent.py`, `tools.py`) are modified.
