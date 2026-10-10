# Victory Auditor Context

- Target: Independent victory audit of RTO Sahayak requirements R1, R2, R3 (Laptop 2)
- ORIGINAL_REQUEST.md: e:\hackthon\.agents\teamwork\ORIGINAL_REQUEST.md
- Working Directory: e:\hackthon\.agents\teamwork\victory_auditor_1
- Orchestrator Working Directory: e:\hackthon\.agents\teamwork\orchestrator_1
- Project Root: e:\hackthon
- Subproject Root: e:\hackthon\rto-sahayak
- Constraints:
  - Laptop 2 owns: data/, compare.py, pdf_tools.py, tests/.
  - Never edit: app.py, agent.py, guardrail.py, tools.py.
  - Verify line counts (< 40), headers ("Source: TODO"), footers ("PLACEHOLDER: verify against official sources", officer disclaimer).
  - Verify data/fees.json, tests/adversarial.txt (15 prompts), and tests/test_basic.py.
  - Verify no cheating, no unowned file edits, and independent test execution.
