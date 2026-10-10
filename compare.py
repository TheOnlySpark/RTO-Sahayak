"""
Document Comparison Engine for RTO Sahayak.

Compares citizen identity fields (name, date of birth, etc.) across
extracted document records to identify factual discrepancies.

Strictly non-judgmental: reports factual differences without declaring
documents deficient or unsuitable. Final decision rests with the RTO officer.
"""

from __future__ import annotations

import difflib
import itertools
import re
from datetime import datetime
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
    "issued_on", "issue_dt", "expiry_dt",
}


def normalize_date(date_str: Any) -> str:
    """
    Normalise date string to canonical ISO YYYY-MM-DD format.

    Supports:
    - YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD
    - DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY
    - DD/MM/YY, DD-MM-YY, DD.MM.YY (with century pivot)
    - DD Month YYYY (e.g., 15 May 1995, 15-MAY-1995, 15th May 1995)
    - Month DD, YYYY (e.g., May 15, 1995, May 15 1995)
    """
    if not date_str or not isinstance(date_str, str):
        return ""

    raw = date_str.strip()
    if not raw:
        return ""

    # Strip ordinals (1st, 2nd, 3rd, 15th) and commas
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
        year = 2000 + year_2d if year_2d <= (current_year % 100) else 1900 + year_2d
        try:
            return datetime(year, month, day).strftime("%Y-%m-%d")
        except ValueError:
            pass

    # Pattern D: DD Month YYYY (e.g., 15 May 1995, 15-May-1995)
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

    # Pattern E: Month DD YYYY (e.g., May 15 1995)
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
    Normalise person name by lowercasing, removing honorifics,
    expanding punctuation, and collapsing whitespace.
    """
    if not name_str or not isinstance(name_str, str):
        return ""

    text = re.sub(r'[\.,_\-]', ' ', name_str.lower())
    tokens = text.strip().split()

    while tokens and tokens[0] in HONORIFICS:
        tokens.pop(0)

    return " ".join(tokens)


def are_names_matching(name_a: str, name_b: str, threshold: float = 0.85) -> bool:
    """
    Compare two personal names using normalization, initials expansion,
    and token similarity.
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

    # 2. Token multiset match (handles inverted name order like "Patel Priya" vs "Priya Patel")
    if sorted(tokens_a) == sorted(tokens_b):
        return True

    # 3. Token initials match when token counts are equal (e.g. "Priya S. Patel" vs "Priya Sanjay Patel")
    if len(tokens_a) == len(tokens_b) and len(tokens_a) > 1:
        match_all = True
        has_full_token_match = False
        for ta, tb in zip(tokens_a, tokens_b):
            if ta == tb:
                has_full_token_match = True
            elif (len(ta) == 1 and tb.startswith(ta)) or (len(tb) == 1 and ta.startswith(tb)):
                continue
            elif ta[0] == tb[0] and len(ta) >= 4 and len(tb) >= 4 and difflib.SequenceMatcher(None, ta, tb).ratio() >= 0.80:
                has_full_token_match = True
            else:
                match_all = False
                break
        if match_all and has_full_token_match:
            return True

    # 3. First and last tokens match, with middle initial/token expansion
    if len(tokens_a) > 1 and len(tokens_b) > 1:
        first_a, last_a = tokens_a[0], tokens_a[-1]
        first_b, last_b = tokens_b[0], tokens_b[-1]
        first_match = (first_a == first_b) or (len(first_a) == 1 and first_b.startswith(first_a)) or (len(first_b) == 1 and first_a.startswith(first_b))
        last_match = (last_a == last_b)
        if first_match and last_match:
            return True

    # 4. Token-level similarity check ensuring first characters match
    if tokens_a and tokens_b:
        if tokens_a[0][0] == tokens_b[0][0] and tokens_a[-1][0] == tokens_b[-1][0]:
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
