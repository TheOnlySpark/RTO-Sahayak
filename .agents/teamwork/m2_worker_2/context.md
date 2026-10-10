# Context for m2_worker_2
Workspace: e:\hackthon
Task: Implement Iteration 2 Remediation:
1. Fix compare.py and rto-sahayak/compare.py (add issue_date, expiry_date, valid_till to METADATA_FIELDS; inverted name multiset check).
2. Fix generate_samples.py and rto-sahayak/generate_samples.py (generate into both roots, provide ensure_samples helper).
3. Fix tests/test_compare.py and rto-sahayak/tests/test_compare.py (in-process ensure_samples hook, rigorous PNG magic byte \x89PNG\r\n\x1a\n validation, PIL.Image.open decoding, lifecycle dates test).
4. Generate authentic binary PNG images to data/samples/ and rto-sahayak/data/samples/.
5. Run tests and verify 100% pass rate.
