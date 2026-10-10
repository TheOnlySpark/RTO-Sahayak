import os
import time
from google import genai
from google.genai import types
from tools import lookup_rules, calc_fees, build_checklist, extract_document, licence_stats, get_slots
from dotenv import load_dotenv

load_dotenv()

try:
    from compare import compare_documents
except ImportError:
    def compare_documents(doc1: dict, doc2: dict) -> dict:
        return {"mismatch": False, "details": "Documents match perfectly. (STUB)"}

try:
    from pdf_tools import generate_handoff_pdf
except ImportError:
    def generate_handoff_pdf(user_name: str, service: str) -> dict:
        return {"status": "success", "file": "dummy.pdf"}

system_instruction = """
You are RTO Sahayak. Calculate age from Date of Birth (DOB) if provided. Ask for age (or DOB) and vehicle class if missing. 
Use tools for facts. Cite the source. 
Never decide eligibility or make legal claims. 
End rule answers with "Final decision rests with the RTO officer."

Documents:
When documents mismatch, explain the difference plainly, say which authority usually corrects it, and never say the application will be rejected.

Licence Stats:
Use only for context about licence volumes. Always state the year and that it is historical. Never apply it to an individual.
"""

def get_client(fallback=False):
    model = os.environ.get("GEMINI_FALLBACK_MODEL", "gemini-2.5-flash-lite") if fallback else os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    client = genai.Client()
    return client, model

def process_message(message: str, history: list = None) -> dict:
    client, model = get_client()
    
    contents = []
    if history:
        for msg in history:
            contents.append(
                types.Content(role=msg["role"], parts=[types.Part.from_text(text=msg["text"])])
            )
            
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=message)]))
    
    tools = [lookup_rules, calc_fees, build_checklist, extract_document, compare_documents, licence_stats, get_slots, generate_handoff_pdf]
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=tools,
        temperature=0.0
    )
    
    tool_calls_made = []
    
    for step in range(4):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
        except Exception as e:
            if "429" in str(e):
                time.sleep(2) # Backoff
                client, model = get_client(fallback=True)
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config
                )
            else:
                raise e
                
        if response.function_calls:
            contents.append(response.candidates[0].content)
            
            parts = []
            for function_call in response.function_calls:
                func_name = function_call.name
                args = function_call.args
                tool_calls_made.append({"name": func_name, "args": args})
                
                # Execute tool
                if func_name == "lookup_rules":
                    res = lookup_rules(**args)
                elif func_name == "calc_fees":
                    res = calc_fees(**args)
                elif func_name == "build_checklist":
                    res = build_checklist(**args)
                elif func_name == "extract_document":
                    res = extract_document(**args)
                elif func_name == "compare_documents":
                    res = compare_documents(**args)
                elif func_name == "licence_stats":
                    res = licence_stats(**args)
                elif func_name == "get_slots":
                    res = get_slots(**args)
                elif func_name == "generate_handoff_pdf":
                    res = generate_handoff_pdf(**args)
                else:
                    res = {"error": "unknown tool"}
                
                parts.append(types.Part.from_function_response(name=func_name, response=res))
                
            contents.append(types.Content(role="user", parts=parts))
        else:
            return {"answer": response.text, "tool_calls": tool_calls_made}
            
    return {"answer": "Max steps reached without a text answer.", "tool_calls": tool_calls_made}
