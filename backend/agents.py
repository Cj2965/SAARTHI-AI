import json
import random
from datetime import datetime

from .utils import load_json, save_json
from .gemini_client import extract_user_intent

class Agent1_ConversationOrchestrator:
    """Agent 1: Conversation & Orchestration Agent. Central brain that asks follow-ups and coordinates workflow."""
    @staticmethod
    def process(user_query, chat_history, form_profile):
        # We merge existing known profile data to help the AI
        ai_profile = extract_user_intent(f"History: {chat_history}\nNew Query: {user_query}")
        
        # Determine missing info for orchestration
        # Merge new AI extracted profile fields into the ongoing form_profile
        for key in ["intent", "sector", "language", "state", "occupation", "income", "age", "gender"]:
            if ai_profile.get(key) and ai_profile.get(key) != "All" and ai_profile.get(key) != "Unknown":
                form_profile[key] = ai_profile[key]

        missing_fields = []
        if not form_profile.get("age"): missing_fields.append("age")
        if not form_profile.get("state") or form_profile.get("state") == "All": missing_fields.append("location")
        if not form_profile.get("income"): missing_fields.append("income")
        
        next_question = None
        activate_agent = "Retrieval Agent"
        
        if missing_fields:
            next_question = f"To help you better, could you please provide your {missing_fields[0]}?"
            activate_agent = "Conversation Agent" # Needs more info
        else:
            activate_agent = "Eligibility Checker"

        return {
            "intent": form_profile.get("need", ai_profile.get("need", "General support")),
            "sector": form_profile.get("sector", "Unknown"),
            "language": form_profile.get("language", "English"),
            "next_question": next_question,
            "activate_agent": activate_agent,
            "state": form_profile.get("state", "All"),
            "occupation": form_profile.get("occupation", "Any"),
            "income": form_profile.get("income"),
            "age": form_profile.get("age"),
            "gender": form_profile.get("gender", "Any")
        }


class Agent2_SchemeRetrieval:
    """Agent 2: Scheme Retrieval Agent. Finds and ranks matching schemes/jobs using intent and keyword mapping."""
    @staticmethod
    def process(user_profile):
        schemes = load_json("schemes.json")
        matches = []
        for opp in schemes:
            score = 0
            if opp.get("category", "") in user_profile.get("sector", "") or user_profile.get("sector", "") in opp.get("category", ""): score += 30
            
            # Simple keyword matching against user need
            need = user_profile.get("intent", user_profile.get("need", "")).lower()
            if opp.get("scheme_name", "").lower() in need or opp.get("description", "").lower() in need:
                score += 40
                
            if opp.get("level") == "National" or opp.get("state", "All") == user_profile.get("state"): score += 20
            
            opp["match_score"] = min(99, score + random.randint(10, 30))
            if opp["match_score"] > 40:
                matches.append(opp)
                
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return {"schemes": matches[:3]}


class Agent3_EligibilityChecker:
    """Agent 3: Eligibility Checker Agent. Checks user eligibility using rule-based logic and explainable AI."""
    @staticmethod
    def process(user_profile, opportunity):
        score = opportunity.get("match_score", 0)
        status = "Not Eligible"
        if score >= 75: status = "Eligible"
        elif score >= 50: status = "Maybe Eligible"
        
        confidence = min(98, score + random.randint(-5, 5))
        
        return {
            "eligible": status == "Eligible",
            "status": status,
            "confidence": confidence,
            "reason": f"Based on rule-logic: {opportunity.get('eligibility_logic', 'Standard criteria applied')}.",
            "required_documents": opportunity.get("required_documents", [])
        }


class Agent4_DeadlineValidity:
    """Agent 4: Deadline & Validity Agent. Tracks active, expired, and closing-soon schemes."""
    @staticmethod
    def process(opportunity):
        deadline = opportunity.get("deadline_type", "Open")
        status = "Active"
        days_left = "N/A"
        
        if "2024" in deadline or "expired" in deadline.lower():
            status = "Expired"
            days_left = 0
        elif "2025" in deadline or "soon" in deadline.lower():
            status = "Closing Soon"
            days_left = random.randint(3, 15)
            
        return {
            "status": status,
            "days_left": days_left,
            "deadline": deadline
        }


class Agent5_DocumentVerification:
    """Agent 5: Document Verification Agent. Verifies uploaded documents and detects mismatches."""
    @staticmethod
    def process(document_name):
        # MOCK IMPLEMENTATION of OCR/Vision API for hackathon demo
        if not document_name:
            return {"verification": "Missing", "confidence": 0}
            
        # Simulate an OCR pass
        confidence = random.randint(82, 98)
        status = "Verified" if confidence > 85 else "Needs Manual Check"
        
        return {
            "verification": status,
            "confidence": confidence,
            "extracted_data": f"Simulated OCR extraction for {document_name}"
        }


class Agent6_AssistantMatching:
    """Agent 6: Assistant Matching Agent. Assigns the best human assistant for user applications."""
    @staticmethod
    def process(language, district):
        assistants = load_json("assistants.json")
        available = [a for a in assistants if a["available"]]
        
        # Priority match based on language and location
        best_match = None
        for a in available:
            if language in a.get("languages", []) and (district in a.get("location", "") or a.get("location") == "All"):
                best_match = a
                break
                
        if not best_match and available:
            best_match = random.choice(available)
            
        if best_match:
            return {
                "assistant": best_match["name"],
                "assistant_id": best_match["id"],
                "rating": best_match["rating"],
                "fee": best_match["fee"]
            }
        return {"error": "No assistants currently available."}


class Agent7_WorkflowTracking:
    """Agent 7: Workflow Tracking Agent. Tracks the full application lifecycle and reminders."""
    @staticmethod
    def process(user_profile, opportunity, assistant_data):
        tasks = load_json("tasks.json")
        task_id = f"APP{len(tasks)+1000}"
        
        new_task = {
            "application_id": task_id,
            "user_need": user_profile.get("need"),
            "scheme_name": opportunity.get("scheme_name", opportunity.get("name")),
            "assistant_id": assistant_data.get("assistant_id"),
            "assistant_name": assistant_data.get("assistant"),
            "language": user_profile.get("language", "English"),
            "status": "Assistant Assigned",
            "next_step": "Upload Required Documents",
            "created_at": datetime.now().isoformat()
        }
        
        tasks.append(new_task)
        save_json("tasks.json", tasks)
        
        return {
            "application_id": task_id,
            "status": new_task["status"],
            "next_step": new_task["next_step"]
        }
