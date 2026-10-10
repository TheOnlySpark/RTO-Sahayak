import os
import json
import glob

def lookup_rules(topic: str) -> dict:
    """Reads data/rules/*.md and returns the best match based on simple keyword matching."""
    best_match = None
    best_score = -1
    
    rules_dir = os.path.join(os.path.dirname(__file__), "data", "rules")
    for filepath in glob.glob(os.path.join(rules_dir, "*.md")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            score = content.lower().count(topic.lower())
            if score > best_score:
                best_score = score
                best_match = {"text": content, "source": os.path.basename(filepath)}
    
    if best_match and best_score > 0:
        return best_match
    return {"text": "No specific rules found.", "source": "none"}

def calc_fees(service: str, vehicle_class: str) -> dict:
    """Reads data/fees.json and returns fee items."""
    fees_path = os.path.join(os.path.dirname(__file__), "data", "fees.json")
    try:
        with open(fees_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"note": "PLACEHOLDER. File not found.", "total": 0, "items": []}
    
    items = [item for item in data.get("fees", []) if item.get("service") == service and item.get("vehicle_class") == vehicle_class]
    total = sum(item.get("amount", 0) for item in items)
    return {"note": "PLACEHOLDER. Values to be verified by human.", "total": total, "items": items}

def build_checklist(service: str, age: int) -> dict:
    """Reads checklist from data/rules and returns documents list."""
    rules = lookup_rules(service)
    text = rules.get("text", "")
    documents = []
    if "Checklist:" in text:
        try:
            checklist_str = text.split("Checklist:")[1].split("\n")[0].strip()
            documents = [d.strip() for d in checklist_str.split(",")]
        except Exception:
            pass
    return {"documents": documents}
