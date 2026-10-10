# Handoff Report: Synthetic Image Explorer (`m2_explorer_3`)

**Agent ID**: `m2_explorer_3`  
**Role**: Synthetic Image Explorer  
**Recipient**: `orchestrator_2` / `parent` (`e35c4cb9-e0bf-457f-8b67-5c1e9c1c606b`)  
**Date**: 2026-10-10  
**Handoff Type**: Hard (Investigation complete, full architecture & blueprints delivered)

---

## 1. Observation

1. **User Request (R1: Synthetic Images)**:
   - File: `e:\hackthon\.agents\teamwork\ORIGINAL_REQUEST.md` (lines 47–49):
     > "Create a Python script to generate 4 fake ID/certificate PNGs in `data/samples/` using Pillow. Each must be marked "SYNTHETIC" with clear fake ID patterns. Two images must share a person's name but differ in date of birth. Save the expected extracted fields as a JSON file for each image."
2. **Comparison & Test Requirements (R2 & R3)**:
   - File: `e:\hackthon\.agents\teamwork\ORIGINAL_REQUEST.md` (lines 50–55):
     > "Implement `compare_documents(docs: list[dict])` in `compare.py` in plain Python. It must normalise dates in multiple formats, fuzzy-match names, and return factual mismatches in the format: `{"mismatches": [{"field", "doc_a", "value_a", "doc_b", "value_b"}]}`. It must not use judgmental words like "rejected" or "invalid"."
     > "Implement unit tests in `tests/` for the `compare_documents` function, covering both a mismatched pair and a matching pair."
3. **Laptop 2 Constraints & Rules**:
   - `e:\hackthon\.agents\rules\project.md`:
     > "Synthetic, public or mock data only. Never ask for or store real personal data. Label sample documents 'SYNTHETIC'."
     > "Every rule explanation cites its source file and ends with: 'Final decision rests with the RTO officer.'"
     > "Handoff PDFs carry the banner: 'DRAFT - for citizen review and officer verification'."
     > "Free only: Gemini free tier, Streamlit, local files. No Hugging Face, no paid services, no billing, no image/video generation models."
4. **Current Workspace State**:
   - `data/samples/` does not yet exist in either `e:\hackthon\data\` or `e:\hackthon\rto-sahayak\data\`.
   - `compare.py` in `rto-sahayak\` is an empty 0-byte file awaiting implementation.

---

## 2. Logic Chain

1. **Document Selection & Pairing Strategy**:
   - Requirement dictates: 4 fake ID/certificate PNGs, two sharing a person's name but differing in DOB, plus tests covering matching and mismatched pairs.
   - **Mismatched Pair (Doc 1 & Doc 2)**:
     - `doc1_driving_licence.png` & `.json`: Driving Licence, Name: `"Rahul Kumar Sharma"`, DOB: `"1995-05-15"`, Number: `"FAKE-DL-DL04-20150001"`.
     - `doc2_aadhaar_card.png` & `.json`: Aadhaar Card, Name: `"Rahul Kumar Sharma"` (identical), DOB: `"1993-05-15"` (mismatch: 1993 vs 1995), Number: `"FAKE-UID-9999-8888-7777"`.
     - When processed through `compare_documents([doc1, doc2])`, names match fuzzily/exactly, and the DOB difference is detected as a factual mismatch:
       `{"field": "date_of_birth", "doc_a": "doc1_driving_licence", "value_a": "1995-05-15", "doc_b": "doc2_aadhaar_card", "value_b": "1993-05-15"}`.
   - **Matching Pair (Doc 3 & Doc 4)**:
     - `doc3_pan_card.png` & `.json`: PAN Card, Name: `"Priya S. Patel"`, DOB: `"1998-11-22"`, Number: `"FAKE-PAN-ABCDE1234F"`.
     - `doc4_voter_id.png` & `.json`: Voter ID Card, Name: `"Priya Sanjay Patel"` (fuzzy match compatible with `Priya S. Patel`), DOB: `"22/11/1998"` (alternate date format normalising to `"1998-11-22"`), Number: `"FAKE-EPIC-XYZ9876543"`.
     - When processed through `compare_documents([doc3, doc4])`, names and dates match successfully, returning zero mismatches: `{"mismatches": []}`.

2. **Visual & Pillow Pure Rendering Architecture**:
   - Adheres to the rule prohibiting external image/video generation models: uses 100% pure standard library Pillow (`PIL.Image`, `PIL.ImageDraw`, `PIL.ImageFont`).
   - Dimensions: `800 x 500` px RGB canvas.
   - Compliance Visual Elements:
     - Top Alert Banner: `(185, 28, 28)` background with bold white centered text: `*** SYNTHETIC DOCUMENT - FOR TESTING ONLY ***`.
     - Bottom Banner: `(30, 41, 59)` slate blue background with white centered text: `DRAFT - for citizen review and officer verification`.
     - Watermark: Faint diagonal repeated watermark `SYNTHETIC SAMPLE - NOT REAL` in `(225, 230, 238)`.
     - Procedural Mock Assets: Geometrically drawn Photo avatar box, 2D QR checkered pattern, specimen signature line, and official header emblem.
     - Regulatory Disclaimer Box: Centered text including `"Final decision rests with the RTO officer."`.
   - Font Safety: Multi-tier fallback function `load_font(size, bold)` checking `arial.ttf`, `calibri.ttf`, `segoeui.ttf`, `DejaVuSans.ttf`, falling back safely to `ImageFont.load_default()` if system TTF fonts are absent.

3. **JSON Extraction Schema**:
   - Uniform dictionary representation across all 4 documents containing:
     `doc_id`, `document_type`, `document_number`, `full_name`, `date_of_birth`, `father_name`, `address`, `issue_date`, `expiry_date`, `issuing_authority`, `is_synthetic` (`true`), `disclaimer`.

---

## 3. Caveats

1. **Read-Only Explorer Scope**: In adherence to the explorer read-only mandate, no code or image files were created directly in `data/samples/` or source directories. The full executable generation script and JSON definitions are documented in `e:\hackthon\.agents\teamwork\m2_explorer_3\analysis.md`.
2. **Dual-Directory Deployment**: Laptop 2 owns both root `e:\hackthon\` and sub-directory `e:\hackthon\rto-sahayak\`. The worker agent should execute the generation script to populate `data/samples/` in both locations.
3. **Date Normalization Dependency**: `doc4_voter_id` utilizes slash format (`22/11/1998`) while `doc3_pan_card` utilizes ISO format (`1998-11-22`). The matching test relies on `compare.py` correctly implementing multi-format date normalization (as surveyed by `m2_explorer_2`).

---

## 4. Conclusion

The specification and architecture for synthetic images and JSON expected fields are complete and ready for immediate implementation by `worker_impl_1`.

Key Deliverables Specified:
1. **Four Synthetic Documents**:
   - `doc1_driving_licence` (Rahul Kumar Sharma, DOB: 1995-05-15) — Mismatch A
   - `doc2_aadhaar_card` (Rahul Kumar Sharma, DOB: 1993-05-15) — Mismatch B
   - `doc3_pan_card` (Priya S. Patel, DOB: 1998-11-22) — Match A
   - `doc4_voter_id` (Priya Sanjay Patel, DOB: 22/11/1998) — Match B
2. **Pillow Generator Script**:
   - Complete, standalone, zero-external-asset Python script detailed in `analysis.md`.
3. **Expected Extracted JSON Files**:
   - Full JSON schemas and data instances documented in `analysis.md`.

---

## 5. Verification Method

Once implemented by the worker:
1. **File Existence Check**:
   - Verify that 4 PNG files and 4 JSON files exist in `data/samples/`:
     - `doc1_driving_licence.png`, `doc1_driving_licence.json`
     - `doc2_aadhaar_card.png`, `doc2_aadhaar_card.json`
     - `doc3_pan_card.png`, `doc3_pan_card.json`
     - `doc4_voter_id.png`, `doc4_voter_id.json`
2. **JSON Schema Integrity**:
   - Run Python validation to ensure all 4 JSON files parse cleanly and contain `"is_synthetic": True` and valid field types:
     ```bash
     python -c "import json, glob; [print(f, json.load(open(f))['doc_id']) for f in glob.glob('data/samples/*.json')]"
     ```
3. **Comparison Validation**:
   - Compare `[doc1, doc2]`: verify exact 1 mismatch on `date_of_birth` (`1995-05-15` vs `1993-05-15`).
   - Compare `[doc3, doc4]`: verify 0 mismatches.
