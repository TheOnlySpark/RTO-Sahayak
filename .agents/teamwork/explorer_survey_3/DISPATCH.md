## 2026-10-10T06:04:31Z
You are Explorer 3 (Requirements & Constraints Explorer) for RTO Sahayak.
Your working directory is e:\hackthon\.agents\teamwork\explorer_survey_3.
MANDATORY: Read the original request at e:\hackthon\.agents\teamwork\ORIGINAL_REQUEST.md before starting work.
Your task:
1. Carefully analyze requirements R1, R2, R3 in ORIGINAL_REQUEST.md alongside the Laptop 2 rules:
   - R1: markdown files in data/rules/ for ll_to_dl_process, documents_checklist, fees_overview, renewal_basics, vehicle_transfer_basics. Each under 40 lines, starts with 'Source: TODO', ends with 'PLACEHOLDER: verify against official sources'. Rule explanations ending with: 'Final decision rests with the RTO officer.'
   - R2: data/fees.json with placeholder fees by service and vehicle class, each including a 'source' field and 'PLACEHOLDER'.
   - R3: tests/adversarial.txt with 15 risky prompts testing eligibility claims. tests/test_basic.py with unit tests for lookup_rules, calc_fees, and build_checklist.
2. Verify all constraints: file ownership (Laptop 2 owns data/, compare.py, pdf_tools.py, tests/; NEVER edit app.py, agent.py, guardrail.py, tools.py).
3. Design the exact schema, test assertions, and adversarial prompts required so that workers have zero ambiguity.
4. Record your detailed findings in e:\hackthon\.agents\teamwork\explorer_survey_3\handoff.md.
5. Send a message to orchestrator with your completion and summary.
