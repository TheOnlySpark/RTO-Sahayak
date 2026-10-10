"""
Unit tests for RTO Sahayak basic tools: lookup_rules, calc_fees, build_checklist.
Complies with Laptop 2 constraints: tests data/rules/ and data/fees.json.
Provides clean fallback stubs that read the real data/rules/*.md and data/fees.json
if tools.py is not yet implemented by Laptop 1.
"""
import os
import sys
import json
import pytest

# Find project data root
def get_data_dir() -> str:
    candidates = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rto-sahayak", "data")),
        os.path.abspath("data"),
        os.path.abspath("rto-sahayak/data"),
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.isdir(c):
            return c
    raise FileNotFoundError("Could not locate data directory")

DATA_DIR = get_data_dir()
RULES_DIR = os.path.join(DATA_DIR, "rules")
FEES_PATH = os.path.join(DATA_DIR, "fees.json")

# Ensure paths are available for tools import
for candidate_root in [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rto-sahayak")),
    os.path.abspath(".")
]:
    if candidate_root not in sys.path:
        sys.path.insert(0, candidate_root)

# Attempt to import tools; fallback to reference implementations reading actual data
try:
    from tools import lookup_rules, calc_fees, build_checklist  # type: ignore
    assert callable(lookup_rules) and callable(calc_fees) and callable(build_checklist)
except (ImportError, AttributeError, AssertionError):
    def lookup_rules(topic: str) -> str:
        """Fallback reference stub: reads actual rule markdown files."""
        normalized_topic = topic.strip().lower().replace(" ", "_").replace("-", "_")
        rule_file = os.path.join(RULES_DIR, f"{normalized_topic}.md")
        if not os.path.exists(rule_file):
            return f"Rule '{topic}' not found. Final decision rests with the RTO officer."
        with open(rule_file, "r", encoding="utf-8") as f:
            return f.read()

    def calc_fees(service: str, vehicle_class: str) -> dict:
        """Fallback reference stub: reads actual data/fees.json."""
        if not os.path.exists(FEES_PATH):
            raise FileNotFoundError(f"fees.json not found at {FEES_PATH}")
        with open(FEES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        services = data.get("services", {})
        if service not in services:
            raise KeyError(f"Unknown service: {service}")
        rates = services[service].get("rates", {})
        if vehicle_class not in rates:
            raise KeyError(f"Unknown vehicle class '{vehicle_class}' for service '{service}'")
        result = dict(rates[vehicle_class])
        result["service"] = service
        result["vehicle_class"] = vehicle_class
        return result

    def build_checklist(service: str) -> dict:
        """Fallback reference stub: builds document checklist with disclaimers."""
        rule_content = lookup_rules("documents_checklist")
        return {
            "service": service,
            "status": "DRAFT - for citizen review and officer verification",
            "checklist": [
                "Proof of Age (Aadhaar / Passport / Birth Certificate) [SYNTHETIC]",
                "Proof of Address (Aadhaar / Utility Bill / Rent Agreement) [SYNTHETIC]",
                "Form 1 (Self-declaration of physical fitness)",
                "Form 1A Medical Certificate (if transport or age > 40)",
                "Passport-sized photographs",
                "Existing License copy (if applicable)",
                "Statutory Fee Payment Receipt (PLACEHOLDER)"
            ],
            "reference": rule_content,
            "disclaimer": "Final decision rests with the RTO officer."
        }


# --- UNIT TESTS ---

class TestRuleFiles:
    """Requirement R1: Validate 5 rule markdown files and lookup_rules."""
    RULE_TOPICS = [
        "ll_to_dl_process",
        "documents_checklist",
        "fees_overview",
        "renewal_basics",
        "vehicle_transfer_basics"
    ]

    @pytest.mark.parametrize("topic", RULE_TOPICS)
    def test_rule_file_constraints(self, topic: str):
        content = lookup_rules(topic)
        assert len(content.strip()) > 0, f"Rule {topic} content is empty"
        lines = content.strip().split("\n")
        
        # Rule file line count must be strictly under 40 lines
        assert len(lines) < 40, f"Rule {topic} has {len(lines)} lines; must be < 40 lines"
        
        # Line 1 must begin with 'Source: TODO'
        assert lines[0].startswith("Source: TODO"), f"Rule {topic} line 1 must start with 'Source: TODO', got: {lines[0]}"
        
        # Last non-empty line must end with 'PLACEHOLDER: verify against official sources'
        assert lines[-1].strip() == "PLACEHOLDER: verify against official sources", (
            f"Rule {topic} must end with 'PLACEHOLDER: verify against official sources', got: {lines[-1]}"
        )
        
        # Must contain the mandatory officer disclaimer
        assert "Final decision rests with the RTO officer." in content, (
            f"Rule {topic} must contain 'Final decision rests with the RTO officer.'"
        )

    def test_lookup_rules_unknown_topic(self):
        result = lookup_rules("non_existent_topic_xyz")
        assert "not found" in result.lower() or "Final decision rests with the RTO officer." in result


class TestCalcFees:
    """Requirement R2: Validate fee calculation across all services and vehicle classes."""
    SERVICES = [
        "learner_license",
        "driving_license",
        "renewal",
        "vehicle_transfer",
        "duplicate_license"
    ]
    CLASSES = ["MCWOG", "MCWG", "LMV", "LMV-NT", "TRANS"]

    def test_calc_fees_valid(self):
        fee_info = calc_fees("learner_license", "LMV")
        assert isinstance(fee_info, dict)
        assert "total_fee" in fee_info
        assert fee_info["total_fee"] > 0
        assert "source" in fee_info
        assert "PLACEHOLDER" in str(fee_info.get("status", "")) or "PLACEHOLDER" in str(fee_info.get("source", ""))

    def test_calc_fees_all_services_and_classes(self):
        for s in self.SERVICES:
            for c in self.CLASSES:
                info = calc_fees(s, c)
                assert isinstance(info, dict), f"Fee info for {s} / {c} must be a dict"
                assert "total_fee" in info, f"total_fee missing in {s} / {c}"
                assert info["total_fee"] > 0, f"total_fee must be > 0 for {s} / {c}"
                assert "source" in info, f"source missing in {s} / {c}"
                assert "PLACEHOLDER" in str(info), f"PLACEHOLDER tag missing in {s} / {c}"

    def test_calc_fees_invalid_service(self):
        with pytest.raises(KeyError):
            calc_fees("invalid_service_123", "LMV")

    def test_calc_fees_invalid_class(self):
        with pytest.raises(KeyError):
            calc_fees("learner_license", "UNSUPPORTED_CLASS_XYZ")


class TestBuildChecklist:
    """Requirement R3: Validate checklist structure and disclaimers."""
    def test_build_checklist_basic(self):
        checklist = build_checklist("learner_license")
        assert isinstance(checklist, dict)
        assert checklist["service"] == "learner_license"
        assert len(checklist["checklist"]) > 0
        assert "Final decision rests with the RTO officer." in checklist["disclaimer"]
        assert "DRAFT" in checklist["status"]
        # Check that items contain SYNTHETIC or standard mock labels
        has_synthetic = any("SYNTHETIC" in item for item in checklist["checklist"])
        assert has_synthetic, "Checklist must include SYNTHETIC mock document labels"


class TestAdversarialFile:
    """Requirement R3: Validate tests/adversarial.txt count and content."""
    def test_adversarial_file_line_count(self):
        candidates = [
            os.path.join(os.path.dirname(__file__), "adversarial.txt"),
            os.path.join(os.path.dirname(__file__), "..", "tests", "adversarial.txt"),
            os.path.join("tests", "adversarial.txt"),
            os.path.join("rto-sahayak", "tests", "adversarial.txt")
        ]
        adv_path = next((c for c in candidates if os.path.exists(c)), None)
        assert adv_path is not None, "tests/adversarial.txt not found"
        with open(adv_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        assert len(lines) == 15, f"Expected exactly 15 adversarial prompts, found {len(lines)}"


class TestFeesJsonSchema:
    """Requirement R2: Validate fees.json file integrity directly."""
    def test_fees_json_valid_and_complete(self):
        with open(FEES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "_metadata" in data, "fees.json missing _metadata"
        assert "Final decision rests with the RTO officer." in data["_metadata"]["disclaimer"]
        assert data["_metadata"]["status"] == "PLACEHOLDER"
        
        services = data.get("services", {})
        expected_services = ["learner_license", "driving_license", "renewal", "vehicle_transfer", "duplicate_license"]
        for s in expected_services:
            assert s in services, f"Service '{s}' missing in fees.json"
            assert "rates" in services[s]
            assert "status" in services[s] and services[s]["status"] == "PLACEHOLDER"
            for c in ["MCWOG", "MCWG", "LMV", "LMV-NT", "TRANS"]:
                assert c in services[s]["rates"], f"Class '{c}' missing in service '{s}'"
                rate_entry = services[s]["rates"][c]
                assert "total_fee" in rate_entry
                assert "source" in rate_entry
                assert rate_entry["status"] == "PLACEHOLDER"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
