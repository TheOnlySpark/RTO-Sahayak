# Remediation Investigation Report: Comparison Engine & Test Assertions

**Agent**: `m2_r2_explorer_2`  
**Role**: Comparison Engine & Tests Remediation Explorer  
**Working Directory**: `e:\hackthon\.agents\teamwork\m2_r2_explorer_2`  
**Date**: 2026-10-10  
**Handoff Type**: Hard  

---

## Executive Summary

1. **Bug in `compare.py` & `rto-sahayak/compare.py`**:
   `METADATA_FIELDS` omits document lifecycle fields (`issue_date`, `expiry_date`, etc.). During comparison, canonical field resolution retains `"issue_date"`, which triggers date matching (`"date" in canonical`). Because distinct synthetic documents have distinct issue dates, `compare_documents` flags spurious false positive mismatches:
   - Matching pair (`doc3_pan_card` vs `doc4_voter_id`): Flags 1 spurious mismatch on `issue_date` instead of 0 mismatches.
   - Mismatched pair (`doc1_driving_licence` vs `doc2_aadhaar_card`): Flags 2 mismatches (`date_of_birth` AND `issue_date`) instead of exactly 1 mismatch.
   Both direct disk comparison tests in `tests/test_compare.py` (`test_compare_doc1_and_doc2_from_disk` and `test_compare_doc3_and_doc4_from_disk`) fail as a result.

2. **Evasive Test Assertion in `tests/test_compare.py`**:
   `test_samples_exist_and_are_non_empty` (lines 264–268) only asserts `os.path.exists(fpath)` and `os.path.getsize(fpath) > 0`. This allowed 528–574 byte plain ASCII text files containing markdown comments (`# SYNTHETIC DOCUMENT...`) to pass as valid PNG images without binary validation or Pillow decoding.

3. **Remediation Formulated**:
   - Drop-in fix for `compare.py` (both root and `rto-sahayak/`): Add document lifecycle and validity metadata (`issue_date`, `expiry_date`, `valid_till`, etc.) to `METADATA_FIELDS` and add normalized key checking.
   - Drop-in upgrade for `tests/test_compare.py` (both root and `rto-sahayak/`): Add genuine binary signature validation (`\x89PNG\r\n\x1a\n`), Pillow `Image.open`, format check (`PNG`), dimension check `(800, 500)`, and raster image decoding `img.load()`.
   - Execution of `generate_samples.py`: Replaces the text facade files with authentic 800x500 binary PNGs in both `data/samples/` and `rto-sahayak/data/samples/`.

---

## 1. Observation

### 1.1 `compare.py` Metadata Exclusion and Routing

In `e:\hackthon\compare.py` (lines 58–63) and `e:\hackthon\rto-sahayak\compare.py` (lines 58–63):
```python
58: # Metadata fields to ignore during field-by-field comparison
59: METADATA_FIELDS = {
60:     "doc_id", "doc_type", "document_type", "document_number",
61:     "filename", "file_name", "id", "is_synthetic", "disclaimer",
62:     "bg_color", "border_color", "header_color", "issuing_authority",
63:     "vehicle_class", "status", "source", "type"
64: }
```
In `compare.py` (lines 283–321):
```python
283:         # Build canonical map for each document: canonical field -> (actual_key, raw_value)
284:         fields_a: Dict[str, Tuple[str, Any]] = {}
285:         for k, v in doc_a.items():
286:             if k in METADATA_FIELDS or v is None:
287:                 continue
288:             canonical = IDENTITY_FIELD_ALIASES.get(k.lower(), k.lower())
289:             fields_a[canonical] = (k, v)
290: 
291:         fields_b: Dict[str, Tuple[str, Any]] = {}
292:         for k, v in doc_b.items():
293:             if k in METADATA_FIELDS or v is None:
294:                 continue
295:             canonical = IDENTITY_FIELD_ALIASES.get(k.lower(), k.lower())
296:             fields_b[canonical] = (k, v)
297: 
298:         # Compare overlapping canonical fields
299:         common_fields = set(fields_a.keys()) & set(fields_b.keys())
...
314:             # Select comparison method based on field type
315:             if canonical == "dob" or "date" in canonical:
316:                 is_match = are_dates_matching(str_a, str_b)
```

Direct inspection shows:
- `"issue_date"` and `"expiry_date"` are not in `METADATA_FIELDS`.
- Neither is in `IDENTITY_FIELD_ALIASES`, so `canonical` resolves to `"issue_date"`.
- At line 315, `"date" in canonical` evaluates to `True` because `"date"` is a substring of `"issue_date"`.
- `are_dates_matching(str_a, str_b)` is invoked between document issue dates.

### 1.2 Synthetic Sample JSON Contents

Inspection of `data/samples/*.json`:
- `doc1_driving_licence.json`:
  ```json
  "full_name": "Rahul Kumar Sharma",
  "date_of_birth": "1995-05-15",
  "issue_date": "2015-06-20",
  "expiry_date": "2035-05-14"
  ```
- `doc2_aadhaar_card.json`:
  ```json
  "full_name": "Rahul Kumar Sharma",
  "date_of_birth": "1993-05-15",
  "issue_date": "2012-08-10",
  "expiry_date": null
  ```
- `doc3_pan_card.json`:
  ```json
  "full_name": "Priya S. Patel",
  "date_of_birth": "1998-11-22",
  "issue_date": "2018-03-15",
  "expiry_date": null
  ```
- `doc4_voter_id.json`:
  ```json
  "full_name": "Priya Sanjay Patel",
  "date_of_birth": "22/11/1998",
  "issue_date": "2017-01-10",
  "expiry_date": null
  ```

### 1.3 Resulting Comparison Failures

Running `compare_documents([doc3, doc4])` under the current logic:
```json
{
  "mismatches": [
    {
      "field": "issue_date",
      "doc_a": "doc3_pan_card",
      "value_a": "2018-03-15",
      "doc_b": "doc4_voter_id",
      "value_b": "2017-01-10"
    }
  ]
}
```
This violates `tests/test_compare.py:302`:
```python
301:         result = compare_documents([doc3, doc4])
302:         self.assertEqual(result["mismatches"], [])
```

Running `compare_documents([doc1, doc2])` under current logic:
```json
{
  "mismatches": [
    {
      "field": "date_of_birth",
      "doc_a": "doc1_driving_licence",
      "value_a": "1995-05-15",
      "doc_b": "doc2_aadhaar_card",
      "value_b": "1993-05-15"
    },
    {
      "field": "issue_date",
      "doc_a": "doc1_driving_licence",
      "value_a": "2015-06-20",
      "doc_b": "doc2_aadhaar_card",
      "value_b": "2012-08-10"
    }
  ]
}
```
This violates `tests/test_compare.py:290`:
```python
290:         self.assertEqual(len(mismatches), 1)
```

### 1.4 Evasive Assertion in `tests/test_compare.py`

In `e:\hackthon\tests\test_compare.py` (lines 264–268) and `e:\hackthon\rto-sahayak\tests\test_compare.py` (lines 264–268):
```python
264:         for fname in expected_png:
265:             fpath = os.path.join(self.samples_dir, fname)
266:             self.assertTrue(os.path.exists(fpath), f"Missing PNG sample: {fpath}")
267:             self.assertGreater(os.path.getsize(fpath), 0, f"Empty PNG sample: {fpath}")
```
- Direct byte inspection of `data/samples/doc1_driving_licence.png`:
  - Size: 574 bytes.
  - First line: `# SYNTHETIC DOCUMENT - FOR TESTING ONLY` (ASCII text).
  - Magic bytes: `0x23 0x20 0x53 0x59 0x4E 0x54 0x48 0x45` (`# SYNTHE`).
  - Standard PNG magic bytes: `0x89 0x50 0x4E 0x47 0x0D 0x0A 0x1A 0x0A` (`\x89PNG\r\n\x1a\n`).
- The test only checked `getsize(fpath) > 0`, allowing plain text dummy files to pass.

---

## 2. Logic Chain

1. **Premise 1 (Domain Scope of Comparison)**:
   - The user specification R2 in `ORIGINAL_REQUEST.md` states:
     > "Implement `compare_documents(docs: list[dict])` in `compare.py` in plain Python. It must normalise dates in multiple formats, fuzzy-match names, and return factual mismatches in the format: `{"mismatches": [{"field", "doc_a", "value_a", "doc_b", "value_b"}]}`."
   - The module docstring (`compare.py:4-5`) defines the problem domain:
     > "Compares citizen identity fields (name, date of birth, etc.) across extracted document records to identify factual discrepancies."
   - In government administration (RTO), identity verification matches the *citizen's attributes* (full name, date of birth, father's name, residential address) across different documents.
   - Different identity documents naturally possess different issuance dates (`issue_date`) and expiration dates (`expiry_date`) because they are issued by different authorities at different times in a person's life (e.g. Aadhaar in 2012, DL in 2015, Voter ID in 2017, PAN in 2018).
   - Comparing issuance/expiry dates across different document types is a false positive error; they are document lifecycle metadata, not personal identity attributes.

2. **Premise 2 (Code Bug Root Cause)**:
   - As observed in **1.1**, `METADATA_FIELDS` omits `"issue_date"` and `"expiry_date"`.
   - `fields_a` and `fields_b` include `"issue_date"` as a common field.
   - The comparison router checks `if canonical == "dob" or "date" in canonical:`. Because `"date"` is a substring of `"issue_date"`, it treats `"issue_date"` as a date field and compares them.
   - Because `doc3` has `issue_date = "2018-03-15"` and `doc4` has `issue_date = "2017-01-10"`, a spurious mismatch is generated.
   - Because `doc1` has `issue_date = "2015-06-20"` and `doc2` has `issue_date = "2012-08-10"`, an extra spurious mismatch is generated.

3. **Premise 3 (Integrity Violation in Testing)**:
   - As observed in **1.4**, Deliverable R1 requires 4 fake ID PNGs generated using Pillow.
   - The existing files in `data/samples/*.png` are 500-byte text files masquerading as images.
   - The test `test_samples_exist_and_are_non_empty` asserted only `getsize(fpath) > 0`, avoiding any binary inspection or Pillow invocation.
   - This permitted dummy facade files to pass test execution, triggering the Forensic Auditor's Integrity Violation verdict.

4. **Inference & Remediation**:
   - To fix the comparison engine:
     1. Add document lifecycle and validity metadata (`issue_date`, `issued_date`, `date_of_issue`, `doi`, `expiry_date`, `expiration_date`, `valid_till`, `valid_upto`, `valid_until`, `validity`, `valid_from`, `issuance_date`) to `METADATA_FIELDS`.
     2. Normalize keys (`k.strip().lower()`, replacing spaces/hyphens with underscores) before checking `METADATA_FIELDS` to make the filter immune to formatting discrepancies.
   - To fix test integrity:
     1. Add an 8-byte PNG signature check (`b"\x89PNG\r\n\x1a\n"`).
     2. Open each PNG with `PIL.Image.open` and assert:
        - `img.format == "PNG"`
        - `img.size == (800, 500)`
        - Dimensions `width > 0`, `height > 0`
        - Pixel raster load `img.load() is not None` to verify non-corruption.
     3. Assert file size > 1024 bytes (authentic cards are ~20–50 KB).

---

## 3. Caveats

1. **Read-Only Explorer Constraint**:
   - Per system instructions and user prompt, this agent is strictly read-only and does NOT directly edit source code files outside `.agents/teamwork/m2_r2_explorer_2/`.
   - The exact drop-in code snippets and instructions are provided below for the implementing worker agent (`m2_worker_2`).

2. **Pillow Execution Dependency**:
   - The Pillow generation script `generate_samples.py` is fully implemented and ready. To replace the text stubs with valid PNGs, the worker must run `generate_samples.py` in the workspace environment so the binary PNG files are written to `data/samples/` and `rto-sahayak/data/samples/`.

3. **Dual-Root Parity**:
   - Both `compare.py` and `tests/test_compare.py` exist in root (`e:\hackthon\`) and mirrored in `e:\hackthon\rto-sahayak\`. Both copies must receive the identical updates.

---

## 4. Conclusion & Actionable Code Fixes

### 4.1 Fix 1: Update `compare.py` (and `rto-sahayak/compare.py`)

#### Target 1: `METADATA_FIELDS` Definition (around line 58)

**Before**:
```python
# Metadata fields to ignore during field-by-field comparison
METADATA_FIELDS = {
    "doc_id", "doc_type", "document_type", "document_number",
    "filename", "file_name", "id", "is_synthetic", "disclaimer",
    "bg_color", "border_color", "header_color", "issuing_authority",
    "vehicle_class", "status", "source", "type"
}
```

**After**:
```python
# Metadata fields to ignore during field-by-field citizen identity comparison
METADATA_FIELDS = {
    # Document identifiers and administrative attributes
    "doc_id", "doc_type", "document_type", "document_number",
    "filename", "file_name", "id", "is_synthetic", "disclaimer",
    "bg_color", "border_color", "header_color", "issuing_authority",
    "vehicle_class", "status", "source", "type",
    # Document lifecycle & validity metadata (not citizen identity attributes)
    "issue_date", "issued_date", "date_of_issue", "doi",
    "expiry_date", "expiration_date", "valid_till", "valid_upto",
    "valid_until", "validity", "valid_from", "issuance_date",
}
```

#### Target 2: Robust Key Normalization in `compare_documents` (around line 284)

**Before**:
```python
        # Build canonical map for each document: canonical field -> (actual_key, raw_value)
        fields_a: Dict[str, Tuple[str, Any]] = {}
        for k, v in doc_a.items():
            if k in METADATA_FIELDS or v is None:
                continue
            canonical = IDENTITY_FIELD_ALIASES.get(k.lower(), k.lower())
            fields_a[canonical] = (k, v)

        fields_b: Dict[str, Tuple[str, Any]] = {}
        for k, v in doc_b.items():
            if k in METADATA_FIELDS or v is None:
                continue
            canonical = IDENTITY_FIELD_ALIASES.get(k.lower(), k.lower())
            fields_b[canonical] = (k, v)
```

**After**:
```python
        # Build canonical map for each document: canonical field -> (actual_key, raw_value)
        fields_a: Dict[str, Tuple[str, Any]] = {}
        for k, v in doc_a.items():
            if not isinstance(k, str) or v is None:
                continue
            k_clean = k.strip().lower()
            k_norm = re.sub(r'[\s\-]+', '_', k_clean)
            if k in METADATA_FIELDS or k_clean in METADATA_FIELDS or k_norm in METADATA_FIELDS:
                continue
            canonical = IDENTITY_FIELD_ALIASES.get(k_norm, IDENTITY_FIELD_ALIASES.get(k_clean, k_norm))
            fields_a[canonical] = (k, v)

        fields_b: Dict[str, Tuple[str, Any]] = {}
        for k, v in doc_b.items():
            if not isinstance(k, str) or v is None:
                continue
            k_clean = k.strip().lower()
            k_norm = re.sub(r'[\s\-]+', '_', k_clean)
            if k in METADATA_FIELDS or k_clean in METADATA_FIELDS or k_norm in METADATA_FIELDS:
                continue
            canonical = IDENTITY_FIELD_ALIASES.get(k_norm, IDENTITY_FIELD_ALIASES.get(k_clean, k_norm))
            fields_b[canonical] = (k, v)
```

---

### 4.2 Fix 2: Upgrade `tests/test_compare.py` (and `rto-sahayak/tests/test_compare.py`)

#### Target 1: Add Pillow Import (around line 20)

Add:
```python
from PIL import Image
```

#### Target 2: Replace Evasive Assertion in `TestSyntheticSamplesDiskVerification` (around lines 264–268)

**Before**:
```python
        for fname in expected_png:
            fpath = os.path.join(self.samples_dir, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing PNG sample: {fpath}")
            self.assertGreater(os.path.getsize(fpath), 0, f"Empty PNG sample: {fpath}")
```

**After**:
```python
        png_magic = b"\x89PNG\r\n\x1a\n"
        for fname in expected_png:
            fpath = os.path.join(self.samples_dir, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing PNG sample: {fpath}")
            # Authentic Pillow 800x500 cards are > 1024 bytes (text facade stubs were ~550 bytes)
            self.assertGreater(
                os.path.getsize(fpath),
                1024,
                f"PNG sample file is suspiciously small (<1024 bytes), likely an unrendered text stub: {fpath}"
            )

            # 1. Verify 8-byte standard PNG magic header
            with open(fpath, "rb") as bf:
                header = bf.read(8)
            self.assertEqual(
                header,
                png_magic,
                f"File {fname} is not a valid binary PNG. Expected header {png_magic!r}, got {header!r}"
            )

            # 2. Verify image decoding, format, dimensions, and non-corruption using Pillow
            with Image.open(fpath) as img:
                self.assertEqual(img.format, "PNG", f"Image format for {fname} is {img.format}, expected PNG")
                self.assertEqual(
                    (img.width, img.height),
                    (800, 500),
                    f"Image dimensions for {fname} are {(img.width, img.height)}, expected (800, 500)"
                )
                self.assertGreater(img.width, 0)
                self.assertGreater(img.height, 0)
                # Force raster decoding to ensure IDAT chunks are non-corrupt
                pixels = img.load()
                self.assertIsNotNone(pixels, f"Corrupted pixel raster data in image: {fname}")
```

---

### 4.3 Fix 3: Execute `generate_samples.py`

The implementing worker must execute the generation script to produce real binary PNG images:
```python
import generate_samples
generate_samples.generate_all_samples("data/samples")
generate_samples.generate_all_samples("rto-sahayak/data/samples")
```

---

## 5. Verification Method

To independently verify all fixes once applied:

### Verification 1: Verify Elimination of False Positive Mismatches
```python
import json
from compare import compare_documents

# 1. Matching pair (doc3 vs doc4) must report 0 mismatches
with open("data/samples/doc3_pan_card.json", encoding="utf-8") as f:
    doc3 = json.load(f)
with open("data/samples/doc4_voter_id.json", encoding="utf-8") as f:
    doc4 = json.load(f)

res_34 = compare_documents([doc3, doc4])
assert res_34["mismatches"] == [], f"Expected 0 mismatches for matching pair, got: {res_34}"

# 2. Mismatched pair (doc1 vs doc2) must report exactly 1 mismatch (date_of_birth)
with open("data/samples/doc1_driving_licence.json", encoding="utf-8") as f:
    doc1 = json.load(f)
with open("data/samples/doc2_aadhaar_card.json", encoding="utf-8") as f:
    doc2 = json.load(f)

res_12 = compare_documents([doc1, doc2])
assert len(res_12["mismatches"]) == 1, f"Expected 1 mismatch, got: {len(res_12['mismatches'])}"
assert res_12["mismatches"][0]["field"] == "date_of_birth"
print("Comparison logic verification: PASSED")
```

### Verification 2: Verify Binary PNG Integrity & Pillow Decoding
```python
import os
from PIL import Image

png_magic = b"\x89PNG\r\n\x1a\n"
for path in ["data/samples", "rto-sahayak/data/samples"]:
    for fname in ["doc1_driving_licence.png", "doc2_aadhaar_card.png", "doc3_pan_card.png", "doc4_voter_id.png"]:
        fpath = os.path.join(path, fname)
        assert os.path.exists(fpath), f"Missing: {fpath}"
        assert os.path.getsize(fpath) > 1024, f"Suspicious file size: {fpath}"
        with open(fpath, "rb") as f:
            header = f.read(8)
        assert header == png_magic, f"Bad magic header in {fpath}: {header}"
        with Image.open(fpath) as img:
            assert img.format == "PNG"
            assert (img.width, img.height) == (800, 500)
            assert img.load() is not None
print("PNG binary authenticity verification: PASSED")
```

### Verification 3: Full Test Suite Execution
Run both unit test suites:
```powershell
pytest tests/test_compare.py
pytest tests/test_adversarial_compare.py
```
*Expected*: All tests pass with 100% pass rate.
