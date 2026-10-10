## 2026-10-10T09:09:37Z
You are m2_worker_2 (Role: Milestone 2 Remediation Worker).
Your assigned working directory is: e:\hackthon\.agents\teamwork\m2_worker_2

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Read the authoritative user request at:
e:\hackthon\.agents\teamwork\ORIGINAL_REQUEST.md (specifically the latest request timestamped 2026-10-10T07:36:23Z).
Also review the remediation reports:
- e:\hackthon\.agents\teamwork\m2_r2_explorer_1\handoff.md
- e:\hackthon\.agents\teamwork\m2_r2_explorer_2\handoff.md
- e:\hackthon\.agents\teamwork\m2_r2_explorer_3\handoff.md
- e:\hackthon\.agents\teamwork\orchestrator_2\GATE_STATUS.md
- e:\hackthon\.agents\teamwork\m2_auditor_1\handoff.md

File Ownership & Boundaries:
- You OWN: compare.py, generate_samples.py, data/samples/, tests/test_compare.py, HANDOFF_NOTES.md.
- You MUST mirror all changes across both e:\hackthon\ and e:\hackthon\rto-sahayak\.
- STRICTLY NEVER EDIT: app.py, agent.py, guardrail.py, tools.py.

Remediation Tasks to Execute:
1. Fix compare.py (both e:\hackthon\compare.py and e:\hackthon\rto-sahayak\compare.py):
   - In METADATA_FIELDS, add document lifecycle and validity metadata: "issue_date", "issued_date", "date_of_issue", "doi", "expiry_date", "expiration_date", "valid_till", "valid_upto", "valid_until", "validity", "valid_from", "issuance_date".
   - In compare_documents, normalize field keys (re.sub(r'[\s\-]+', '_', k.strip().lower())) so metadata exclusion is delimiter- and case-insensitive.
   - In are_names_matching, add token multiset comparison (if sorted(tokens_a) == sorted(tokens_b): return True) to handle inverted name orderings like "Patel Priya" vs "Priya Patel".
   - Maintain zero judgmental vocabulary.

2. Fix generate_samples.py (both e:\hackthon\generate_samples.py and e:\hackthon\rto-sahayak\generate_samples.py):
   - Ensure the script provides an ensure_samples(target_dir=None) function.
   - Update generate_all_samples() to write authentic Pillow-rendered 800x500 binary PNGs and JSONs to both e:\hackthon\data\samples\ and e:\hackthon\rto-sahayak\data\samples\.
   - Make sure binary PNGs actually get created with standard PNG magic bytes (b"\x89PNG\r\n\x1a\n") and non-trivial file size (> 15KB).

3. Fix tests/test_compare.py (both e:\hackthon\tests\test_compare.py and e:\hackthon\rto-sahayak\tests\test_compare.py):
   - In setUpClass, import and call ensure_samples() so authentic binary PNGs are auto-generated if missing or invalid.
   - Replace the evasive test assertion in test_samples_exist_and_are_non_empty with rigorous validation:
     a) Verify 8-byte PNG magic signature (b"\x89PNG\r\n\x1a\n").
     b) Open each file with PIL.Image.open: assert img.format == "PNG", assert img.size == (800, 500), assert img.load() succeeds.
     c) Assert file size is genuine (> 1024 bytes).
   - Add test_lifecycle_dates_ignored_in_comparison to verify that differing issue_date between matching documents does not produce false mismatches.

4. Execute & Verify:
   - Ensure authentic binary PNG files are written to both data/samples/ directories.
   - Run the test suite (python -m unittest tests/test_compare.py and pytest) and ensure 100% of tests pass.
   - Run tests/test_adversarial_compare.py as well.

5. Update HANDOFF_NOTES.md and write your handoff report to e:\hackthon\.agents\teamwork\m2_worker_2\handoff.md.
   - Send completion message to parent when done.
