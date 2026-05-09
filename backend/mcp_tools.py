import uuid
import datetime
from .utils import load_json, save_json
from .gemini_client import extract_intent, translate_text

def analyze_user_need(user_query, profile_form_data):
    """
    Uses Gemini output or fallback keyword logic to build a structured profile.
    """
    # Get structured intent from query
    intent = extract_intent(user_query)
    
    # Merge with explicit profile data from form
    user_profile = {
        "query_intent": intent,
        "state": profile_form_data.get("state") or intent.get("state"),
        "age": profile_form_data.get("age") or intent.get("age"),
        "gender": profile_form_data.get("gender") or intent.get("gender"),
        "income": profile_form_data.get("income") or intent.get("income"),
        "occupation": profile_form_data.get("occupation") or intent.get("occupation"),
        "language": profile_form_data.get("language") or intent.get("language", "English")
    }
    
    return user_profile

def search_opportunities(user_profile):
    """
    Searches schemes.json and jobs.json.
    Returns top 3 matching opportunities based on sector, need, state, etc.
    """
    schemes = load_json("schemes.json")
    jobs = load_json("jobs.json")
    
    all_opportunities = schemes + jobs
    scored_opps = []
    
    target_sector = user_profile.get("query_intent", {}).get("sector", "")
    target_state = user_profile.get("state", "All")
    
    for opp in all_opportunities:
        score = 0
        
        # Sector match
        if opp.get("sector") == target_sector:
            score += 1000
            
        # State match
        opp_state = opp.get("state", "All")
        if opp_state == "All" or opp_state == target_state:
            score += 20
            
        # Income logic (simple)
        user_income = user_profile.get("income")
        opp_income_limit = opp.get("income_limit")
        if user_income and opp_income_limit:
            try:
                if int(user_income) <= int(opp_income_limit):
                    score += 20
            except ValueError:
                pass
        else:
            score += 10 # Default partial score if not strictly limited
            
        # Gender match
        user_gender = user_profile.get("gender")
        opp_gender = opp.get("gender_preference")
        if opp_gender and user_gender:
            if opp_gender.lower() == user_gender.lower():
                score += 20
        elif not opp_gender:
            score += 10
            
        scored_opps.append({
            "opportunity": opp,
            "score": score
        })
        
    # Sort by score descending and return top 3
    scored_opps.sort(key=lambda x: x["score"], reverse=True)
    return [item["opportunity"] for item in scored_opps[:3]]

def check_eligibility(user_profile, opportunity):
    """
    Analyzes eligibility.
    """
    score = 0
    max_score = 100
    reasons = []
    
    # State check
    if opportunity.get("state") != "All" and opportunity.get("state") != user_profile.get("state"):
        reasons.append(f"Scheme is for {opportunity.get('state')} but you are in {user_profile.get('state')}.")
        max_score -= 30
    else:
        score += 30
        
    # Income check
    if opportunity.get("income_limit") and user_profile.get("income"):
        try:
            if int(user_profile.get("income")) > int(opportunity.get("income_limit")):
                reasons.append(f"Income exceeds the limit of {opportunity.get('income_limit')}.")
                max_score -= 40
            else:
                score += 40
        except ValueError:
            pass
    else:
        score += 40
        
    # Gender check
    if opportunity.get("gender_preference") and user_profile.get("gender"):
        if opportunity.get("gender_preference").lower() != user_profile.get("gender").lower():
            reasons.append(f"Scheme is targeted towards {opportunity.get('gender_preference')}.")
            max_score -= 30
        else:
            score += 30
    else:
        score += 30
        
    confidence = int((score / 100.0) * 100)
    
    status = "eligible"
    if confidence < 50:
        status = "not eligible"
    elif confidence < 90:
        status = "maybe eligible"
        
    if not reasons:
        reasons.append("You appear to meet the basic criteria.")
        
    return {
        "status": status,
        "confidence_score": confidence,
        "reason": " ".join(reasons),
        "required_documents": opportunity.get("documents", []),
        "missing_documents": ["Check required list"], # Mock
        "next_step": "Gather documents and apply online or request a Saarthi Assistant."
    }

def request_assistant(user_profile, opportunity):
    """
    Assigns an assistant from assistants.json based on language/location.
    """
    assistants = load_json("assistants.json")
    user_lang = user_profile.get("language", "English")
    
    best_match = None
    for assistant in assistants:
        if assistant.get("available") and user_lang in assistant.get("languages", []):
            best_match = assistant
            break
            
    # Fallback to first available if language match fails
    if not best_match:
        for assistant in assistants:
            if assistant.get("available"):
                best_match = assistant
                break
                
    if not best_match:
        return {"error": "No assistants available currently."}
        
    task_id = f"TASK-{str(uuid.uuid4())[:8].upper()}"
    
    new_task = {
        "task_id": task_id,
        "user_need": user_profile.get("query_intent", {}).get("need", "Application Help"),
        "scheme_name": opportunity.get("name"),
        "assistant_id": best_match["id"],
        "assistant_name": best_match["name"],
        "language": user_lang,
        "fee": best_match["fee"],
        "status": "Pending",
        "created_at": datetime.datetime.now().isoformat(),
        "user_profile": user_profile
    }
    
    tasks = load_json("tasks.json")
    tasks.append(new_task)
    save_json("tasks.json", tasks)
    
    return {
        "task_id": task_id,
        "assistant_name": best_match["name"],
        "assistant_language": user_lang,
        "fee": best_match["fee"],
        "task_status": "Pending"
    }

def track_deadline(opportunity):
    """
    Returns deadline info.
    """
    deadline = opportunity.get("deadline", "Open")
    return {
        "deadline": deadline,
        "reminder_status": "Set" if deadline != "Open" else "N/A",
        "next_action": "Apply before deadline" if deadline != "Open" else "Apply anytime"
    }

def translate_response(text, target_language):
    """Wrapper for gemini translation."""
    return translate_text(text, target_language)
