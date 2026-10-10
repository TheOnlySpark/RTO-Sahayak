## 2026-10-10T06:20:13Z
You are Worker 1 (Implementation Worker) for RTO Sahayak Milestone 1.
Your working directory is e:\hackthon\.agents\teamwork\worker_impl_1.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

MANDATORY: Read the original user request at e:\hackthon\.agents\teamwork\ORIGINAL_REQUEST.md.
Also read the explorer reports:
- e:\hackthon\.agents\teamwork\explorer_survey_1\handoff.md
- e:\hackthon\.agents\teamwork\explorer_survey_2\handoff.md
- e:\hackthon\.agents\teamwork\explorer_survey_3\handoff.md

Your Task:
1. Implement Requirement R1 (Data Rules):
   Create the 5 markdown files in data/rules/:
   - ll_to_dl_process.md
   - documents_checklist.md
   - fees_overview.md
   - renewal_basics.md
   - vehicle_transfer_basics.md
   Each file MUST:
   - Be under 40 lines.
   - Start line 1 with "Source: TODO" (e.g. "Source: TODO (Parivahan Sarathi Guidelines)").
   - End with "PLACEHOLDER: verify against official sources".
   - Include: "Final decision rests with the RTO officer."

2. Implement Requirement R2 (Fees Data):
   Create data/fees.json:
   - Valid JSON covering services: learner_license, driving_license, renewal, vehicle_transfer, duplicate_license across vehicle classes: MCWOG, MCWG, LMV, LMV-NT, TRANS.
   - Every service and rate entry must include "source" and "PLACEHOLDER" tags.
   - Include metadata disclaimer: "Final decision rests with the RTO officer."

3. Implement Requirement R3 (Adversarial Prompts & Basic Unit Tests):
   - Create tests/adversarial.txt: Exactly 15 risky prompts testing eligibility claims, legal guarantees, official impersonation, etc. (1 per line).
   - Create tests/test_basic.py: Unit tests for lookup_rules, calc_fees, and build_checklist.
     Important constraint: Laptop 2 owns tests/, data/, compare.py, pdf_tools.py, but CANNOT edit tools.py, app.py, agent.py, guardrail.py. tools.py is currently 0 bytes.
     Therefore, tests/test_basic.py should attempt to import lookup_rules, calc_fees, build_checklist from tools, but provide clean fallback stubs that read the real data/rules/*.md and data/fees.json if tools.py is not yet implemented, ensuring pytest runs cleanly and passes.
     Tests must verify:
     - All 5 rule files exist, are < 40 lines, start with "Source: TODO", end with "PLACEHOLDER", and contain "Final decision rests with the RTO officer."
     - calc_fees calculates fees for all services and classes, checks "source" and "PLACEHOLDER", and raises KeyError on invalid input.
     - build_checklist produces valid checklist structure with disclaimers.
     - tests/adversarial.txt exists and has exactly 15 prompts.

4. Update HANDOFF_NOTES.md:
   - Document the interface request for Laptop 1 (Person 1, owner of tools.py) specifying the expected functions: lookup_rules(topic), calc_fees(service, vehicle_class), build_checklist(service).

5. Directory Mirroring:
   - Create all data files in both e:\hackthon\data and e:\hackthon\rto-sahayak\data.
   - Create all test files in both e:\hackthon\tests and e:\hackthon\rto-sahayak\tests.
   - Ensure HANDOFF_NOTES.md is updated in both e:\hackthon\HANDOFF_NOTES.md and e:\hackthon\rto-sahayak\HANDOFF_NOTES.md.
   - Strictly DO NOT touch app.py, agent.py, guardrail.py, tools.py.

6. Verification:
   - Run tests with pytest (e.g. pytest tests/test_basic.py -v) from both e:\hackthon and e:\hackthon\rto-sahayak.
   - Verify all tests pass with 0 failures.
   - Verify line counts of all rule markdown files (< 40 lines).
   - Verify line count of tests/adversarial.txt (exactly 15 lines).
   - Verify data/fees.json is valid JSON.

7. Reporting:
   - Write your complete handoff report in e:\hackthon\.agents\teamwork\worker_impl_1\handoff.md detailing:
     - Exact files created and modified.
     - Build/test execution commands and full output.
     - Adherence to all rules and invariants.
   - Send a message to orchestrator upon completion.
