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


## Follow-up — 2026-10-10T07:36:23Z

# Teamwork Project Prompt — Draft

> Status: Launched
> Goal: Delegate to teamwork_preview
> Requested team: [none — teamwork routes from the description]

Create synthetic ID documents, expected field JSONs, and a document comparison script with tests.

Working directory: e:\hackthon

## Requirements

### R1. Synthetic Images
Create a Python script to generate 4 fake ID/certificate PNGs in `data/samples/` using Pillow. Each must be marked "SYNTHETIC" with clear fake ID patterns. Two images must share a person's name but differ in date of birth. Save the expected extracted fields as a JSON file for each image.

### R2. Comparison Script
Implement `compare_documents(docs: list[dict])` in `compare.py` in plain Python. It must normalise dates in multiple formats, fuzzy-match names, and return factual mismatches in the format: `{"mismatches": [{"field", "doc_a", "value_a", "doc_b", "value_b"}]}`. It must not use judgmental words like "rejected" or "invalid".

### R3. Unit Tests
Implement unit tests in `tests/` for the `compare_documents` function, covering both a mismatched pair and a matching pair. Execute the tests to ensure they pass.

## Acceptance Criteria

### Verification
- [ ] 4 PNGs and 4 JSON files exist in `data/samples/`.
- [ ] `compare.py` contains the `compare_documents` function meeting the requirements.
- [ ] Tests exist in `tests/` and pass when run.
- [ ] `app.py`, `agent.py`, and `tools.py` are strictly not modified.
