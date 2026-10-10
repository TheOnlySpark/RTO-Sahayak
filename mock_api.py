"""
Mock External API for RTO Sahayak.

Provides synthetic service endpoints (such as RTO appointment slots)
for testing and demonstration purposes.

Strictly synthetic data:
Never claims real government connection or live slot availability.
Final decision rests with the RTO officer.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

# Standard synthetic appointment slot templates
SAMPLE_SLOT_TEMPLATES = [
    "2026-10-15 10:00 AM - 11:00 AM",
    "2026-10-15 11:30 AM - 12:30 PM",
    "2026-10-16 02:00 PM - 03:00 PM",
    "2026-10-16 03:30 PM - 04:30 PM",
    "2026-10-19 10:00 AM - 11:00 AM",
    "2026-10-19 02:30 PM - 03:30 PM",
]

SYNTHETIC_NOTE = "synthetic sample slots, not real availability"


def get_slots(rto_code: str) -> Dict[str, Any]:
    """
    Retrieve synthetic appointment slots for a given RTO code.

    Args:
        rto_code: String representing the RTO jurisdiction code (e.g., 'DL04', 'MH01').

    Returns:
        Dict containing:
        - "slots": List of synthetic time slot strings.
        - "note": "synthetic sample slots, not real availability"
    """
    code_clean = str(rto_code or "").strip().upper()

    # Deterministic subset or variation based on RTO code for realistic mock testing
    if not code_clean:
        selected_slots = SAMPLE_SLOT_TEMPLATES[:4]
    else:
        # Simple deterministic partition
        code_num = sum(ord(c) for c in code_clean)
        offset = code_num % 2
        selected_slots = SAMPLE_SLOT_TEMPLATES[offset : offset + 4]

    return {
        "slots": selected_slots,
        "note": SYNTHETIC_NOTE,
    }


if __name__ == "__main__":
    result = get_slots("DL04")
    print(f"RTO DL04 Slots: {result}")
