from .utils import load_json, save_json
import datetime
import uuid

def collect_feedback(user_profile, opportunity, rating, comment, issue_type):
    """
    Saves feedback in feedback.json
    Returns improvement suggestion.
    """
    feedback_data = load_json('feedback.json')
    
    new_feedback = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.now().isoformat(),
        "user_profile": user_profile,
        "opportunity_name": opportunity.get('name') if opportunity else None,
        "rating": rating,
        "issue_type": issue_type,
        "comment": comment
    }
    
    feedback_data.append(new_feedback)
    save_json('feedback.json', feedback_data)
    
    return "Thank you. Saarthi will use this feedback to improve future recommendations."
