## 2026-10-10T09:32:38Z

You are m2_r3_worker_1 (Role: Milestone 2 Final Remediation Worker).
Your assigned working directory is: e:\hackthon\.agents\teamwork\m2_r3_worker_1

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Read the authoritative user request at:
e:\hackthon\.agents\teamwork\ORIGINAL_REQUEST.md (specifically the latest request timestamped 2026-10-10T07:36:23Z).
Also review the critical forensic audit report at:
e:\hackthon\.agents\teamwork\m2_r2_auditor_1\handoff.md
And the gate status at:
e:\hackthon\.agents\teamwork\orchestrator_2\GATE_STATUS.md
And orchestrator handoff at:
e:\hackthon\.agents\teamwork\orchestrator_2\handoff.md

File Ownership & Boundaries:
- You OWN: data/, compare.py, pdf_tools.py, tests/, generate_samples.py, HANDOFF_NOTES.md.
- STRICTLY NEVER EDIT: app.py, agent.py, guardrail.py, tools.py.
- You must mirror all deliverables symmetrically across e:\hackthon\ and e:\hackthon\rto-sahayak\.

The Single Critical Failure to Fix:
The 8 PNG files on disk (in e:\hackthon\data\samples/*.png and e:\hackthon\rto-sahayak\data\samples/*.png) are STILL 500-byte ASCII text files starting with `# SYNTHETIC`! The Python generator `generate_samples.py` was never executed to populate the repository with real binary images.

Your Concrete Tasks:
1. Generate the Authentic Binary PNG Files on Disk:
   - Use run_command to execute:
     `python generate_samples.py`
     with Cwd="e:\\hackthon", WaitMsBeforeAsync=10000.
   - Verify that all 4 PNG files in e:\hackthon\data\samples/ and all 4 in e:\hackthon\rto-sahayak\data\samples/ are now REAL binary PNGs:
     - File size > 15 KB (typically 20-50 KB).
     - Standard 8-byte PNG magic header: b"\x89PNG\r\n\x1a\n".
     - Openable with PIL.Image.open at (800, 500) resolution.
2. Remove Evasive Test Setup in tests/test_compare.py:
   - In both e:\hackthon\tests\test_compare.py and e:\hackthon\rto-sahayak\tests\test_compare.py:
     Remove the `try: generate_samples.ensure_samples() except Exception: pass` hook from `setUpClass`.
     `setUpClass` must NOT generate or mutate files dynamically during test runs; tests must directly test pre-existing repository assets on disk.
3. Synchronize Dual-Root Files:
   - Symmetrically copy e:\hackthon\tests\test_adversarial_compare.py to e:\hackthon\rto-sahayak\tests\test_adversarial_compare.py (ensure identical 297 lines).
   - Check if pdf_tools.py exists in rto-sahayak/ and sync to root e:\hackthon\pdf_tools.py if needed.
4. Run Tests via run_command:
   - Run: `python -m unittest tests/test_compare.py`
   - Run: `python -m unittest tests/test_adversarial_compare.py`
   - Verify that 100% of tests pass cleanly.
5. Update HANDOFF_NOTES.md in both locations and write your comprehensive handoff report to:
   e:\hackthon\.agents\teamwork\m2_r3_worker_1\handoff.md
   Send completion message to parent when done.
