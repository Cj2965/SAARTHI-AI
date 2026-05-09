from flask import Flask, request, jsonify, send_from_directory
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Import our backend tools
from backend.mcp_tools import (
    analyze_user_need, 
    search_opportunities, 
    check_eligibility, 
    request_assistant, 
    track_deadline, 
    translate_response
)
from backend.feedback import collect_feedback
from backend.utils import load_json, save_json

app = Flask(__name__, static_folder='frontend')

# Serve Static Files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# API Endpoints
@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.json
    user_query = data.get('query', '')
    profile_data = data.get('profile', {})
    
    # Analyze Need
    user_profile = analyze_user_need(user_query, profile_data)
    
    # Search Opportunities
    opportunities = search_opportunities(user_profile)
    
    results = []
    for opp in opportunities:
        eligibility = check_eligibility(user_profile, opp)
        deadline_info = track_deadline(opp)
        
        # We can translate texts if needed
        language = profile_data.get('language', 'English')
        if language != 'English':
            opp['description'] = translate_response(opp['description'], language)
            eligibility['reason'] = translate_response(eligibility['reason'], language)
            
        results.append({
            "opportunity": opp,
            "eligibility": eligibility,
            "deadline_info": deadline_info
        })
        
    return jsonify({
        "user_profile": user_profile,
        "results": results
    })

@app.route('/api/request_assistant', methods=['POST'])
def api_request_assistant():
    data = request.json
    user_profile = data.get('user_profile')
    opportunity = data.get('opportunity')
    
    task_result = request_assistant(user_profile, opportunity)
    return jsonify(task_result)

@app.route('/api/feedback', methods=['POST'])
def api_feedback():
    data = request.json
    user_profile = data.get('user_profile')
    opportunity = data.get('opportunity')
    rating = data.get('rating')
    comment = data.get('comment')
    issue_type = data.get('issue_type')
    
    res = collect_feedback(user_profile, opportunity, rating, comment, issue_type)
    return jsonify({"message": res})

@app.route('/api/tasks/new', methods=['POST'])
def add_new_task():
    data = request.json
    tasks = load_json("tasks.json")
    tasks.insert(0, data)
    save_json("tasks.json", tasks)
    return jsonify({"success": True})

@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    tasks = load_json("tasks.json")
    return jsonify(tasks)

@app.route('/api/tasks/update', methods=['POST'])
def api_update_task():
    data = request.json
    task_id = data.get('task_id')
    new_status = data.get('status')
    
    tasks = load_json("tasks.json")
    updated = False
    for t in tasks:
        if t['task_id'] == task_id:
            t['status'] = new_status
            updated = True
            break
            
    if updated:
        save_json("tasks.json", tasks)
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Task not found"})

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    prompt = data.get('prompt')
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_google_ai_studio_api_key_here":
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            context = """You are Saarthi AI, a helpful floating assistant guiding citizens in India.
You are embedded on the Saarthi platform website.
Website features:
- AI matches users with government schemes, jobs, and welfare programs.
- Multilingual voice support.
- Micro-employment: We assign human 'Saarthi Assistants' to physically help users fill forms.
If users ask what the website does, summarize that we bridge citizens with government opportunities and create micro-employment. Guide them to use the 'Discover Schemes' section.
Keep answers short, simple, and in the language the user speaks."""
            response = model.generate_content(f"{context}\n\nUser: {prompt}\nSaarthi AI:")
            reply = response.text.strip()
        except Exception as e:
            reply = f"I'm sorry, I cannot process your request right now. (Error: {e})"
    else:
        reply = "Hello! Please add your Gemini API key in the `.env` file to chat with me. As a fallback: I recommend checking the Discover tab to explore schemes!"
        
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
