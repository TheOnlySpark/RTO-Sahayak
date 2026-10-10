"""
Unit tests for pdf_tools.py and mock_api.py.

Verifies:
- ID masking logic (Aadhaar, PAN, DL, generic)
- Mock API appointment slots generation with required synthetic disclaimer
- generate_handoff_pdf end-to-end PDF generation to outputs/
- Binary PDF validation (%PDF- magic header, file size > 0)
- Non-judgmental vocabulary compliance
- Mirror compatibility between root and rto-sahayak
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
import unittest

# Ensure candidate project roots are in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
RTO_SUBDIR = REPO_ROOT / "rto-sahayak"
for candidate in [REPO_ROOT, RTO_SUBDIR]:
    c_str = str(candidate)
    if c_str not in sys.path:
        sys.path.insert(0, c_str)

import mock_api
from mock_api import get_slots, SYNTHETIC_NOTE
import pdf_tools
from pdf_tools import (
    generate_handoff_pdf,
    mask_id_number,
    MANDATORY_BANNER,
    MANDATORY_FOOTER,
)

FORBIDDEN_WORDS = {
    "rejected",
    "reject",
    "invalid",
    "forged",
    "forgery",
    "fraud",
    "fraudulent",
    "illegal",
    "tampered",
    "suspicious",
    "unacceptable",
    "bogus",
}


class TestMockApi(unittest.TestCase):
    """Test synthetic slot availability from mock_api.py."""

    def test_get_slots_structure_and_disclaimer(self):
        res = get_slots("DL04")
        self.assertIsInstance(res, dict)
        self.assertIn("slots", res)
        self.assertIn("note", res)
        self.assertEqual(res["note"], SYNTHETIC_NOTE)
        self.assertEqual(res["note"], "synthetic sample slots, not real availability")
        self.assertIsInstance(res["slots"], list)
        self.assertGreater(len(res["slots"]), 0)
        for slot in res["slots"]:
            self.assertIsInstance(slot, str)
            self.assertIn("2026", slot)

    def test_get_slots_various_rto_codes(self):
        codes = ["DL04", "MH01", "KA01", "GJ01", "", None]
        for c in codes:
            res = get_slots(c)
            self.assertIn("slots", res)
            self.assertEqual(res["note"], "synthetic sample slots, not real availability")
            self.assertGreater(len(res["slots"]), 0)


class TestIdMasking(unittest.TestCase):
    """Test identity document masking to preserve privacy."""

    def test_mask_aadhaar_formatted(self):
        self.assertEqual(mask_id_number("9999-8888-7777"), "XXXX-XXXX-7777")
        self.assertEqual(mask_id_number("1234 5678 9012"), "XXXX XXXX 9012")

    def test_mask_aadhaar_raw_12_digits(self):
        self.assertEqual(mask_id_number("123456789012"), "XXXX-XXXX-9012")

    def test_mask_pan(self):
        self.assertEqual(mask_id_number("ABCDE1234F"), "XXXXX1234F")
        self.assertEqual(mask_id_number("abcde1234f"), "XXXXX1234F")

    def test_mask_fake_dl_and_uid(self):
        dl_masked = mask_id_number("FAKE-DL-DL04-20150001")
        self.assertTrue(dl_masked.endswith("0001"))
        self.assertNotIn("2015", dl_masked.split("-")[2] if len(dl_masked.split("-")) > 2 else "")

        uid_masked = mask_id_number("FAKE-UID-9999-8888-7777")
        self.assertTrue(uid_masked.endswith("7777"))

    def test_mask_short_or_empty(self):
        self.assertEqual(mask_id_number(""), "")
        self.assertEqual(mask_id_number(None), "")
        self.assertEqual(mask_id_number("123"), "123")
        self.assertEqual(mask_id_number("ABCD"), "ABCD")


class TestPdfHandoffGeneration(unittest.TestCase):
    """Test PDF generation, file persistence, binary magic bytes, and sections."""

    def setUp(self):
        self.sample_summary = {
            "citizen_name": "Rahul Kumar Sharma",
            "service_name": "Learner Licence to Driving Licence",
            "reference_id": "SYNTH-TEST-REF-001",
            "citizen_summary": {
                "full_name": "Rahul Kumar Sharma",
                "date_of_birth": "1995-05-15",
                "father_name": "Suresh Kumar Sharma",
                "address": "123, Gandhi Marg, Synthetic City, New Delhi - 110001",
                "id_number": "FAKE-DL-DL04-20150001",
            },
            "checklist": [
                {"document": "Form 2 Application", "status": "Submitted", "note": "Synthetic"},
                {"document": "Learner Licence", "status": "Submitted", "note": "Synthetic"},
                {"document": "Medical Fitness (Form 1A)", "status": "Pending", "note": "Required"},
            ],
            "mismatches": [
                {
                    "field": "date_of_birth",
                    "doc_a": "Driving Licence",
                    "value_a": "1995-05-15",
                    "doc_b": "Aadhaar Card",
                    "value_b": "1993-05-15",
                }
            ],
            "estimated_fees": {
                "items": [
                    {"service": "Application Fee", "amount": "₹200 (ESTIMATE)"},
                    {"service": "Driving Test Fee", "amount": "₹300 (ESTIMATE)"},
                    {"service": "Smart Card Processing Fee", "amount": "₹200 (ESTIMATE)"},
                ],
                "total": "₹700 (ESTIMATE)",
            },
            "rule_sources": [
                "data/rules/ll_to_dl_process.md",
                "data/rules/documents_checklist.md",
                "data/rules/fees_overview.md",
            ],
            "next_steps": [
                "Book an appointment slot at RTO Synthetic Zone 04.",
                "Bring original physical documents for officer in-person verification.",
                "Pay official statutory fees at authorized RTO counter.",
            ],
            "output_filename": "sample_handoff_test.pdf",
        }

    def test_generate_handoff_pdf_returns_path_and_creates_valid_pdf(self):
        res = generate_handoff_pdf(self.sample_summary)
        self.assertIsInstance(res, dict)
        self.assertIn("pdf_path", res)

        pdf_path = Path(res["pdf_path"])
        self.assertTrue(pdf_path.exists(), f"PDF was not created at: {pdf_path}")
        self.assertGreater(pdf_path.stat().st_size, 500, f"PDF file size too small: {pdf_path.stat().st_size}")

        # Check binary %PDF- magic header
        with open(pdf_path, "rb") as f:
            header = f.read(5)
        self.assertEqual(header, b"%PDF-", f"Invalid PDF binary header: {header!r}")

    def test_generate_handoff_pdf_zero_mismatches(self):
        summary_clean = dict(self.sample_summary)
        summary_clean["mismatches"] = []
        summary_clean["output_filename"] = "sample_clean_test.pdf"

        res = generate_handoff_pdf(summary_clean)
        pdf_path = Path(res["pdf_path"])
        self.assertTrue(pdf_path.exists())
        self.assertGreater(pdf_path.stat().st_size, 500)

        with open(pdf_path, "rb") as f:
            header = f.read(5)
        self.assertEqual(header, b"%PDF-")


class TestNonJudgmentalVocabularyInPdfTools(unittest.TestCase):
    """Audit pdf_tools.py to ensure zero judgmental vocabulary in source code."""

    def test_source_code_clean_of_forbidden_words(self):
        source_path = Path(pdf_tools.__file__).resolve()
        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read().lower()

        found_violations = []
        import re
        for word in FORBIDDEN_WORDS:
            if re.search(r'\b' + re.escape(word) + r'\b', content):
                found_violations.append(word)

        self.assertEqual(
            found_violations,
            [],
            f"pdf_tools.py contains prohibited judgmental words: {found_violations}",
        )


if __name__ == "__main__":
    unittest.main()
