"""
Adversarial Stress Test Suite for Document Comparison Engine (compare.py).

Written by m2_challenger_1 (Empirical Challenger) to aggressively test:
1. Date Normalization across edge formats, 2-digit years, and invalid inputs.
2. Fuzzy Name Matching across honorifics, whitespace, initials, typos, and negative pairs.
3. Structural Edge Cases (empty lists, single doc, matching pairs, multi-field mismatches).
4. Strict Non-Judgmental Vocabulary Audit on outputs and code.
"""

import json
import os
import sys
import unittest
import difflib

# Add repository root to path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import compare
from compare import (
    compare_documents,
    normalize_date,
    normalize_name,
    are_names_matching,
    are_dates_matching,
    get_doc_identifier,
)

FORBIDDEN_WORDS = [
    "rejected",
    "reject",
    "invalid",
    "fake",
    "forged",
    "fraudulent",
    "forgery",
    "fraud",
    "tampered",
    "suspicious",
    "bogus",
]


class TestAdversarialDateNormalization(unittest.TestCase):
    """Stress testing date normalization engine with edge cases and malformed inputs."""

    def test_iso_variations(self):
        self.assertEqual(normalize_date("1995-05-15"), "1995-05-15")
        self.assertEqual(normalize_date("1995/05/15"), "1995-05-15")
        self.assertEqual(normalize_date("1995.05.15"), "1995-05-15")
        self.assertEqual(normalize_date("  1995-05-15  "), "1995-05-15")

    def test_dmy_delimiters_and_padding(self):
        self.assertEqual(normalize_date("15/05/1995"), "1995-05-15")
        self.assertEqual(normalize_date("15-05-1995"), "1995-05-15")
        self.assertEqual(normalize_date("15.05.1995"), "1995-05-15")
        # Single digit day and month
        self.assertEqual(normalize_date("5/5/1995"), "1995-05-05")
        self.assertEqual(normalize_date("05/05/1995"), "1995-05-05")

    def test_textual_and_ordinal_formats(self):
        self.assertEqual(normalize_date("15 May 1995"), "1995-05-15")
        self.assertEqual(normalize_date("15th May 1995"), "1995-05-15")
        self.assertEqual(normalize_date("1st January 2000"), "2000-01-01")
        self.assertEqual(normalize_date("2nd February 2001"), "2001-02-02")
        self.assertEqual(normalize_date("3rd March 1990"), "1990-03-03")
        self.assertEqual(normalize_date("May 15 1995"), "1995-05-15")
        self.assertEqual(normalize_date("May 15, 1995"), "1995-05-15")
        self.assertEqual(normalize_date("15-MAY-1995"), "1995-05-15")
        self.assertEqual(normalize_date("15-may-1995"), "1995-05-15")

    def test_two_digit_years(self):
        # 1900s vs 2000s pivot
        self.assertEqual(normalize_date("15/05/95"), "1995-05-15")
        self.assertEqual(normalize_date("15-05-95"), "1995-05-15")
        self.assertEqual(normalize_date("10/08/12"), "2012-08-10")
        self.assertEqual(normalize_date("01/01/24"), "2024-01-01")

    def test_invalid_and_unparseable_dates_graceful_handling(self):
        # Must not raise exceptions
        self.assertEqual(normalize_date(""), "")
        self.assertEqual(normalize_date(None), "")
        self.assertEqual(normalize_date("   "), "")
        self.assertEqual(normalize_date(12345), "")
        self.assertEqual(normalize_date("not-a-date"), "not-a-date")
        self.assertEqual(normalize_date("31/02/1995"), "31/02/1995")
        self.assertEqual(normalize_date("99/99/9999"), "99/99/9999")

    def test_cross_format_equality(self):
        self.assertTrue(are_dates_matching("1995-05-15", "15/05/1995"))
        self.assertTrue(are_dates_matching("15 May 1995", "15th May 1995"))
        self.assertTrue(are_dates_matching("15-MAY-1995", "15/05/95"))
        self.assertTrue(are_dates_matching("May 15, 1995", "1995.05.15"))
        # Genuine difference
        self.assertFalse(are_dates_matching("1995-05-15", "1993-05-15"))
        self.assertFalse(are_dates_matching("15/05/1995", "16/05/1995"))


class TestAdversarialNameMatching(unittest.TestCase):
    """Stress testing fuzzy name matching engine with tricky variations and negative controls."""

    def test_identical_names_case_and_whitespace(self):
        self.assertTrue(are_names_matching(
            " rahul  kumar  sharma ",
            "RAHUL KUMAR SHARMA"
        ))
        self.assertTrue(are_names_matching(
            "\tpriya   patel\n",
            "PRIYA PATEL"
        ))

    def test_honorifics_stripping(self):
        self.assertTrue(are_names_matching("Mr. Rahul Sharma", "Rahul Sharma"))
        self.assertTrue(are_names_matching("Ms. Priya Patel", "Priya Patel"))
        self.assertTrue(are_names_matching("Dr. Rahul Sharma", "Rahul Sharma"))
        self.assertTrue(are_names_matching("Shri Suresh Sharma", "Suresh Sharma"))
        self.assertTrue(are_names_matching("Smt. Sunita Devi", "Sunita Devi"))
        self.assertTrue(are_names_matching("Dr. Prof. Priya Patel", "Priya Patel"))

    def test_initials_and_token_expansions(self):
        self.assertTrue(are_names_matching("Priya S. Patel", "Priya Sanjay Patel"))
        self.assertTrue(are_names_matching("Priya Sanjay Patel", "Priya S. Patel"))
        self.assertTrue(are_names_matching("R. K. Sharma", "Rahul Kumar Sharma"))
        self.assertTrue(are_names_matching("Rahul Kumar Sharma", "R. K. Sharma"))
        self.assertTrue(are_names_matching("R. Kumar Sharma", "Rahul K. Sharma"))

    def test_typos_in_tokens(self):
        self.assertTrue(are_names_matching("Rahul Sharme", "Rahul Sharma"))
        self.assertTrue(are_names_matching("Rahul Kumar Sharma", "Rahuk Kumar Sharma"))
        self.assertTrue(are_names_matching("Vikram Singh", "Vickram Singh"))

    def test_negative_controls_completely_different_names(self):
        # Must strictly NOT match
        self.assertFalse(are_names_matching("Rahul Kumar Sharma", "Priya Sanjay Patel"))
        self.assertFalse(are_names_matching("Rahul Sharma", "Priya Patel"))
        self.assertFalse(are_names_matching("Aarav Gupta", "Vivaan Sharma"))
        self.assertFalse(are_names_matching("Amit Shah", "Rajesh Patel"))

    def test_negative_controls_shared_surnames_different_first_names(self):
        # Relatives sharing surname must not falsely match
        self.assertFalse(are_names_matching("Sunil Verma", "Anil Verma"))
        self.assertFalse(are_names_matching("Rohit Kumar", "Mohit Kumar"))
        self.assertFalse(are_names_matching("Suresh Sharma", "Ramesh Sharma"))

    def test_inverted_name_orderings(self):
        # Inverted name ordering: "Patel Priya" vs "Priya Patel"
        self.assertTrue(are_names_matching("Patel Priya", "Priya Patel"))
        self.assertTrue(are_names_matching("Priya Patel", "Patel Priya"))
        # Inverted name ordering: "Sharma Rahul Kumar" vs "Rahul Kumar Sharma"
        self.assertTrue(are_names_matching("Sharma Rahul Kumar", "Rahul Kumar Sharma"))
        self.assertTrue(are_names_matching("Rahul Kumar Sharma", "Sharma Rahul Kumar"))



class TestAdversarialStructuralEdgeCases(unittest.TestCase):
    """Stress testing structural variations, missing fields, and multiple mismatches."""

    def test_empty_docs_list(self):
        self.assertEqual(compare_documents([]), {"mismatches": []})

    def test_single_doc(self):
        doc = {"doc_id": "doc1", "name": "Rahul Sharma", "dob": "1995-05-15"}
        self.assertEqual(compare_documents([doc]), {"mismatches": []})

    def test_none_input(self):
        self.assertEqual(compare_documents(None), {"mismatches": []})

    def test_matching_pair(self):
        doc_a = {
            "doc_id": "doc_a",
            "full_name": "Priya S. Patel",
            "date_of_birth": "1998-11-22",
            "father_name": "Sanjay Patel",
        }
        doc_b = {
            "doc_id": "doc_b",
            "applicant_name": "Priya Sanjay Patel",
            "dob": "22/11/1998",
            "father": "Sanjay Patel",
        }
        result = compare_documents([doc_a, doc_b])
        self.assertEqual(result, {"mismatches": []})

    def test_multiple_mismatches_across_multiple_fields(self):
        doc_a = {
            "doc_id": "licence_1",
            "full_name": "Rahul Sharma",
            "date_of_birth": "1995-05-15",
            "father_name": "Suresh Sharma",
            "address": "Delhi",
        }
        doc_b = {
            "doc_id": "licence_2",
            "full_name": "Priya Patel",
            "date_of_birth": "1998-11-22",
            "father_name": "Sanjay Patel",
            "address": "Ahmedabad",
        }
        result = compare_documents([doc_a, doc_b])
        mismatches = result["mismatches"]
        self.assertEqual(len(mismatches), 4)

        mismatched_fields = {m["field"] for m in mismatches}
        self.assertEqual(mismatched_fields, {"address", "date_of_birth", "father_name", "full_name"})

        for m in mismatches:
            self.assertIn("field", m)
            self.assertIn("doc_a", m)
            self.assertIn("value_a", m)
            self.assertIn("doc_b", m)
            self.assertIn("value_b", m)

    def test_duplicate_doc_identifiers_disambiguated(self):
        doc_a = {"doc_id": "same_id", "dob": "1995-05-15"}
        doc_b = {"doc_id": "same_id", "dob": "1993-05-15"}
        result = compare_documents([doc_a, doc_b])
        self.assertEqual(len(result["mismatches"]), 1)
        m = result["mismatches"][0]
        self.assertNotEqual(m["doc_a"], m["doc_b"])
        self.assertIn("(doc 1)", m["doc_a"])
        self.assertIn("(doc 2)", m["doc_b"])

    def test_non_dict_and_none_values_handling(self):
        doc_a = {"doc_id": "doc_a", "dob": None, "name": "Rahul Sharma"}
        doc_b = {"doc_id": "doc_b", "dob": "1995-05-15", "name": "Rahul Sharma"}
        # None dob in doc_a should be ignored, leaving zero common fields for dob
        result = compare_documents([doc_a, doc_b])
        self.assertEqual(result["mismatches"], [])

        # Non-dict element in docs list should not crash
        result_with_bad_elem = compare_documents([doc_a, "bad_entry", doc_b])
        self.assertIn("mismatches", result_with_bad_elem)

    def test_lifecycle_field_filtering_zero_mismatches(self):
        """Verify that documents with identical identity fields but different issue_date or expiry_date produce ZERO mismatches!"""
        doc_a = {
            "doc_id": "doc_licence",
            "name": "Rahul Kumar Sharma",
            "dob": "15/05/1995",
            "issue_date": "2015-01-10",
            "expiry_date": "2035-01-09",
            "valid_till": "2035-01-09",
            "valid_upto": "2035-01-09",
            "date_of_issue": "2015-01-10",
        }
        doc_b = {
            "doc_id": "doc_aadhaar",
            "full_name": "Sharma Rahul Kumar",
            "date_of_birth": "1995-05-15",
            "issue_date": "2018-06-20",
            "expiry_date": "2028-06-19",
            "valid_till": "2028-06-19",
            "valid_upto": "2028-06-19",
            "date_of_issue": "2018-06-20",
        }
        result = compare_documents([doc_a, doc_b])
        self.assertEqual(
            result["mismatches"],
            [],
            f"Expected 0 mismatches for documents with differing lifecycle dates, got: {result['mismatches']}"
        )



class TestAdversarialVocabularyAudit(unittest.TestCase):
    """Rigorous audit asserting zero occurrences of judgmental words in output payload."""

    def test_audit_mismatch_payload_for_judgmental_words(self):
        doc_a = {
            "doc_id": "doc_a",
            "name": "Rahul Sharma",
            "dob": "1995-05-15",
            "father": "Suresh Sharma",
        }
        doc_b = {
            "doc_id": "doc_b",
            "name": "Vikram Singh",
            "dob": "1993-05-15",
            "father": "Mahesh Singh",
        }
        result = compare_documents([doc_a, doc_b])

        dumped = json.dumps(result).lower()
        for forbidden in FORBIDDEN_WORDS:
            self.assertNotIn(
                forbidden,
                dumped,
                f"Prohibited judgmental term '{forbidden}' detected in comparison output"
            )


if __name__ == "__main__":
    unittest.main()
