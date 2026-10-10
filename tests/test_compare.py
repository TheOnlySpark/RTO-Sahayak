"""
Comprehensive unit test suite for document comparison engine (compare.py).

Covers:
- Multi-format date normalization
- Fuzzy name matching with initials, honorifics, and typos
- compare_documents edge cases (empty list, single doc, None)
- Matching document pairs (zero mismatches)
- Mismatched document pairs (factual discrepancy identification)
- Direct verification with 4 synthetic sample JSONs from data/samples/
- Strict non-judgmental vocabulary audit on code and comparison outputs
- Verification of sample PNG and JSON file existence
"""

import glob
import json
import os
import sys
import unittest
import difflib

# Add candidate roots to sys.path
CANDIDATE_ROOTS = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rto-sahayak")),
    os.path.abspath("."),
    os.path.abspath("rto-sahayak"),
]
for root in CANDIDATE_ROOTS:
    if root not in sys.path:
        sys.path.insert(0, root)

from PIL import Image
import generate_samples
import compare
from compare import (
    compare_documents,
    normalize_date,
    normalize_name,
    are_names_matching,
    are_dates_matching,
    get_doc_identifier,
)

# Prohibited judgmental vocabulary across RTO Sahayak outputs
FORBIDDEN_WORDS = {
    "rejected",
    "reject",
    "invalid",
    "fake",
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


def find_samples_dir() -> str:
    """Find data/samples directory from available candidates."""
    for base in CANDIDATE_ROOTS:
        candidate = os.path.join(base, "data", "samples")
        if os.path.isdir(candidate):
            return candidate
    return os.path.abspath("data/samples")


class TestDateNormalization(unittest.TestCase):
    """Test date parsing and normalization across multiple formats."""

    def test_iso_formats(self):
        self.assertEqual(normalize_date("1995-05-15"), "1995-05-15")
        self.assertEqual(normalize_date("1998/11/22"), "1998-11-22")
        self.assertEqual(normalize_date("2001.01.05"), "2001-01-05")

    def test_indian_dmy_formats(self):
        self.assertEqual(normalize_date("15/05/1995"), "1995-05-15")
        self.assertEqual(normalize_date("15-05-1995"), "1995-05-15")
        self.assertEqual(normalize_date("22/11/1998"), "1998-11-22")
        self.assertEqual(normalize_date("05.01.2001"), "2001-01-05")
        self.assertEqual(normalize_date("5/1/2001"), "2001-01-05")

    def test_two_digit_years(self):
        # 95 -> 1995
        self.assertEqual(normalize_date("15/05/95"), "1995-05-15")
        self.assertEqual(normalize_date("22-11-98"), "1998-11-22")
        # 12 -> 2012
        self.assertEqual(normalize_date("10/08/12"), "2012-08-10")

    def test_textual_month_names(self):
        self.assertEqual(normalize_date("15 May 1995"), "1995-05-15")
        self.assertEqual(normalize_date("15-MAY-1995"), "1995-05-15")
        self.assertEqual(normalize_date("15th May 1995"), "1995-05-15")
        self.assertEqual(normalize_date("22nd November 1998"), "1998-11-22")
        self.assertEqual(normalize_date("1st Jan 2000"), "2000-01-01")

    def test_month_day_year_format(self):
        self.assertEqual(normalize_date("May 15, 1995"), "1995-05-15")
        self.assertEqual(normalize_date("May 15 1995"), "1995-05-15")
        self.assertEqual(normalize_date("November 22, 1998"), "1998-11-22")

    def test_empty_and_invalid_dates(self):
        self.assertEqual(normalize_date(""), "")
        self.assertEqual(normalize_date(None), "")
        self.assertEqual(normalize_date("   "), "")
        self.assertEqual(normalize_date("not-a-date"), "not-a-date")

    def test_are_dates_matching_cross_format(self):
        self.assertTrue(are_dates_matching("1995-05-15", "15/05/1995"))
        self.assertTrue(are_dates_matching("1998-11-22", "22/11/1998"))
        self.assertTrue(are_dates_matching("15 May 1995", "1995-05-15"))
        self.assertTrue(are_dates_matching("15th May 1995", "15/05/95"))
        self.assertFalse(are_dates_matching("1995-05-15", "1993-05-15"))


class TestNameNormalizationAndMatching(unittest.TestCase):
    """Test person name cleaning, token matching, initials, and fuzzy comparison."""

    def test_name_normalization_strips_honorifics(self):
        self.assertEqual(normalize_name("Mr. Rahul Sharma"), "rahul sharma")
        self.assertEqual(normalize_name("Shri Rahul Kumar Sharma"), "rahul kumar sharma")
        self.assertEqual(normalize_name("Smt. Priya Patel"), "priya patel")
        self.assertEqual(normalize_name("Dr. Priya S. Patel"), "priya s patel")

    def test_identical_names(self):
        self.assertTrue(are_names_matching("Rahul Kumar Sharma", "Rahul Kumar Sharma"))
        self.assertTrue(are_names_matching("rahul kumar sharma", "RAHUL KUMAR SHARMA"))
        self.assertTrue(are_names_matching("  Rahul   Kumar  Sharma  ", "Rahul Kumar Sharma"))

    def test_inverted_name_orderings(self):
        self.assertTrue(are_names_matching("Patel Priya", "Priya Patel"))
        self.assertTrue(are_names_matching("Sharma Rahul Kumar", "Rahul Kumar Sharma"))


    def test_initials_matching(self):
        # Doc 3 vs Doc 4 match pair
        self.assertTrue(are_names_matching("Priya S. Patel", "Priya Sanjay Patel"))
        self.assertTrue(are_names_matching("Priya Sanjay Patel", "Priya S. Patel"))
        self.assertTrue(are_names_matching("Rahul K. Sharma", "Rahul Kumar Sharma"))
        self.assertTrue(are_names_matching("R. K. Sharma", "Rahul Kumar Sharma"))

    def test_minor_typos(self):
        self.assertTrue(are_names_matching("Rahul Kumar Sharma", "Rahuk Kumar Sharma"))
        self.assertTrue(are_names_matching("Vikram Singh", "Vickram Singh"))

    def test_distinct_individuals_do_not_match(self):
        self.assertFalse(are_names_matching("Rahul Kumar Sharma", "Priya Sanjay Patel"))
        # Same surname, different first name
        self.assertFalse(are_names_matching("Sunil Verma", "Anil Verma"))
        self.assertFalse(are_names_matching("Rohit Kumar", "Mohit Kumar"))

    def test_empty_names(self):
        self.assertTrue(are_names_matching("", ""))
        self.assertFalse(are_names_matching("Rahul", ""))
        self.assertFalse(are_names_matching("", "Rahul"))


class TestDocumentComparison(unittest.TestCase):
    """Test compare_documents function on various inputs."""

    def test_empty_and_single_document(self):
        self.assertEqual(compare_documents([]), {"mismatches": []})
        self.assertEqual(compare_documents(None), {"mismatches": []})
        single_doc = {
            "doc_id": "doc1",
            "full_name": "Rahul Kumar Sharma",
            "dob": "1995-05-15",
        }
        self.assertEqual(compare_documents([single_doc]), {"mismatches": []})

    def test_matching_pair_returns_zero_mismatches(self):
        doc_a = {
            "doc_id": "doc3_pan_card",
            "document_type": "PAN Card",
            "full_name": "Priya S. Patel",
            "date_of_birth": "1998-11-22",
            "father_name": "Sanjay Patel",
            "address": "45, Patel Colony, Synthetic Nagar, Ahmedabad - 380001",
        }
        doc_b = {
            "doc_id": "doc4_voter_id",
            "document_type": "Voter ID Card",
            "full_name": "Priya Sanjay Patel",
            "date_of_birth": "22/11/1998",
            "father_name": "Sanjay Patel",
            "address": "45, Patel Colony, Synthetic Nagar, Ahmedabad - 380001",
        }
        result = compare_documents([doc_a, doc_b])
        self.assertIn("mismatches", result)
        self.assertEqual(len(result["mismatches"]), 0)

    def test_mismatched_dob_pair_reports_factual_difference(self):
        doc_a = {
            "doc_id": "doc1_driving_licence",
            "document_type": "Driving Licence",
            "full_name": "Rahul Kumar Sharma",
            "date_of_birth": "1995-05-15",
            "father_name": "Suresh Kumar Sharma",
            "address": "123, Gandhi Marg, Synthetic City, New Delhi - 110001",
        }
        doc_b = {
            "doc_id": "doc2_aadhaar_card",
            "document_type": "Aadhaar Card",
            "full_name": "Rahul Kumar Sharma",
            "date_of_birth": "1993-05-15",
            "father_name": "Suresh Kumar Sharma",
            "address": "123, Gandhi Marg, Synthetic City, New Delhi - 110001",
        }
        result = compare_documents([doc_a, doc_b])
        self.assertIn("mismatches", result)
        mismatches = result["mismatches"]
        self.assertEqual(len(mismatches), 1)

        m = mismatches[0]
        self.assertEqual(m["field"], "date_of_birth")
        self.assertEqual(m["doc_a"], "doc1_driving_licence")
        self.assertEqual(m["value_a"], "1995-05-15")
        self.assertEqual(m["doc_b"], "doc2_aadhaar_card")
        self.assertEqual(m["value_b"], "1993-05-15")

    def test_field_alias_resolution(self):
        # One uses 'dob' and 'name', the other uses 'date_of_birth' and 'full_name'
        doc_a = {"doc_id": "card_a", "name": "Rahul Sharma", "dob": "1995-05-15"}
        doc_b = {"doc_id": "card_b", "full_name": "Rahul Sharma", "date_of_birth": "1995-05-15"}
        result = compare_documents([doc_a, doc_b])
        self.assertEqual(result["mismatches"], [])

    def test_multi_document_pairwise_comparison(self):
        doc_a = {"doc_id": "doc_a", "full_name": "Rahul Sharma", "dob": "1995-05-15"}
        doc_b = {"doc_id": "doc_b", "full_name": "Rahul Sharma", "dob": "1993-05-15"}
        doc_c = {"doc_id": "doc_c", "full_name": "Priya Patel", "dob": "1998-11-22"}

        result = compare_documents([doc_a, doc_b, doc_c])
        # A vs B has 1 mismatch (dob)
        # A vs C has 2 mismatches (name, dob)
        # B vs C has 2 mismatches (name, dob)
        # Total = 5 mismatches
        self.assertEqual(len(result["mismatches"]), 5)


class TestSyntheticSamplesIntegration(unittest.TestCase):
    """Test loading and comparing the real synthetic sample JSONs from data/samples/."""

    @classmethod
    def setUpClass(cls):
        cls.samples_dir = find_samples_dir()
        try:
            generate_samples.ensure_samples()
        except Exception:
            pass

    def test_samples_exist_and_are_non_empty(self):
        expected_json = [
            "doc1_driving_licence.json",
            "doc2_aadhaar_card.json",
            "doc3_pan_card.json",
            "doc4_voter_id.json",
        ]
        expected_png = [
            "doc1_driving_licence.png",
            "doc2_aadhaar_card.png",
            "doc3_pan_card.png",
            "doc4_voter_id.png",
        ]

        for fname in expected_json:
            fpath = os.path.join(self.samples_dir, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing JSON sample: {fpath}")
            self.assertGreater(os.path.getsize(fpath), 0, f"Empty JSON sample: {fpath}")

        png_magic = b"\x89PNG\r\n\x1a\n"
        for fname in expected_png:
            fpath = os.path.join(self.samples_dir, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing PNG sample: {fpath}")
            # Verify file size is genuine (> 1024 bytes)
            self.assertGreater(
                os.path.getsize(fpath),
                1024,
                f"PNG sample file is suspiciously small (<1024 bytes): {fpath}"
            )

            # a) Verify 8-byte standard PNG magic signature
            with open(fpath, "rb") as bf:
                header = bf.read(8)
            self.assertEqual(
                header,
                png_magic,
                f"File {fname} is not a valid binary PNG. Expected header {png_magic!r}, got {header!r}"
            )

            # b) Open each file with PIL.Image.open: assert img.format == "PNG", assert img.size == (800, 500), assert img.load() succeeds
            with Image.open(fpath) as img:
                self.assertEqual(img.format, "PNG", f"Image format for {fname} is {img.format}, expected PNG")
                self.assertEqual(
                    img.size,
                    (800, 500),
                    f"Image dimensions for {fname} are {img.size}, expected (800, 500)"
                )
                pixels = img.load()
                self.assertIsNotNone(pixels, f"Corrupted pixel raster data in image: {fname}")

    def test_sample_jsons_schema_and_synthetic_flags(self):
        for json_path in glob.glob(os.path.join(self.samples_dir, "*.json")):
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertTrue(data.get("is_synthetic"), f"Missing is_synthetic: {json_path}")
            self.assertIn("doc_id", data)
            self.assertIn("document_type", data)
            self.assertIn("document_number", data)
            self.assertIn("full_name", data)
            self.assertIn("date_of_birth", data)
            self.assertIn("disclaimer", data)
            self.assertIn("Final decision rests with the RTO officer.", data["disclaimer"])

    def test_compare_doc1_and_doc2_from_disk(self):
        with open(os.path.join(self.samples_dir, "doc1_driving_licence.json"), "r", encoding="utf-8") as f:
            doc1 = json.load(f)
        with open(os.path.join(self.samples_dir, "doc2_aadhaar_card.json"), "r", encoding="utf-8") as f:
            doc2 = json.load(f)

        result = compare_documents([doc1, doc2])
        mismatches = result["mismatches"]
        self.assertEqual(len(mismatches), 1)
        self.assertEqual(mismatches[0]["field"], "date_of_birth")
        self.assertEqual(mismatches[0]["value_a"], "1995-05-15")
        self.assertEqual(mismatches[0]["value_b"], "1993-05-15")

    def test_compare_doc3_and_doc4_from_disk(self):
        with open(os.path.join(self.samples_dir, "doc3_pan_card.json"), "r", encoding="utf-8") as f:
            doc3 = json.load(f)
        with open(os.path.join(self.samples_dir, "doc4_voter_id.json"), "r", encoding="utf-8") as f:
            doc4 = json.load(f)

        result = compare_documents([doc3, doc4])
        self.assertEqual(result["mismatches"], [])

    def test_lifecycle_dates_ignored_in_comparison(self):
        """Verify that differing document issue/expiry dates between matching documents do not produce false mismatches."""
        doc_a = {
            "doc_id": "doc_a",
            "full_name": "Rahul Sharma",
            "dob": "1995-05-15",
            "issue_date": "2015-06-20",
            "expiry_date": "2035-05-14",
        }
        doc_b = {
            "doc_id": "doc_b",
            "full_name": "Rahul Sharma",
            "dob": "1995-05-15",
            "issue_date": "2012-08-10",
            "expiry_date": "2030-01-01",
        }
        result = compare_documents([doc_a, doc_b])
        self.assertEqual(result["mismatches"], [])



class TestNonJudgmentalVocabularyAudit(unittest.TestCase):
    """Audit compare.py code and compare_documents outputs to guarantee non-judgmental language."""

    def test_compare_module_source_has_no_forbidden_words(self):
        source_path = inspect_path = getattr(compare, "__file__", None)
        if not source_path or not os.path.exists(source_path):
            source_path = os.path.abspath("compare.py")

        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read().lower()

        found_violations = []
        for word in FORBIDDEN_WORDS:
            # Word boundary search to avoid false positives on subwords
            import re
            if re.search(r'\b' + re.escape(word) + r'\b', content):
                found_violations.append(word)

        self.assertEqual(
            found_violations,
            [],
            f"compare.py contains prohibited judgmental vocabulary: {found_violations}",
        )

    def test_comparison_result_payload_has_no_forbidden_words(self):
        doc_a = {"doc_id": "doc_a", "name": "Rahul Sharma", "dob": "1995-05-15"}
        doc_b = {"doc_id": "doc_b", "name": "Priya Patel", "dob": "1993-05-15"}
        result = compare_documents([doc_a, doc_b])

        result_str = json.dumps(result).lower()
        found_violations = []
        for word in FORBIDDEN_WORDS:
            import re
            if re.search(r'\b' + re.escape(word) + r'\b', result_str):
                found_violations.append(word)

        self.assertEqual(
            found_violations,
            [],
            f"compare_documents returned output containing judgmental vocabulary: {found_violations}",
        )


if __name__ == "__main__":
    unittest.main()
