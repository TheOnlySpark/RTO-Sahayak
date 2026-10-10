## 2026-10-10T07:39:55Z
You are m2_explorer_2 (Role: Comparison Algorithm Explorer).
Your assigned working directory is: e:\hackthon\.agents\teamwork\m2_explorer_2

Read the authoritative user request at:
e:\hackthon\.agents\teamwork\ORIGINAL_REQUEST.md (specifically the latest request timestamped 2026-10-10T07:36:23Z).
Also review the orchestrator plan at:
e:\hackthon\.agents\teamwork\orchestrator_2\plan.md

Constraints:
- You are strictly READ-ONLY. Do NOT write or modify any code files. Write only to your working directory.
- Laptop 2 owns: data/, compare.py, pdf_tools.py, tests/.
- Strictly NEVER edit: app.py, agent.py, guardrail.py, tools.py.
- Rule and fee content is PLACEHOLDER until verified.
- Must use plain Python (standard library only for compare.py: e.g. re, datetime, difflib).

Your tasks:
1. Analyze the requirements for compare_documents(docs: list[dict]) in compare.py:
   - docs: list of dictionaries representing extracted fields from documents (e.g., {"name": ..., "dob": ..., "doc_type": ...} or similar).
   - normalise dates in multiple formats (e.g. DD/MM/YYYY, YYYY-MM-DD, DD-MM-YYYY, DD/MM/YY, Month DD, YYYY, etc. -> ISO YYYY-MM-DD).
   - fuzzy-match names (e.g. handling whitespace, case, honorifics like Mr/Ms, minor typos/Levenshtein/difflib ratio threshold, initials vs full name).
   - return factual mismatches in the exact format:
     {"mismatches": [{"field": ..., "doc_a": ..., "value_a": ..., "doc_b": ..., "value_b": ...}]}
   - Strictly NO judgmental words like "rejected", "invalid", "fake", "forged", "fraudulent", etc. Only factual comparison!
   - What fields should be compared when multiple docs are passed (pairwise or all pairs)?
2. Propose a robust, clean, student-explainable plain Python design and algorithm for compare.py.
3. Design test strategy for matching and mismatched pairs to be implemented in tests/test_compare.py.

Output:
Write a comprehensive report to e:\hackthon\.agents\teamwork\m2_explorer_2\handoff.md.
Include exact specifications, date regexes/parsing logic, fuzzy comparison threshold, and code structure recommendations.
When done, send a message back to caller (parent) using send_message with your completion summary.
