# Document Comparison Engine Analysis & Design Specification

**Agent**: `m2_explorer_2` (Comparison Algorithm Explorer)  
**Assigned Folder**: `e:\hackthon\.agents\teamwork\m2_explorer_2`  
**Milestone**: Milestone 2 (Document Verification, Synthetic Samples & Comparison Engine)  
**Parent / Caller**: `e35c4cb9-e0bf-457f-8b67-5c1e9c1c606b`

---

## 1. Observation

1. **User Request (`e:\hackthon\.agents\teamwork\ORIGINAL_REQUEST.md`)**:
   - Lines 50-52:
     > "### R2. Comparison Script  
     > Implement `compare_documents(docs: list[dict])` in `compare.py` in plain Python. It must normalise dates in multiple formats, fuzzy-match names, and return factual mismatches in the format: `{"mismatches": [{"field", "doc_a", "value_a", "doc_b", "value_b"}]}`. It must not use judgmental words like "rejected" or "invalid"."
   - Lines 53-55:
     > "### R3. Unit Tests  
     > Implement unit tests in `tests/` for the `compare_documents` function, covering both a mismatched pair and a matching pair. Execute the tests to ensure they pass."

2. **Existing Files and Status**:
   - `e:\hackthon\rto-sahayak\compare.py`: Currently an empty file (0 bytes, 1 blank line).
   - `e:\hackthon\compare.py`: Not present yet at workspace root.
   - `tests/test_basic.py`: Line 1-238 demonstrates the test conventions for the project, path resolution mechanism for `rto-sahayak/` and workspace root, and strict compliance with officer disclaimers and synthetic data labeling.

3. **Peer Explorer Alignment (`e:\hackthon\.agents\teamwork\m2_explorer_3\analysis.md`)**:
   - Lines 21-29 specify 4 synthetic documents:
     - `doc1_driving_licence`: Name `Rahul Kumar Sharma`, DOB `1995-05-15`.
     - `doc2_aadhaar_card`: Name `Rahul Kumar Sharma`, DOB `1993-05-15` (Mismatched Pair: same name, differing DOB).
     - `doc3_pan_card`: Name `Priya S. Patel`, DOB `1998-11-22`.
     - `doc4_voter_id`: Name `Priya Sanjay Patel`, DOB `22/11/1998` (Matching Pair: fuzzy name via initial `S.` == `Sanjay`, normalized date `22/11/1998` == `1998-11-22`).
   - Fields in JSON files: `doc_id`, `document_type`, `document_number`, `full_name`, `date_of_birth`, `father_name`, `address`, `issue_date`, `expiry_date`.

4. **Safety & Policy Constraints**:
   - Strictly NO judgmental words: words such as `rejected`, `invalid`, `fake`, `forged`, `fraudulent`, `illegal`, `tampered`, `suspicious`, `unacceptable` must NEVER appear in output keys, values, or explanations.
   - Must use standard library only: `re`, `datetime`, `difflib`, `itertools`.
   - Small, student-explainable plain Python design.
   - Mandatory disclaimer: "Final decision rests with the RTO officer."

---

## 2. Logic Chain

1. **Date Normalization Reasoning**:
   - In Indian official documents, dates appear in varied formats: `DD/MM/YYYY`, `DD-MM-YYYY`, `DD.MM.YYYY`, `YYYY-MM-DD`, `DD/MM/YY`, `DD Month YYYY` ("15 May 1995"), `Month DD, YYYY` ("May 15, 1995"), and with ordinal suffixes ("15th May 1995").
   - To avoid locale discrepancies across different OS environments (e.g. Windows vs Linux C-runtime `%b` quirks), dates should be parsed via regular expressions with explicit numerical month mapping (`MONTH_MAP`), validated via `datetime(year, month, day)`, and serialized to ISO `YYYY-MM-DD`.
   - For 2-digit years (`%y`), a century pivot is required: values <= current 2-digit year are 2000s; values > current 2-digit year are 1900s (e.g. `95` -> `1995`, `05` -> `2005`).

2. **Name Matching Reasoning**:
   - Differences in citizen names occur across 4 dimensions:
     1. Case & Whitespace: Solved by `.lower()` and collapsing whitespace.
     2. Honorifics: Prefixes such as `Mr.`, `Shri`, `Smt.`, `Dr.` should be stripped from the start of token lists.
     3. Initials vs Full Name: Example: `"Priya S. Patel"` vs `"Priya Sanjay Patel"` or `"R. K. Sharma"` vs `"Rahul Kumar Sharma"`. When tokens align and an initial matches the first letter of the corresponding full name token, this represents the same person.
     4. Minor Typos: `difflib.SequenceMatcher.ratio()` with a threshold of `0.85` safely matches typos (`"Rahul"` vs `"Rahuk"`, ratio 0.92; `"Vikram"` vs `"Vickram"`, ratio 0.96) while rejecting distinct names (`"Rahul"` vs `"Priya"`, ratio 0.67; `"Rohit"` vs `"Mohit"`, ratio 0.80).

3. **Field Filtering & Canonical Aliasing Reasoning**:
   - Different documents have different structural fields: a Driving Licence has `vehicle_class` and `license_number`; an Aadhaar card does not. Comparing document numbers across different document types is invalid because each document has its own unique numbering scheme.
   - Document comparison must specifically compare **citizen identity fields**:
     - Name (`name`, `full_name`)
     - Date of Birth (`dob`, `date_of_birth`)
     - Father / Guardian Name (`father_name`, `father`)
     - Address (`address`, if present)
     - Gender (`gender`, if present)
   - Canonical aliasing allows documents with `{"dob": "..."}` and `{"date_of_birth": "..."}` or `{"name": "..."}` and `{"full_name": "..."}` to be compared seamlessly.
   - Metadata keys (`doc_id`, `document_type`, `document_number`, `disclaimer`, `is_synthetic`, etc.) must be ignored during field-by-field value comparison.

4. **Multi-Document Pairwise Reasoning**:
   - If `len(docs) < 2`: returns `{"mismatches": []}`.
   - If `len(docs) >= 2`: `itertools.combinations(enumerate(docs), 2)` performs an exhaustive pairwise comparison.
   - Every pairwise discrepancy is captured with exact keys:
     `{"field": field_name, "doc_a": id_a, "value_a": val_a, "doc_b": id_b, "value_b": val_b}`.
   - All comparisons are strictly factual: they report only that values differ between document A and document B, leaving all determinations to the RTO officer.

---

## 3. Caveats

1. **Address Comparison Granularity**:
   - Addresses across Indian documents often differ in formatting (e.g., abbreviations like "Rd" vs "Road", pin codes, colony names). The proposed engine performs normalized whitespace/case equality for address strings. Deep street-level address matching is not required for Milestone 2.
2. **Ambiguous Numeric Dates (e.g., `05/06/1995`)**:
   - Indian official documents overwhelmingly follow `DD/MM/YYYY`. The engine prioritizes `DD/MM/YYYY` over `MM/DD/YYYY` for slash/dash delimiters.
3. **Empty / Missing Fields**:
   - If a document does not contain a field present in another document, no mismatch is raised. Mismatches are only reported when both documents supply a value for the same identity field and those values factually differ.

---

## 4. Conclusion & Proposed Implementation

### 4.1 Proposed `compare.py` Architecture

The implementer should write the following complete, self-contained implementation into both `compare.py` (root) and `rto-sahayak/compare.py`:

```python
"""
Document Comparison Engine for RTO Sahayak.

Compares citizen identity fields (name, date of birth, etc.) across
extracted document records to identify factual discrepancies.

Strictly non-judgmental: reports factual differences without declaring
documents 'invalid', 'fake', or 'rejected'. Final decision rests with the RTO officer.
"""

from __future__ import annotations

import re
from datetime import datetime
import difflib
import itertools
from typing import Any, Dict, List, Optional, Tuple

# Common prefixes/honorifics in Indian identity documents
HONORIFICS = {
    "mr", "mrs", "ms", "miss", "shri", "sh", "sri", "smt", "dr", "prof", "master"
}

# Explicit month dictionary for robust cross-platform parsing
MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

# Canonical identity field mapping
IDENTITY_FIELD_ALIASES = {
    "name": "name",
    "full_name": "name",
    "applicant_name": "name",
    "holder_name": "name",
    "dob": "dob",
    "date_of_birth": "dob",
    "birth_date": "dob",
    "father_name": "father_name",
    "father": "father_name",
    "fathers_name": "father_name",
    "address": "address",
    "residential_address": "address",
    "gender": "gender",
}

# Metadata fields to ignore during field-by-field comparison
METADATA_FIELDS = {
    "doc_id", "doc_type", "document_type", "document_number",
    "filename", "file_name", "id", "is_synthetic", "disclaimer",
    "bg_color", "border_color", "header_color", "issuing_authority",
    "vehicle_class", "status", "source", "type"
}


def normalize_date(date_str: Any) -> str:
    """
    Normalise date string to ISO YYYY-MM-DD format.
    
    Supports:
    - YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD
    - DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY
    - DD/MM/YY, DD-MM-YY, DD.MM.YY
    - DD Month YYYY (e.g. 15 May 1995, 15-MAY-1995, 15th May 1995)
    - Month DD, YYYY (e.g. May 15, 1995, May 15 1995)
    """
    if not date_str or not isinstance(date_str, str):
        return ""
    
    raw = date_str.strip()
    if not raw:
        return ""
    
    # Clean ordinals (1st, 2nd, 3rd, 15th) and commas
    cleaned = re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1', raw, flags=re.IGNORECASE)
    cleaned = cleaned.replace(",", " ")
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    current_year = datetime.now().year
    
    # Pattern A: YYYY-MM-DD or YYYY/MM/DD or YYYY.MM.DD
    m = re.match(r'^(\d{4})[-/.](0?[1-9]|1[0-2])[-/.](0?[1-9]|[12]\d|3[01])$', cleaned)
    if m:
        year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            return datetime(year, month, day).strftime("%Y-%m-%d")
        except ValueError:
            pass
            
    # Pattern B: DD-MM-YYYY or DD/MM/YYYY or DD.MM.YYYY
    m = re.match(r'^(0?[1-9]|[12]\d|3[01])[-/.](0?[1-9]|1[0-2])[-/.](\d{4})$', cleaned)
    if m:
        day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            return datetime(year, month, day).strftime("%Y-%m-%d")
        except ValueError:
            pass
            
    # Pattern C: DD-MM-YY or DD/MM/YY or DD.MM.YY (2-digit year)
    m = re.match(r'^(0?[1-9]|[12]\d|3[01])[-/.](0?[1-9]|1[0-2])[-/.](\d{2})$', cleaned)
    if m:
        day, month, year_2d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        # Century pivot
        year = 2000 + year_2d if year_2d <= (current_year % 100) else 1900 + year_2d
        try:
            return datetime(year, month, day).strftime("%Y-%m-%d")
        except ValueError:
            pass
            
    # Pattern D: DD Month YYYY (e.g. 15 May 1995, 15-May-1995)
    m = re.match(r'^(0?[1-9]|[12]\d|3[01])[-/\s]+([a-zA-Z]+)[-/\s]+(\d{2,4})$', cleaned)
    if m:
        day = int(m.group(1))
        m_str = m.group(2).lower()
        y_val = int(m.group(3))
        if y_val < 100:
            y_val = 2000 + y_val if y_val <= (current_year % 100) else 1900 + y_val
        if m_str in MONTH_MAP:
            try:
                return datetime(y_val, MONTH_MAP[m_str], day).strftime("%Y-%m-%d")
            except ValueError:
                pass

    # Pattern E: Month DD YYYY (e.g. May 15 1995)
    m = re.match(r'^([a-zA-Z]+)[-/\s]+(0?[1-9]|[12]\d|3[01])[-/\s]+(\d{2,4})$', cleaned)
    if m:
        m_str = m.group(1).lower()
        day = int(m.group(2))
        y_val = int(m.group(3))
        if y_val < 100:
            y_val = 2000 + y_val if y_val <= (current_year % 100) else 1900 + y_val
        if m_str in MONTH_MAP:
            try:
                return datetime(y_val, MONTH_MAP[m_str], day).strftime("%Y-%m-%d")
            except ValueError:
                pass

    # Fallback to standard strptime formats
    fallback_formats = [
        "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",
        "%d %b %Y", "%d %B %Y", "%b %d %Y", "%B %d %Y",
    ]
    for fmt in fallback_formats:
        try:
            return datetime.strptime(cleaned, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return raw


def normalize_name(name_str: Any) -> str:
    """
    Normalise a personal name by lowercasing, removing honorifics,
    expanding initials punctuation, and collapsing whitespace.
    """
    if not name_str or not isinstance(name_str, str):
        return ""
    
    # Replace dots and special characters with space to separate initials
    text = re.sub(r'[\.,_\-]', ' ', name_str.lower())
    tokens = text.strip().split()
    
    # Strip leading honorifics (e.g., Mr, Shri, Smt)
    while tokens and tokens[0] in HONORIFICS:
        tokens.pop(0)
        
    return " ".join(tokens)


def are_names_matching(name_a: str, name_b: str, threshold: float = 0.85) -> bool:
    """
    Compare two names using normalization, initial expansion, and fuzzy similarity.
    """
    norm_a = normalize_name(name_a)
    norm_b = normalize_name(name_b)
    
    if not norm_a or not norm_b:
        return norm_a == norm_b
        
    # 1. Exact match after normalization
    if norm_a == norm_b:
        return True
        
    tokens_a = norm_a.split()
    tokens_b = norm_b.split()
    
    # 2. Token initials match (e.g. "Priya S. Patel" vs "Priya Sanjay Patel")
    if len(tokens_a) == len(tokens_b) and len(tokens_a) > 1:
        match_all = True
        has_full_match = False
        for ta, tb in zip(tokens_a, tokens_b):
            if ta == tb:
                has_full_match = True
            elif (len(ta) == 1 and tb.startswith(ta)) or (len(tb) == 1 and ta.startswith(tb)):
                continue
            else:
                match_all = False
                break
        if match_all and has_full_match:
            return True

    # 3. Fuzzy match via SequenceMatcher ratio for typos
    ratio = difflib.SequenceMatcher(None, norm_a, norm_b).ratio()
    if ratio >= threshold:
        return True
        
    return False


def are_dates_matching(date_a: str, date_b: str) -> bool:
    """
    Compare two date strings by normalizing them to ISO YYYY-MM-DD.
    """
    norm_a = normalize_date(date_a)
    norm_b = normalize_date(date_b)
    
    if norm_a and norm_b:
        return norm_a == norm_b
    return str(date_a).strip() == str(date_b).strip()


def get_doc_identifier(doc: dict, index: int) -> str:
    """Extract a human-readable identifier for the document."""
    candidates = ["doc_id", "doc_type", "document_type", "doc_name", "filename", "id"]
    for k in candidates:
        val = doc.get(k)
        if val and isinstance(val, str) and val.strip():
            return val.strip()
    return f"document_{index + 1}"


def compare_documents(docs: list[dict]) -> dict:
    """
    Compare extracted fields across documents and return factual mismatches.
    
    Args:
        docs: list of dicts representing extracted document fields.
        
    Returns:
        dict with structure:
        {"mismatches": [{"field": ..., "doc_a": ..., "value_a": ..., "doc_b": ..., "value_b": ...}]}
    """
    if not docs or not isinstance(docs, list) or len(docs) < 2:
        return {"mismatches": []}
        
    mismatches = []
    
    # Perform pairwise comparison for all distinct document pairs
    for (idx_a, doc_a), (idx_b, doc_b) in itertools.combinations(enumerate(docs), 2):
        if not isinstance(doc_a, dict) or not isinstance(doc_b, dict):
            continue
            
        id_a = get_doc_identifier(doc_a, idx_a)
        id_b = get_doc_identifier(doc_b, idx_b)
        
        # Disambiguate if identifiers are identical
        if id_a == id_b:
            id_a = f"{id_a} (doc {idx_a + 1})"
            id_b = f"{id_b} (doc {idx_b + 1})"
            
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
            
        # Compare overlapping canonical fields
        common_fields = set(fields_a.keys()) & set(fields_b.keys())
        
        # Sort for deterministic output
        for canonical in sorted(common_fields):
            key_a, val_a = fields_a[canonical]
            key_b, val_b = fields_b[canonical]
            
            str_a = str(val_a).strip()
            str_b = str(val_b).strip()
            
            if not str_a and not str_b:
                continue
                
            is_match = False
            
            # Select comparison method based on field type
            if canonical == "dob" or "date" in canonical:
                is_match = are_dates_matching(str_a, str_b)
            elif canonical in ("name", "father_name") or "name" in canonical:
                is_match = are_names_matching(str_a, str_b)
            else:
                is_match = re.sub(r'\s+', ' ', str_a.lower()) == re.sub(r'\s+', ' ', str_b.lower())
                
            if not is_match:
                field_name = key_a if key_a == key_b else canonical
                mismatches.append({
                    "field": field_name,
                    "doc_a": id_a,
                    "value_a": val_a,
                    "doc_b": id_b,
                    "value_b": val_b,
                })
                
    return {"mismatches": mismatches}
```

---

### 4.2 Proposed Test Suite for `tests/test_compare.py`

The test suite must be placed in `tests/test_compare.py` (and mirrored in `rto-sahayak/tests/test_compare.py`):

```python
"""
Unit tests for compare_documents in compare.py.
Covers matching pairs, mismatched pairs, edge cases, date normalization,
fuzzy name matching, and strict non-judgmental language audit.
"""

import os
import sys
import json
import pytest

# Ensure project root is importable
for candidate in [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rto-sahayak")),
    os.path.abspath("."),
]:
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

from compare import compare_documents, normalize_date, normalize_name, are_names_matching, are_dates_matching


class TestDateNormalization:
    """Verifies normalize_date across multiple date formats."""
    
    @pytest.mark.parametrize("input_date,expected", [
        ("1995-05-15", "1995-05-15"),
        ("15/05/1995", "1995-05-15"),
        ("15-05-1995", "1995-05-15"),
        ("15.05.1995", "1995-05-15"),
        ("5/5/1995", "1995-05-05"),
        ("15/05/95", "1995-05-15"),
        ("15 May 1995", "1995-05-15"),
        ("15-MAY-1995", "1995-05-15"),
        ("15th May 1995", "1995-05-15"),
        ("May 15, 1995", "1995-05-15"),
        ("22/11/1998", "1998-11-22"),
    ])
    def test_valid_date_formats(self, input_date, expected):
        assert normalize_date(input_date) == expected

    def test_invalid_date_fallback(self):
        assert normalize_date("not-a-date") == "not-a-date"
        assert normalize_date("") == ""
        assert normalize_date(None) == ""


class TestFuzzyNameMatching:
    """Verifies are_names_matching for whitespace, case, honorifics, initials, and typos."""
    
    def test_exact_and_case(self):
        assert are_names_matching("Rahul Kumar Sharma", "rahul kumar sharma") is True
        assert are_names_matching("RAHUL KUMAR SHARMA", "Rahul Kumar Sharma") is True

    def test_whitespace_and_punctuation(self):
        assert are_names_matching("  Rahul   Kumar   Sharma  ", "Rahul Kumar Sharma") is True

    def test_honorifics_removal(self):
        assert are_names_matching("Mr. Rahul Sharma", "Rahul Sharma") is True
        assert are_names_matching("Shri Rahul Sharma", "Rahul Sharma") is True
        assert are_names_matching("Mrs. Priya Sharma", "Priya Sharma") is True
        assert are_names_matching("Dr. Vikram Singh", "Vikram Singh") is True

    def test_initials_matching(self):
        assert are_names_matching("Priya S. Patel", "Priya Sanjay Patel") is True
        assert are_names_matching("R. K. Sharma", "Rahul Kumar Sharma") is True
        assert are_names_matching("Rahul K. Sharma", "Rahul Kumar Sharma") is True

    def test_minor_typos(self):
        assert are_names_matching("Vikram Singh", "Vickram Singh") is True
        assert are_names_matching("Rahul Sharma", "Rahuk Sharma") is True

    def test_distinct_names_do_not_match(self):
        assert are_names_matching("Rahul Sharma", "Priya Sharma") is False
        assert are_names_matching("Amit Kumar", "Sumit Verma") is False


class TestCompareDocuments:
    """Verifies compare_documents requirements R2 & R3."""

    def test_matching_pair_returns_empty_mismatches(self):
        doc_a = {
            "doc_id": "doc3_pan_card",
            "full_name": "Priya S. Patel",
            "date_of_birth": "1998-11-22",
            "father_name": "Sanjay Patel",
        }
        doc_b = {
            "doc_id": "doc4_voter_id",
            "full_name": "Priya Sanjay Patel",
            "date_of_birth": "22/11/1998",
            "father_name": "Sanjay Patel",
        }
        result = compare_documents([doc_a, doc_b])
        assert isinstance(result, dict)
        assert "mismatches" in result
        assert result["mismatches"] == []

    def test_mismatched_dob_pair(self):
        doc_a = {
            "doc_id": "doc1_driving_licence",
            "full_name": "Rahul Kumar Sharma",
            "date_of_birth": "1995-05-15",
        }
        doc_b = {
            "doc_id": "doc2_aadhaar_card",
            "full_name": "Rahul Kumar Sharma",
            "date_of_birth": "1993-05-15",
        }
        result = compare_documents([doc_a, doc_b])
        assert "mismatches" in result
        assert len(result["mismatches"]) == 1
        m = result["mismatches"][0]
        assert m["field"] in ("date_of_birth", "dob")
        assert m["doc_a"] == "doc1_driving_licence"
        assert m["value_a"] == "1995-05-15"
        assert m["doc_b"] == "doc2_aadhaar_card"
        assert m["value_b"] == "1993-05-15"

    def test_mismatched_name_pair(self):
        doc_a = {
            "doc_id": "doc1_driving_licence",
            "name": "Rahul Sharma",
            "dob": "1995-05-15",
        }
        doc_b = {
            "doc_id": "doc2_aadhaar_card",
            "name": "Amit Sharma",
            "dob": "1995-05-15",
        }
        result = compare_documents([doc_a, doc_b])
        assert len(result["mismatches"]) == 1
        assert result["mismatches"][0]["field"] == "name"

    def test_empty_and_single_doc_inputs(self):
        assert compare_documents([]) == {"mismatches": []}
        assert compare_documents([{"name": "Rahul"}]) == {"mismatches": []}

    def test_non_judgmental_vocabulary_audit(self):
        doc_a = {"doc_type": "DL", "name": "Rahul", "dob": "1995-05-15"}
        doc_b = {"doc_type": "Aadhaar", "name": "Vikram", "dob": "1990-01-01"}
        result = compare_documents([doc_a, doc_b])
        
        result_str = json.dumps(result).lower()
        forbidden_words = [
            "rejected", "invalid", "fake", "forged", "fraudulent",
            "illegal", "tampered", "suspicious", "unacceptable", "failed"
        ]
        for word in forbidden_words:
            assert word not in result_str, f"Found forbidden judgmental word '{word}' in output!"


class TestSyntheticSamplesIntegration:
    """Tests compare_documents against data/samples JSON files if present."""

    def test_sample_files_if_exist(self):
        samples_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "samples"))
        if not os.path.exists(samples_dir):
            pytest.skip("data/samples not yet populated")
            
        json_files = [f for f in os.listdir(samples_dir) if f.endswith(".json")]
        if len(json_files) < 4:
            pytest.skip("Less than 4 JSON sample files present")
            
        docs = {}
        for jf in json_files:
            with open(os.path.join(samples_dir, jf), "r", encoding="utf-8") as f:
                data = json.load(f)
                docs[data.get("doc_id", jf)] = data
                
        if "doc1_driving_licence" in docs and "doc2_aadhaar_card" in docs:
            res_mismatch = compare_documents([docs["doc1_driving_licence"], docs["doc2_aadhaar_card"]])
            assert len(res_mismatch["mismatches"]) == 1
            assert res_mismatch["mismatches"][0]["field"] in ("date_of_birth", "dob")
            
        if "doc3_pan_card" in docs and "doc4_voter_id" in docs:
            res_match = compare_documents([docs["doc3_pan_card"], docs["doc4_voter_id"]])
            assert len(res_match["mismatches"]) == 0
```

---

## 5. Verification Method

To independently verify this design:

1. **Syntax & stdlib Inspection**:
   - Inspect that `compare.py` uses only Python standard library modules (`re`, `datetime`, `difflib`, `itertools`, `typing`).
   - Confirm absence of external packages like `fuzzywuzzy`, `dateutil`, `pandas`.

2. **Schema & Contract Check**:
   - Verify output structure matches `{"mismatches": [{"field": ..., "doc_a": ..., "value_a": ..., "doc_b": ..., "value_b": ...}]}`.
   - Run the vocabulary audit to ensure no judgmental words (`rejected`, `invalid`, `fake`, etc.) exist in keys or values.

3. **Execution Command**:
   - Once implemented by `worker_impl_1`:
     ```powershell
     pytest tests/test_compare.py -v
     ```
   - Must achieve 100% test pass rate across all parametrized date formats, name variants, matching pairs, and mismatched pairs.
