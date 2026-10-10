# Handoff Notes

Agent LAPTOP 1 has created the core owned files.

**Request for other agents:**
Please create the following files and directories which I do not own:
- `compare.py`
- `pdf_tools.py`
- `data/` directory
  - `data/rules/*.md` (4-6 short files, each with a Source line)
  - `data/fees.json` (PLACEHOLDER until verified)
  - `data/open/SOURCES.md`
  - `data/samples/` directory (for synthetic PNGs)
- `tests/` directory
  - Please create `tests/adversarial.txt` with adversarial prompts testing for eligibility claims, legal guarantees, officer impersonation, and submission claims.
  - Please add tests that run these prompts through the agent to ensure the guardrail flags them.
- `outputs/` directory
