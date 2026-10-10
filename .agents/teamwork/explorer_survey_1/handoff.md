# Explorer 1 Survey Handoff Report: Codebase Interface & Schema Analysis

## 1. Observation

Direct observations made during filesystem inspection of `e:\hackthon` and `e:\hackthon\rto-sahayak`:

### Codebase Inventory & File States
- **`e:\hackthon\rto-sahayak\tools.py`**:
  - Size: 0 bytes (1 empty line).
  - Content: Completely empty.
  - Functions `lookup_rules`, `calc_fees`, and `build_checklist` are currently **unimplemented** (0 definitions found via `grep_search`).
- **`e:\hackthon\rto-sahayak\app.py`**: 0 bytes (empty scaffold).
- **`e:\hackthon\rto-sahayak\agent.py`**: 0 bytes (empty scaffold).
- **`e:\hackthon\rto-sahayak\guardrail.py`**: 0 bytes (empty scaffold).
- **`e:\hackthon\rto-sahayak\compare.py`**: 0 bytes (empty scaffold).
- **`e:\hackthon\rto-sahayak\pdf_tools.py`**: 0 bytes (empty scaffold).
- **`e:\hackthon\rto-sahayak\requirements.txt`**: 0 bytes (empty scaffold).
- **`e:\hackthon\rto-sahayak\HANDOFF_NOTES.md`**: 0 bytes (empty scaffold).
- **`e:\hackthon\rto-sahayak\README.md`**: 0 bytes (empty scaffold).
- **`e:\hackthon\rto-sahayak\data\fees.json`**: 0 bytes (empty scaffold).
- **`e:\hackthon\rto-sahayak\data\rules/`**: Directory exists, currently contains 0 files.
- **`e:\hackthon\rto-sahayak\data\open/`** & **`samples/`**: Directories exist, currently contain 0 files.
- **`e:\hackthon\rto-sahayak\tests/`**: Directory exists, currently contains 0 files.
- **Root `e:\hackthon` directory**:
  - Contains `.agents/`, `.git/`, and `rto-sahayak/`.
  - Currently does not contain top-level `data/` or `tests/` directories.

### Rules and File Ownership Constraints
- Quoted verbatim from `USER_RULES` and `.agents/rules/project.md`:
  > "This machine is LAPTOP 2 for RTO Sahayak. I OWN: data/, compare.py, pdf_tools.py, tests/."
  > "I never edit: app.py, agent.py, guardrail.py, tools.py. Requests go in HANDOFF_NOTES.md."
  > "Rule and fee content is PLACEHOLDER until Person 3 verifies it; never invent official figures."
  > "Respect file ownership. If you need a change in a file you don't own, write it in HANDOFF_NOTES.md and use a stub."
  > "Every rule explanation cites its source file and ends with: 'Final decision rests with the RTO officer.'"
  > "Handoff PDFs carry the banner: 'DRAFT - for citizen review and officer verification'."

---

## 2. Logic Chain

1. **Premise 1 (Ownership Boundary)**:
   Laptop 2 owns `data/`, `compare.py`, `pdf_tools.py`, and `tests/`. Laptop 2 is strictly forbidden from writing or modifying `tools.py`, `app.py`, `agent.py`, or `guardrail.py`.
2. **Premise 2 (Empty Scaffold State)**:
   Because `tools.py` is currently 0 bytes, there is no legacy code or existing signature to be backward-compatible with inside `tools.py`.
3. **Premise 3 (Requirement Fulfillment & Decoupling)**:
   - Requirement R1 mandates creating 5 markdown rule files in `data/rules/` (`ll_to_dl_process.md`, `documents_checklist.md`, `fees_overview.md`, `renewal_basics.md`, `vehicle_transfer_basics.md`), each under 40 lines, starting with `Source: TODO` and ending with `PLACEHOLDER: verify against official sources`.
   - Requirement R2 mandates creating `data/fees.json` with placeholder fees by service and vehicle class, each including `"source"` and `"PLACEHOLDER"`.
   - Requirement R3 mandates `tests/test_basic.py` with unit tests for `lookup_rules`, `calc_fees`, and `build_checklist`.
4. **Deduction (Interface & Contract Definition)**:
   Because Laptop 2 cannot edit `tools.py`, but must deliver `test_basic.py` that tests `lookup_rules`, `calc_fees`, and `build_checklist`:
   - Laptop 2 must define the exact contract, arguments, return formats, and file-path resolutions for `tools.py`.
   - This specification must be recorded in `HANDOFF_NOTES.md` for Laptop 1 (Person 1) to implement in `tools.py`.
   - In `tests/test_basic.py`, the test suite should implement or import the functions cleanly (e.g. attempting to import from `tools`, and providing reference stub implementations or testing stub functions that read the real `data/rules/*.md` and `data/fees.json` if `tools.py` is not yet populated), ensuring `pytest` runs and passes completely without violating the rule never to edit `tools.py`.
5. **Deduction (Path Resolution)**:
   Because the repository has both `e:\hackthon\` and `e:\hackthon\rto-sahayak\`, file loaders and tests must support data files located in either directory, or files should be populated in both paths (`e:\hackthon\data` and `e:\hackthon\rto-sahayak\data`) as outlined in the orchestration plan.

---

## 3. Interface & Schema Specification

### 3.1 `lookup_rules(topic: str) -> dict | str`
- **Purpose**: Reads rule documentation from `data/rules/{topic}.md`.
- **Arguments**:
  - `topic` (`str`): Name or key of the topic. Expected supported keys:
    - `"ll_to_dl_process"`
    - `"documents_checklist"`
    - `"fees_overview"`
    - `"renewal_basics"`
    - `"vehicle_transfer_basics"`
- **Path Resolution**: Looks up `data/rules/{topic}.md` (case-insensitive, normalizing spaces/dashes to underscores). Checks both `./data/rules/{topic}.md` and `./rto-sahayak/data/rules/{topic}.md`.
- **Return Format**:
  - String of markdown text containing the rule content, OR
  - Dict:
    ```python
    {
        "topic": topic,
        "content": markdown_text,
        "source": "Source: TODO",
        "placeholder": True,
        "disclaimer": "Final decision rests with the RTO officer."
    }
    ```
- **Error Handling**: Raises `FileNotFoundError` or returns error indicator if topic is unknown.

### 3.2 `calc_fees(service: str, vehicle_class: str) -> dict | float | int`
- **Purpose**: Calculates/looks up official placeholder fee from `data/fees.json`.
- **Arguments**:
  - `service` (`str`): Target service, e.g. `"learner_license"`, `"driving_license"`, `"renewal"`, `"vehicle_transfer"`.
  - `vehicle_class` (`str`): Vehicle category, e.g. `"MCWG"`, `"MCWOG"`, `"LMV"`, `"TRANS"`.
- **Path Resolution**: Looks up `data/fees.json` or `rto-sahayak/data/fees.json`.
- **JSON Schema in `data/fees.json`**:
  ```json
  {
    "version": "1.0-PLACEHOLDER",
    "disclaimer": "PLACEHOLDER: verify against official sources. Final decision rests with the RTO officer.",
    "services": {
      "learner_license": {
        "MCWG": { "application_fee": 150, "test_fee": 50, "total": 200, "source": "PLACEHOLDER: Ministry of Road Transport & Highways", "status": "PLACEHOLDER" },
        "MCWOG": { "application_fee": 150, "test_fee": 50, "total": 200, "source": "PLACEHOLDER: Ministry of Road Transport & Highways", "status": "PLACEHOLDER" },
        "LMV": { "application_fee": 150, "test_fee": 50, "total": 200, "source": "PLACEHOLDER: Ministry of Road Transport & Highways", "status": "PLACEHOLDER" }
      },
      "driving_license": {
        "MCWG": { "application_fee": 200, "test_fee": 300, "total": 500, "source": "PLACEHOLDER: Central Motor Vehicles Rules", "status": "PLACEHOLDER" },
        "LMV": { "application_fee": 200, "test_fee": 300, "total": 500, "source": "PLACEHOLDER: Central Motor Vehicles Rules", "status": "PLACEHOLDER" },
        "TRANS": { "application_fee": 200, "test_fee": 300, "total": 500, "source": "PLACEHOLDER: Central Motor Vehicles Rules", "status": "PLACEHOLDER" }
      },
      "renewal": {
        "MCWG": { "application_fee": 200, "test_fee": 0, "total": 200, "source": "PLACEHOLDER: Central Motor Vehicles Rules", "status": "PLACEHOLDER" },
        "LMV": { "application_fee": 200, "test_fee": 0, "total": 200, "source": "PLACEHOLDER: Central Motor Vehicles Rules", "status": "PLACEHOLDER" }
      },
      "vehicle_transfer": {
        "MCWG": { "application_fee": 150, "test_fee": 0, "total": 150, "source": "PLACEHOLDER: Central Motor Vehicles Rules", "status": "PLACEHOLDER" },
        "LMV": { "application_fee": 300, "test_fee": 0, "total": 300, "source": "PLACEHOLDER: Central Motor Vehicles Rules", "status": "PLACEHOLDER" }
      }
    }
  }
  ```
- **Return Format**:
  - Dict returning fee breakdown:
    ```python
    {
        "service": service,
        "vehicle_class": vehicle_class,
        "application_fee": 200,
        "test_fee": 300,
        "total": 500,
        "source": "PLACEHOLDER: Central Motor Vehicles Rules",
        "placeholder": True
    }
    ```
- **Error Handling**: Raises `KeyError` or returns `None` for unsupported service/class combinations.

### 3.3 `build_checklist(service_or_topic: str) -> list[str] | dict`
- **Purpose**: Generates document checklist for a given citizen service request.
- **Arguments**:
  - `service_or_topic` (`str`): Target service/topic, e.g. `"documents_checklist"`, `"ll_to_dl_process"`, `"renewal_basics"`, `"vehicle_transfer_basics"`.
- **Path Resolution**: Reads `data/rules/documents_checklist.md` or the matching service markdown file.
- **Return Format**:
  - A structured list of document requirements, e.g.:
    ```python
    [
        "Application Form (Form 2 for DL / Form 9 for Renewal / Form 29 & 30 for Transfer)",
        "Proof of Age (Aadhaar / Birth Certificate / Passport / School Certificate - SYNTHETIC)",
        "Proof of Address (Aadhaar / Utility Bill / Voter ID - SYNTHETIC)",
        "Learner's License copy (if applying for permanent DL)",
        "Passport size photographs",
        "Medical Certificate (Form 1A, if applicant age > 40 or commercial)"
    ]
    ```
- **Constraint**: Must adhere to synthetic/mock labeling rule (`SYNTHETIC`) and state "Final decision rests with the RTO officer."

---

## 4. Caveats

1. **Current Code State**: All Python source files in `rto-sahayak` (`tools.py`, `agent.py`, `app.py`, `guardrail.py`, `compare.py`, `pdf_tools.py`) are currently empty (0 bytes). No existing implementations were found.
2. **Laptop 2 Boundary**: Laptop 2 cannot write into `tools.py`. Therefore, `tests/test_basic.py` must be designed so that it can either import functions from `tools` if Laptop 1 implements them, or test the reference functions/data parser stubs without failing if `tools.py` remains empty during Milestone 1-2.
3. **No Assumptions on Other Branches**: We inspected local filesystem state. No git network access was performed.

---

## 5. Conclusion

1. **tools.py**: Empty (0 bytes). Needs interface specification handed off to Person 1 via `HANDOFF_NOTES.md`.
2. **Consuming modules**: `compare.py` and `pdf_tools.py` (owned by Laptop 2) can now be designed against the defined data contracts for `data/rules/*.md` and `data/fees.json`.
3. **Data Schema & Rules**: All 5 markdown files must strictly adhere to the <40 lines limit, start with `Source: TODO`, end with `PLACEHOLDER: verify against official sources`, and include the required disclaimer: `Final decision rests with the RTO officer.`.
4. **Fees Data**: `data/fees.json` must provide structured breakdown per service and vehicle class, with `"source"` and `"PLACEHOLDER"` tags in every entry.
5. **Dual Directory Placement**: Because tests and scripts may be executed from either `e:\hackthon\` or `e:\hackthon\rto-sahayak\`, creating `data/` and `tests/` in both locations ensures seamless testing and tool resolution.

---

## 6. Verification Method

To independently verify these findings:
1. **File status check**:
   - `view_file` on `e:\hackthon\rto-sahayak\tools.py` confirms 0 bytes.
   - `list_dir` on `e:\hackthon\rto-sahayak\data\rules` confirms empty directory.
   - `view_file` on `e:\hackthon\rto-sahayak\data\fees.json` confirms 0 bytes.
2. **Interface contract validation**:
   - Verify that all 5 files in `data/rules/` comply with `< 40` lines and exact header/footer patterns.
   - Verify that `data/fees.json` parses as valid JSON with `source` and `PLACEHOLDER` fields.
   - Verify that `pytest` executed against `tests/test_basic.py` imports and validates `lookup_rules`, `calc_fees`, and `build_checklist` against the generated data.
