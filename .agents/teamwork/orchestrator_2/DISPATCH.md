# Dispatch Record

## 2026-10-10T07:37:31Z
You are the Project Orchestrator for RTO Sahayak milestone 2.
Your assigned workspace directory is e:\hackthon\.agents\teamwork\orchestrator_2.
Read the authoritative user request at e:\hackthon\.agents\teamwork\ORIGINAL_REQUEST.md (specifically the latest request timestamped 2026-10-10T07:36:23Z).

User & Project Constraints:
- Laptop 2 ownership: data/, compare.py, pdf_tools.py, tests/.
- Strictly NEVER edit: app.py, agent.py, guardrail.py, tools.py. Requests for other laptops go in HANDOFF_NOTES.md.
- Rule and fee content is PLACEHOLDER until verified.
- Synthetic, public, or mock data only. Synthetic images must be clearly marked "SYNTHETIC" with clear fake ID patterns.
- Deliverables:
  1. Script generating 4 fake ID/certificate PNGs in data/samples/ using Pillow. Two images share a person's name but differ in DOB. Save expected extracted fields as JSON for each image.
  2. Implement compare_documents(docs: list[dict]) in compare.py in plain Python: normalise dates in multiple formats, fuzzy-match names, return factual mismatches in format {"mismatches": [{"field", "doc_a", "value_a", "doc_b", "value_b"}]}, no judgmental words like "rejected" or "invalid".
  3. Unit tests in tests/ for compare_documents covering mismatched and matching pairs. Verify tests pass.

Maintain your own BRIEFING.md and progress.md in e:\hackthon\.agents\teamwork\orchestrator_2.
When finished, notify Sentinel with completion report.
