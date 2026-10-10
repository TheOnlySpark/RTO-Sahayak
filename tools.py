import os
import json
import glob
import csv

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

def extract_document(file_id: str) -> dict:
    """Sends image bytes to Gemini and asks for JSON only. Do not log contents."""
    from google import genai
    from google.genai import types
    import json
    import streamlit as st
    
    client = genai.Client()
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    
    system_instruction = "Extract the document details into a valid JSON object with exact keys: type, name, dob, address, masked_id. Do not output markdown, just raw JSON."
    
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.0
    )
    
    file_bytes = st.session_state.uploaded_files.get(file_id)
    if not file_bytes:
        return {"error": "File not found."}
        
    try:
        response = client.models.generate_content(
            model=model,
            contents=[types.Part.from_bytes(data=file_bytes, mime_type="image/jpeg"), "Extract document details as JSON."],
            config=config
        )
        
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text.strip())
    except Exception as e:
        return {"error": str(e)}

def licence_stats(state: str, year: str = "2019-20") -> dict:
    """Reads historical statistics about licences issued."""
    open_dir = os.path.join(os.path.dirname(__file__), "data", "open")
    csv_path = os.path.join(open_dir, "licences.csv")
    sources_path = os.path.join(open_dir, "SOURCES.md")
    
    source_text = "Unknown Source"
    try:
        with open(sources_path, "r", encoding="utf-8") as f:
            source_text = f.read().strip()
    except FileNotFoundError:
        pass
        
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("state", "").lower() == state.lower() and row.get("year", "") == year:
                    return {
                        "total": int(row.get("total", 0)),
                        "male": int(row.get("male", 0)),
                        "female": int(row.get("female", 0)),
                        "professional": int(row.get("professional", 0)),
                        "non_professional": int(row.get("non_professional", 0)),
                        "source": source_text,
                        "year": year
                    }
    except FileNotFoundError:
        pass
        
    return {"available": False, "reason": "state did not report this year"}

import datetime
def get_slots(service: str) -> list:
    """Returns available appointment slots."""
    return [str(datetime.date.today() + datetime.timedelta(days=i)) for i in range(1, 4)]
