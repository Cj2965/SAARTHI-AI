import os
import json
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key and api_key != "your_google_ai_studio_api_key_here":
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

def extract_intent(user_query):
    """
    Sends the user query to Gemini to extract structured information.
    Returns safe fallback if Gemini API fails or is not configured.
    """
    if not model:
        return _fallback_intent(user_query)
        
    prompt = f"""
    Analyze the following user query about government schemes, loans, jobs, or welfare.
    Extract the following information in strict JSON format.
    Do not include markdown blocks, just the JSON.
    
    Keys to extract:
    - need: (e.g., Business loan, Scholarship, Job, Agriculture support, Personal Vehicle)
    - sector: (Choose ONE from: Finance & Business, Personal Finance, Education & Jobs, Welfare & Public Support, Agriculture, Health, Community & Social Support, Miscellaneous & Public Services)
    - language: (Detect the language of the query: English, Hindi, Kannada, etc)
    - state: (If mentioned, else null)
    - occupation: (If mentioned, else null)
    - income: (If mentioned, else null)
    - age: (If mentioned, else null)
    - gender: (If mentioned, else null)
    
    User Query: "{user_query}"
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Remove markdown if present
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        result = json.loads(text)
        return result
    except Exception as e:
        print(f"Gemini API Error (Intent): {e}")
        return _fallback_intent(user_query)

def translate_text(text, target_language):
    """
    Translates text to the target language using Sarvam AI first,
    then falls back to Gemini if Sarvam fails.
    """
    target_lang_lower = target_language.lower()
    if target_lang_lower == "english":
        return text

    # Try Sarvam AI
    sarvam_key = os.getenv("SARVAM_API_KEY")
    if sarvam_key:
        lang_map = {
            "hindi": "hi-IN",
            "kannada": "kn-IN",
            "tamil": "ta-IN",
            "telugu": "te-IN",
            "bengali": "bn-IN",
            "marathi": "mr-IN"
        }
        target_code = lang_map.get(target_lang_lower)
        
        if target_code:
            try:
                url = "https://api.sarvam.ai/translate"
                payload = {
                    "input": text,
                    "source_language_code": "en-IN",
                    "target_language_code": target_code,
                    "speaker_gender": "Female",
                    "mode": "formal",
                    "model": "mayura:v1"
                }
                headers = {"api-subscription-key": sarvam_key, "Content-Type": "application/json"}
                response = requests.post(url, json=payload, headers=headers, timeout=5)
                if response.status_code == 200:
                    return response.json().get("translated_text", text)
            except Exception as e:
                print(f"Sarvam API Error: {e}")

    # Fallback to Gemini
    if not model:
        return text
        
    prompt = f"""
    Translate the following text to {target_language}.
    Keep it conversational, natural, and culturally appropriate. Do not do a robotic literal translation.
    
    Text: "{text}"
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error (Translation): {e}")
        return text

def _fallback_intent(user_query):
    """Simple keyword-based fallback if AI fails."""
    query_lower = user_query.lower()
    
    intent = {
        "need": "Unknown",
        "sector": "Miscellaneous & Public Services",
        "language": "English",
        "state": None,
        "occupation": None,
        "income": None,
        "age": None,
        "gender": None
    }
    
    # Simple keyword matching
    if "bike" in query_lower or "vehicle" in query_lower or "car" in query_lower:
        intent["need"] = "Personal Vehicle"
        intent["sector"] = "Personal Finance"
    elif "loan" in query_lower or "business" in query_lower or "funding" in query_lower:
        intent["need"] = "Business loan"
        intent["sector"] = "Finance & Business"
    elif "scholarship" in query_lower or "job" in query_lower or "training" in query_lower:
        intent["need"] = "Education or Job"
        intent["sector"] = "Education & Jobs"
    elif "welfare" in query_lower or "ration" in query_lower or "pension" in query_lower:
        intent["need"] = "Welfare Support"
        intent["sector"] = "Welfare & Public Support"
        
    if "hindi" in query_lower or "mujhe" in query_lower:
        intent["language"] = "Hindi"
    elif "kannada" in query_lower or "beku" in query_lower:
        intent["language"] = "Kannada"
        
    if "tailor" in query_lower or "silai" in query_lower:
        intent["occupation"] = "Tailoring"
        
    return intent
