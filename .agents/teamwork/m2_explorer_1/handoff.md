# Milestone 2 Exploration Report — Codebase Structure & Dependencies

**Author**: `m2_explorer_1` (Role: Codebase & Dependency Explorer)  
**Date**: 2026-10-10  
**Target Workspace**: `e:\hackthon` & `e:\hackthon\rto-sahayak`  
**Milestone**: Milestone 2 (Synthetic IDs, Document Comparison, & Unit Tests)  

---

## 1. Observation

### 1.1 Dual-Root Project Layout
Direct directory inspection (`list_dir`) reveals a two-tier directory architecture:
1. **Primary Workspace Root**: `e:\hackthon\`
   - `.agents/`
   - `.git/`, `.gitignore`
   - `HANDOFF_NOTES.md` (4,262 bytes)
   - `README.md` (15 bytes)
   - `agent.py` (4,084 bytes — Laptop 1 owned)
   - `app.py` (1,905 bytes — Laptop 1 owned)
   - `data/`
     - `fees.json` (5,217 bytes)
     - `rules/` (7 markdown files: `ll_to_dl_process.md`, `documents_checklist.md`, `fees_overview.md`, `renewal_basics.md`, `vehicle_transfer_basics.md`, `rule1.md`, `rule2.md`)
   - `guardrail.py` (636 bytes — Laptop 1 owned)
   - `requirements.txt` (40 bytes: `streamlit`, `google-genai`, `python-dotenv`)
   - `rto-sahayak/` (nested project directory)
   - `test_tools.py` (649 bytes, standard library `unittest` suite)
   - `tests/`
     - `adversarial.txt` (1,492 bytes, 15 prompts)
     - `test_basic.py` (10,672 bytes, 238 lines)
   - `tools.py` (4,736 bytes, 119 lines — Laptop 1 owned)

2. **Nested Project Directory**: `e:\hackthon\rto-sahayak\`
   - `.agents/`, `.env.example`, `.git/`, `.gitignore`
   - `HANDOFF_NOTES.md` (4,169 bytes)
   - `README.md` (15 bytes)
   - `agent.py` (3,589 bytes)
   - `app.py` (1,223 bytes)
   - `compare.py` (0 bytes, empty stub file)
   - `data/`
     - `fees.json` (5,147 bytes)
     - `open/` (`SOURCES.md`, `licences.csv`)
     - `rules/` (7 markdown files)
     - `samples/` (Directory exists, 0 children / completely empty)
   - `guardrail.py` (636 bytes)
   - `outputs/` (Directory exists)
   - `pdf_tools.py` (0 bytes, empty stub file)
   - `requirements.txt` (40 bytes)
   - `tests/`
     - `adversarial.txt` (1,477 bytes, 15 prompts)
     - `test_basic.py` (10,435 bytes, 238 lines)
   - `tools.py` (2,006 bytes, 48 lines)

### 1.2 Status of `compare.py`
- Root path `e:\hackthon\compare.py`: **DOES NOT EXIST**.
- Nested path `e:\hackthon\rto-sahayak\compare.py`: **EXISTS BUT IS 0 BYTES** (empty file).
- No implementation or functions (`compare_documents`) currently exist in either file.

### 1.3 Status of `data/` and `data/samples/`
- Root path `e:\hackthon\data\samples`: **DOES NOT EXIST**.
- Nested path `e:\hackthon\rto-sahayak\data\samples`: **EXISTS BUT IS EMPTY** (`Empty directory`).
- `data/rules/` and `data/fees.json` are fully intact in both locations, containing all Milestone 1 deliverables.

### 1.4 Status of `tests/`
- Root path `e:\hackthon\tests/`:
  - `adversarial.txt`: 15 risky prompts, verified intact.
  - `test_basic.py`: 238 lines verifying rules, fees, checklist, schema, and fallback stubs.
- Nested path `e:\hackthon\rto-sahayak\tests/`:
  - `adversarial.txt`: 15 risky prompts, verified intact.
  - `test_basic.py`: 238 lines, verified intact.
- `tests/test_compare.py`: **DOES NOT EXIST** in either root or nested path.
- `test_tools.py` exists at root (`e:\hackthon\test_tools.py`) and uses standard library `unittest`.

### 1.5 Dependencies and Environment
- `requirements.txt` in both root and nested directories specifies:
  ```text
  streamlit
  google-genai
  python-dotenv
  ```
- Pillow (`PIL`) is not explicitly pinned in `requirements.txt`, but Pillow is a core dependency of `streamlit` (`st.image`).
- `pytest` is used by `test_basic.py` (`import pytest`, `pytest.mark.parametrize`), while `test_tools.py` uses `unittest`.
- Interactive shell command execution via `run_command` was declined by the user permission prompt. Therefore, implementations must be completely self-contained, deterministic, and dual-compatible with standard Python library (`unittest` and standard library packages).

### 1.6 `HANDOFF_NOTES.md` Coordination State
- Both `e:\hackthon\HANDOFF_NOTES.md` and `e:\hackthon\rto-sahayak\HANDOFF_NOTES.md` record:
  - Laptop 1 ownership: `app.py`, `agent.py`, `guardrail.py`, `tools.py`.
  - Laptop 2 ownership: `data/`, `compare.py`, `pdf_tools.py`, `tests/`.
  - Request from Laptop 1 to Laptop 2 to create `compare.py`, `pdf_tools.py`, `data/samples/`, and tests.
  - Milestone 1 response from Laptop 2 documenting completion of rules, fees, adversarial prompts, and basic tests.
  - Milestone 2 completion will need to be appended to `HANDOFF_NOTES.md`.

---

## 2. Logic Chain

1. **Dual-Tier Mirroring Precedent**:
   - In Milestone 1, all deliverables created by Laptop 2 (`data/rules/`, `data/fees.json`, `tests/test_basic.py`, `tests/adversarial.txt`) were duplicated across `e:\hackthon\` and `e:\hackthon\rto-sahayak\`.
   - The Orchestrator Plan (`orchestrator_2/plan.md:9`) explicitly requires: *"Target Locations: Both e:\hackthon\ and e:\hackthon\rto-sahayak\ for owned deliverables (data/samples/, compare.py, tests/)."*
   - Therefore, any new files created for Milestone 2 (`compare.py`, `data/samples/*.png`, `data/samples/*.json`, and `tests/test_compare.py`) must be placed in both `e:\hackthon\` and `e:\hackthon\rto-sahayak\`.

2. **Clean-Slate Implementation for `compare.py`**:
   - Because `compare.py` is absent at root and 0 bytes in `rto-sahayak`, the Worker does not have to refactor or preserve legacy code; it can implement `compare_documents(docs: list[dict]) -> dict` cleanly from scratch.
   - Per Requirement R2, `compare_documents` must:
     a) Accept `docs: list[dict]` representing extracted document field dictionaries.
     b) Normalize dates across formats (e.g. `DD/MM/YYYY`, `YYYY-MM-DD`, `DD-MM-YYYY`, `DD Month YYYY`, `D/M/YYYY`).
     c) Fuzzy-match names (token sorting, case/whitespace stripping, similarity threshold via `difflib.SequenceMatcher`).
     d) Output factual mismatches strictly in schema: `{"mismatches": [{"field": ..., "doc_a": ..., "value_a": ..., "doc_b": ..., "value_b": ...}]}`.
     e) Strictly avoid judgmental words (`rejected`, `invalid`, `fraud`, `fail`, `fake`).

3. **Sample Generation Architecture for `data/samples/`**:
   - `data/samples/` is empty in `rto-sahayak` and missing in root.
   - Requirement R1 requires 4 fake ID/certificate PNGs generated with Pillow, marked "SYNTHETIC", with fake ID patterns.
   - Two images must share a person's name (e.g., "Rajesh Kumar Sharma") but differ in date of birth (e.g., "15/08/1985" vs "15/08/1987").
   - Each image must have an accompanying expected JSON file (e.g., `sample_1.json`, `sample_2.json`, `sample_3.json`, `sample_4.json`) containing the ground truth extracted fields (`type`, `name`, `dob`, `address`, `masked_id`).
   - A standalone generation script (e.g., `generate_samples.py`) should be created to produce and write these 8 files into `data/samples/` in both locations.

4. **Test Architecture for `tests/test_compare.py`**:
   - Requirement R3 requires unit tests covering both a matching pair and a mismatched pair.
   - Tests must verify:
     a) Matching documents return empty mismatches `{"mismatches": []}`.
     b) Name fuzzy matches succeed for minor variations (e.g., "Rajesh Kumar" vs "Rajesh K.").
     c) Date normalization matches across formats (e.g., "15/08/1990" vs "1990-08-15").
     d) Genuine discrepancies (e.g., DOB mismatch between sample 1 and sample 2) produce structured mismatch records.
     e) Output format compliance: keys `field`, `doc_a`, `value_a`, `doc_b`, `value_b`.
     f) Zero judgmental terminology in return payloads.
   - To guarantee zero environment friction, tests should inherit from `unittest.TestCase` and include `if __name__ == '__main__': unittest.main()`, making them runnable with both `pytest` and `python -m unittest`.

---

## 3. Caveats

1. **Command Execution Restriction**:
   - Running terminal commands via `run_command` prompted for user approval and was denied.
   - The Worker and Auditors must ensure all Python scripts rely exclusively on standard libraries (`difflib`, `datetime`, `re`, `json`, `os`, `sys`, `unittest`) and standard Pillow (`PIL.Image`, `PIL.ImageDraw`), avoiding any complex binary build steps or uninstalled third-party packages.
2. **File Ownership Boundaries**:
   - Laptop 2 strictly owns: `data/`, `compare.py`, `pdf_tools.py`, `tests/`.
   - Never touch: `app.py`, `agent.py`, `guardrail.py`, `tools.py`.
   - All coordination requests must be documented in `HANDOFF_NOTES.md`.

---

## 4. Conclusion & Recommendations for the Worker

1. **Files to Create & Locations**:
   - `compare.py`: Implement `compare_documents` in both `e:\hackthon\compare.py` and `e:\hackthon\rto-sahayak\compare.py`.
   - `data/samples/`: Create directory in `e:\hackthon\data\samples\` and populate both root and `e:\hackthon\rto-sahayak\data\samples\` with:
     - 4 synthetic PNG images: `sample_dl_1.png`, `sample_aadhaar_2.png`, `sample_voter_3.png`, `sample_passport_4.png` (or similar).
     - 4 corresponding JSON files: `sample_dl_1.json`, `sample_aadhaar_2.json`, `sample_voter_3.json`, `sample_passport_4.json`.
   - `tests/test_compare.py`: Create in both `e:\hackthon\tests\test_compare.py` and `e:\hackthon\rto-sahayak\tests\test_compare.py`.
   - `HANDOFF_NOTES.md`: Append Milestone 2 handoff report to both `e:\hackthon\HANDOFF_NOTES.md` and `e:\hackthon\rto-sahayak\HANDOFF_NOTES.md`.

2. **Design Specifications for Implementation**:
   - **`compare_documents`**:
     - Input: `docs: list[dict]`
     - Output: `{"mismatches": [{"field": str, "doc_a": str, "value_a": Any, "doc_b": str, "value_b": Any}]}`
     - Date parser: Normalize standard formats (`%Y-%m-%d`, `%d/%m/%Y`, `%d-%m-%Y`, `%d %b %Y`, `%d %B %Y`) to canonical `YYYY-MM-DD`.
     - Name parser: Clean whitespace, lowercase, remove punctuation, compute `difflib.SequenceMatcher(None, name1, name2).ratio()` with threshold >= 0.85 (or token matching).
     - Non-judgmental vocabulary: Label mismatches strictly as differences, never as "rejected", "invalid", or "fraud".
   - **Synthetic Samples**:
     - Clear red/yellow banner: `"SYNTHETIC - FOR TESTING ONLY"`.
     - Fictional identifiers: `"FAKE-DL-2024-001"`, `"FAKE-AADHAAR-9999-8888-7777"`, etc.
     - Pair sharing name but differing DOB: e.g., Doc 1 DOB `"1990-05-15"`, Doc 2 DOB `"1992-05-15"` with identical name `"Sunil Verma"`.

---

## 5. Verification Method

1. **Static & AST Code Inspection**:
   - View `compare.py` and verify `compare_documents` function definition, arguments, return dictionary structure, and absence of prohibited strings (`"reject"`, `"invalid"`, `"fraud"`).
   - View `tests/test_compare.py` and verify test classes covering matching documents, mismatched documents, date normalization, and fuzzy name matching.
2. **File Existence Check**:
   - Inspect `data/samples/` in both root and rto-sahayak: verify 4 `.png` files and 4 `.json` files exist with non-zero file sizes.
3. **Execution Commands**:
   ```bash
   python -m unittest tests/test_compare.py
   pytest tests/test_compare.py -v
   pytest tests/test_basic.py -v
   ```
