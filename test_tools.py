import unittest
import os
from tools import extract_document, licence_stats, lookup_rules, calc_fees, build_checklist

class TestTools(unittest.TestCase):
    def test_licence_stats_not_found(self):
        res = licence_stats("UnknownState", "2019-20")
        self.assertEqual(res, {"available": False, "reason": "state did not report this year"})
        
    def test_lookup_rules(self):
        res = lookup_rules("license")
        self.assertIn("text", res)
        
    def test_calc_fees(self):
        res = calc_fees("license", "LMV")
        self.assertIn("total", res)

if __name__ == "__main__":
    unittest.main()
