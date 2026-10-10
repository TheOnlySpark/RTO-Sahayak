# Adversarial Challenge Report — Milestone 2 Verification

## Challenge Summary

**Overall risk assessment**: CRITICAL
**Final Verdict**: **REQUEST_CHANGES**

Empirical verification of Milestone 2 synthetic sample documents and comparison logic revealed two critical defects:
1. All 4 PNG files in both `data/samples/` and `rto-sahayak/data/samples/` are invalid plain text files containing ASCII comments, not binary PNG images. They cannot be opened with Pillow and lack valid dimensions.
2. In `compare.py` (both root and `rto-sahayak`), `METADATA_FIELDS` omits `"issue_date"` and `"expiry_date"`. This causes `compare_documents` to compare issue dates across documents, flagging false mismatches on the matching sample pair (`doc3` vs `doc4`) and adding an unintended second mismatch to `doc1` vs `doc2`, breaking the test suite assertions in `tests/test_compare.py`.

---

## 1. Observation

### Observation 1: Sample PNG Files Are Plain Text, Not Binary PNG Images
Direct file inspection of all 4 `.png` files in `data/samples/` and `rto-sahayak/data/samples/` reveals:
- File sizes:
  - `doc1_driving_licence.png`: 574 bytes
  - `doc2_aadhaar_card.png`: 530 bytes
  - `doc3_pan_card.png`: 528 bytes
  - `doc4_voter_id.png`: 545 bytes
- File content of `data/samples/doc1_driving_licence.png`:
  ```text
  1: # SYNTHETIC DOCUMENT - FOR TESTING ONLY
  2: # DRAFT - for citizen review and officer verification
  3: # Document Type: Driving Licence
  4: # Document Number: FAKE-DL-DL04-20150001
  5: # Subject: Rahul Kumar Sharma
  6: # Date of Birth: 1995-05-15
  7: # Father's Name: Suresh Kumar Sharma
  8: # Address: 123, Gandhi Marg, Synthetic City, New Delhi - 110001
  9: # Issuing Authority: RTO Synthetic Zone 04, New Delhi
  10: # Vehicle Class: LMV, MCWG
  11: # Issue Date: 2015-06-20
  12: # Expiry Date: 2035-05-14
  13: # Notice: Synthetic test record. Not an official government document.
  14: # Final decision rests with the RTO officer.
  ```
- The identical text representation is present in `doc2_aadhaar_card.png`, `doc3_pan_card.png`, `doc4_voter_id.png`, and in `rto-sahayak/data/samples/*.png`.
- A valid PNG file requires the 8-byte magic header `\x89PNG\r\n\x1a\n` (`0x89 0x50 0x4E 0x47 0x0D 0x0A 0x1A 0x0A`). These files begin with `0x23 0x20 0x53 0x59` (`# SY`).
- Running `PIL.Image.open("data/samples/doc1_driving_licence.png")` will fail with:
  `PIL.UnidentifiedImageError: cannot identify image file 'data/samples/doc1_driving_licence.png'`.
- `generate_samples.py` exists with complete Pillow generation logic (creating 800x500 images via `Image.new("RGB", (800, 500))`), but was never executed to overwrite the text placeholder files on disk.

### Observation 2: Existing PNG Test Only Checks `exists` and `size > 0`
In `tests/test_compare.py` (lines 264–267) and `rto-sahayak/tests/test_compare.py`:
```python
for fname in expected_png:
    fpath = os.path.join(self.samples_dir, fname)
    self.assertTrue(os.path.exists(fpath), f"Missing PNG sample: {fpath}")
    self.assertGreater(os.path.getsize(fpath), 0, f"Empty PNG sample: {fpath}")
```
The test suite never invokes `PIL.Image.open(fpath)` or checks image format, dimensions, or corruption.

### Observation 3: Metadata JSON Files are Valid and Conform to Persona Requirements
Direct inspection of `data/samples/*.json` and `rto-sahayak/data/samples/*.json`:
- `doc1_driving_licence.json`:
  - `full_name`: `"Rahul Kumar Sharma"`
  - `date_of_birth`: `"1995-05-15"`
  - `is_synthetic`: `true`
  - `disclaimer`: includes `"Final decision rests with the RTO officer."`
- `doc2_aadhaar_card.json`:
  - `full_name`: `"Rahul Kumar Sharma"`
  - `date_of_birth`: `"1993-05-15"` (mismatch with doc1)
  - `is_synthetic`: `true`
- `doc3_pan_card.json`:
  - `full_name`: `"Priya S. Patel"`
  - `date_of_birth`: `"1998-11-22"`
- `doc4_voter_id.json`:
  - `full_name`: `"Priya Sanjay Patel"`
  - `date_of_birth`: `"22/11/1998"` (different format matching doc3)
- Persona pairs:
  - Document 1 & 2 share full name `"Rahul Kumar Sharma"` and differ in DOB (`1995-05-15` vs `1993-05-15`).
  - Document 3 & 4 represent the same persona with name variations (`"Priya S. Patel"` vs `"Priya Sanjay Patel"`) and matching normalized DOB.

### Observation 4: `compare.py` Omits `issue_date` and `expiry_date` From `METADATA_FIELDS`
In `compare.py` (and `rto-sahayak/compare.py`), lines 58–63:
```python
METADATA_FIELDS = {
    "doc_id", "doc_type", "document_type", "document_number",
    "filename", "file_name", "id", "is_synthetic", "disclaimer",
    "bg_color", "border_color", "header_color", "issuing_authority",
    "vehicle_class", "status", "source", "type"
}
```
In lines 284–330 of `compare.py`:
- `issue_date` is not in `METADATA_FIELDS`, so it is treated as a canonical comparison field.
- Because `"date"` is in `"issue_date"` (line 315: `if canonical == "dob" or "date" in canonical:`), `compare_documents` executes `are_dates_matching(doc_a["issue_date"], doc_b["issue_date"])`.
- In `doc1` and `doc2`:
  - `doc1["issue_date"] = "2015-06-20"`
  - `doc2["issue_date"] = "2012-08-10"`
  - `compare_documents([doc1, doc2])` flags TWO mismatches: `date_of_birth` AND `issue_date`.
- In `doc3` and `doc4` (intended matching pair):
  - `doc3["issue_date"] = "2018-03-15"`
  - `doc4["issue_date"] = "2017-01-10"`
  - `compare_documents([doc3, doc4])` flags ONE mismatch: `issue_date`.
  - It does NOT return 0 mismatches.
- In `tests/test_compare.py`:
  - `test_compare_doc1_and_doc2_from_disk` (line 290): `self.assertEqual(len(mismatches), 1)` will FAIL because `len(mismatches)` is 2.
  - `test_compare_doc3_and_doc4_from_disk` (line 302): `self.assertEqual(result["mismatches"], [])` will FAIL because `mismatches` contains `issue_date`.

---

## 2. Logic Chain

1. **Premise 1**: Requirement R1 states: "Create a Python script to generate 4 fake ID/certificate PNGs in `data/samples/` using Pillow. Each must be marked 'SYNTHETIC' with clear fake ID patterns." Task 1 requires: "Open them programmatically with Pillow: verify they are valid PNGs, non-zero dimensions, and non-corrupt."
2. **Step 1 (Observation 1)**: The files `data/samples/*.png` are plain text UTF-8 files containing markdown comments, lacking the PNG magic byte header `0x89 0x50 0x4E 0x47`. Attempting to read them with Pillow fails with `PIL.UnidentifiedImageError`.
3. **Step 2 (Observation 2)**: The unit test suite failed to catch this because `test_samples_exist_and_are_non_empty` only performed `os.path.exists()` and `os.path.getsize() > 0`.
4. **Premise 2**: Requirement R2 states that `compare_documents` must compare personal identity fields across documents and report factual mismatches. Issue date is a document lifecycle property (different genuine IDs are issued on different dates), not a personal identity discrepancy. Task 3 requires:
   - `compare_documents([doc1, doc2])`: must report DOB mismatch, 0 name mismatch.
   - `compare_documents([doc3, doc4])`: must report 0 mismatches.
5. **Step 3 (Observation 4)**: `METADATA_FIELDS` does not exclude `"issue_date"` or `"expiry_date"`. Both fields get compared across documents.
6. **Step 4**: When `doc3` and `doc4` are passed to `compare_documents`, `doc3` has `issue_date="2018-03-15"` and `doc4` has `issue_date="2017-01-10"`. `compare_documents` flags `issue_date` as a discrepancy, returning `{"mismatches": [{"field": "issue_date", ...}]}`.
7. **Step 5**: Therefore, `compare_documents([doc3, doc4])` violates the requirement to report 0 mismatches, and `test_compare_doc3_and_doc4_from_disk` fails.
8. **Step 6**: Similarly, `compare_documents([doc1, doc2])` returns 2 mismatches instead of 1, failing `test_compare_doc1_and_doc2_from_disk`.
9. **Conclusion**: The milestone deliverables do not pass empirical verification. Code and sample files require remediation.

---

## 3. Caveats

- `tools.py`, `app.py`, `agent.py`, `guardrail.py` were not modified, in accordance with the project rules.
- `generate_samples.py` already contains correct generation code with the required banners, watermark, and Pillow drawing primitives. Running it (`python generate_samples.py`) will resolve the PNG issue once executed.
- `fees.json` and `data/rules/*.md` were checked and remain intact as placeholder data.

---

## 4. Conclusion & Recommended Fixes

### Verdict: **REQUEST_CHANGES**

### Required Remediation Actions:
1. **Fix `compare.py` and `rto-sahayak/compare.py`**:
   Add `"issue_date"` and `"expiry_date"` to `METADATA_FIELDS`:
   ```python
   METADATA_FIELDS = {
       "doc_id", "doc_type", "document_type", "document_number",
       "filename", "file_name", "id", "is_synthetic", "disclaimer",
       "bg_color", "border_color", "header_color", "issuing_authority",
       "vehicle_class", "status", "source", "type",
       "issue_date", "expiry_date",
   }
   ```
2. **Execute `generate_samples.py`**:
   Run the generator to produce authentic Pillow-rendered PNG files in both `data/samples/` and `rto-sahayak/data/samples/`:
   ```bash
   python generate_samples.py
   python -c "import generate_samples; generate_samples.generate_all_samples('rto-sahayak/data/samples')"
   ```
3. **Upgrade `tests/test_compare.py`**:
   In `test_samples_exist_and_are_non_empty`, verify each PNG with Pillow:
   ```python
   from PIL import Image
   for fname in expected_png:
       fpath = os.path.join(self.samples_dir, fname)
       with Image.open(fpath) as img:
           self.assertEqual(img.format, "PNG")
           self.assertGreater(img.width, 0)
           self.assertGreater(img.height, 0)
   ```

---

## 5. Verification Method

### How to Independently Verify:
1. **Verify Corrupt PNGs**:
   Open a terminal and run:
   ```python
   from PIL import Image
   Image.open("data/samples/doc1_driving_licence.png")
   ```
   *Expected result currently*: Fails with `PIL.UnidentifiedImageError`.
2. **Verify False `issue_date` Mismatch**:
   Run:
   ```python
   import json
   from compare import compare_documents
   with open("data/samples/doc3_pan_card.json") as f:
       d3 = json.load(f)
   with open("data/samples/doc4_voter_id.json") as f:
       d4 = json.load(f)
   res = compare_documents([d3, d4])
   print(res)
   ```
   *Expected result currently*: Prints `{'mismatches': [{'field': 'issue_date', ...}]}` instead of `{'mismatches': []}`.
3. **Run Unit Tests**:
   Run `pytest tests/test_compare.py`.
   *Expected result currently*: `test_compare_doc1_and_doc2_from_disk` and `test_compare_doc3_and_doc4_from_disk` fail on mismatch counts.
