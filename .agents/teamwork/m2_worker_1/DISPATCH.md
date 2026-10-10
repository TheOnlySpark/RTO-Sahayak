## 2026-10-10T07:48:15Z
You are m2_worker_1 (Role: Implementation Worker for Milestone 2).
Your assigned working directory is: e:\hackthon\.agents\teamwork\m2_worker_1

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Read the authoritative user request at:
e:\hackthon\.agents\teamwork\ORIGINAL_REQUEST.md (specifically the latest request timestamped 2026-10-10T07:36:23Z).
Also review the explorer handoffs:
- e:\hackthon\.agents\teamwork\m2_explorer_1\handoff.md
- e:\hackthon\.agents\teamwork\m2_explorer_2\handoff.md
- e:\hackthon\.agents\teamwork\m2_explorer_3\handoff.md
Also review orchestrator plan at e:\hackthon\.agents\teamwork\orchestrator_2\plan.md.

File Ownership & Boundaries:
- You OWN: data/samples/, compare.py, tests/test_compare.py, HANDOFF_NOTES.md, and optional data generation script.
- You must create / mirror deliverables in both e:\hackthon\ and e:\hackthon\rto-sahayak\ (e.g. data/samples/, compare.py, tests/test_compare.py).
- STRICTLY NEVER EDIT: app.py, agent.py, guardrail.py, tools.py. Requests for other laptops go in HANDOFF_NOTES.md.
- Rule and fee content is PLACEHOLDER until verified.
- Synthetic, public, or mock data only. Synthetic images must be clearly marked "SYNTHETIC" with clear fake ID patterns.

Tasks to implement:
1. R1: Synthetic Images & JSONs
   - Create a generation script (e.g. generate_samples.py or in data/samples/generator.py) using Pillow.
   - Run it to generate 4 fake ID/certificate PNGs in data/samples/ (and rto-sahayak/data/samples/):
     - Each clearly marked "SYNTHETIC" and "DRAFT - for citizen review and officer verification" with clear fake ID numbers (e.g. FAKE-DL-..., FAKE-AADHAAR-...).
     - Document 1 & Document 2: Mismatched pair sharing person name ("Rahul Kumar Sharma") but differing in DOB ("1995-05-15" vs "1993-05-15").
     - Document 3 & Document 4: Matching pair ("Priya S. Patel" vs "Priya Sanjay Patel", matching DOB with varied formatting).
   - Save the expected extracted fields as a JSON file for each image in data/samples/ (e.g. doc1_driving_licence.json, doc2_aadhaar_card.json, doc3_pan_card.json, doc4_voter_id.json) and mirror to rto-sahayak/data/samples/.
   - Verify that all 4 PNG files and 4 JSON files actually exist and are non-empty!

2. R2: Document Comparison Script in compare.py
   - Implement compare_documents(docs: list[dict]) in compare.py (and mirror to rto-sahayak/compare.py) in plain Python stdlib.
   - Multi-format date normalization (ISO YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY, 2-digit years, textual month names like "15 May 1995", ordinal suffixes).
   - Fuzzy name matching (handles case, whitespace, Indian honorifics Mr/Mrs/Ms/Shri/Smt/Dr, initials like "Priya S. Patel" vs "Priya Sanjay Patel", difflib.SequenceMatcher for minor typos).
   - Return factual mismatches in exact format:
     {"mismatches": [{"field": ..., "doc_a": ..., "value_a": ..., "doc_b": ..., "value_b": ...}]}
   - Strictly NO judgmental words anywhere in code, docstrings, or return values (no "rejected", "invalid", "fake", "forged", "fraudulent", etc.).
   - Handle empty list, single document (0 mismatches), and multiple documents (pairwise comparison of identity fields).

3. R3: Unit Tests in tests/test_compare.py
   - Implement comprehensive unit tests in tests/test_compare.py (and mirror to rto-sahayak/tests/test_compare.py).
   - Tests must cover:
     - Date normalization with various formats.
     - Fuzzy name matching (identical names, initials, minor typos, differing names).
     - Empty doc list, single doc, matching document pair (0 mismatches).
     - Mismatched document pair (e.g. doc1 vs doc2 DOB mismatch).
     - The 4 synthetic sample JSONs loaded directly from data/samples/.
     - Non-judgmental vocabulary assertion (verifying returned mismatch dictionaries contain no forbidden words).
   - Run the tests using pytest and/or python -m unittest and ensure all tests PASS.

4. Documentation & Verification:
   - Run tests and record the exact execution command and output.
   - Update HANDOFF_NOTES.md with any notes for other laptops (e.g. Laptop 1 / Person 3).
   - Write your handoff report to e:\hackthon\.agents\teamwork\m2_worker_1\handoff.md with Observation, Logic Chain, Caveats, Conclusion, and Verification Method with passing test output.
   - Send completion message to parent when done.
