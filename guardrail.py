import re

def check_reply(text: str) -> str:
    patterns = [
        r"(?i)\byou are eligible\b",
        r"(?i)\byou will be approved\b",
        r"(?i)\bno penalty\b",
        r"(?i)\blegally allowed\b",
        r"(?i)\bas an rto officer\b",
        r"(?i)\bas an officer\b",
        r"(?i)\bi have submitted\b",
        r"(?i)\bhas been submitted\b"
    ]
    
    for pattern in patterns:
        if re.search(pattern, text):
            return "Based on general guidelines, these are the typical rules. Please confirm your specific case with the RTO. Final decision rests with the RTO officer."
    return text
