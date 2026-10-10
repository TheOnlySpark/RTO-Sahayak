import os
import time
from google import genai
from google.genai import types
from tools import lookup_rules, calc_fees, build_checklist
from guardrail import check_reply
from dotenv import load_dotenv

load_dotenv()

system_instruction = """
You are RTO Sahayak. Ask for age and vehicle class if missing. 
Use tools for facts. Cite the source. 
Never decide eligibility or make legal claims. 
End rule answers with "Final decision rests with the RTO officer."
"""

def get_client(fallback=False):
    model = os.environ.get("GEMINI_FALLBACK_MODEL", "gemini-2.5-flash-lite") if fallback else os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    # Will use GEMINI_API_KEY from environment
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
    
    tools = [lookup_rules, calc_fees, build_checklist]
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
                try:
                    response = client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=config
                    )
                except Exception as inner_e:
                    if "429" in str(inner_e):
                        return {"answer": "This is a cached demo response due to API rate limits. Please try again later.", "tool_calls": tool_calls_made}
                    else:
                        raise inner_e
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
                else:
                    res = {"error": "unknown tool"}
                
                parts.append(types.Part.from_function_response(name=func_name, response=res))
                
            contents.append(types.Content(role="user", parts=parts))
        else:
            safe_text = check_reply(response.text)
            return {"answer": safe_text, "tool_calls": tool_calls_made}
            
    return {"answer": "Max steps reached without a text answer.", "tool_calls": tool_calls_made}
