import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
DATA_FILE = 'data/student_data.json'
API_KEY = os.getenv('AI_API_KEY')

# Helper function to read data
def read_data():
    if not os.path.exists(DATA_FILE):
        return {"progress": {"overall_percentage": 0, "subjects": {}, "skills": []}}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Helper function to write data
def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

import requests

# Simulated AI response function (Beginner friendly fallback)
def generate_ai_response(prompt, context_type):
    if API_KEY:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            system_instruction = f"You are an AI college study companion helping a student with {context_type}."
            
            payload = {
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"Student Request:\n{prompt}"}
                ]
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error connecting to AI: {str(e)}\n\n(Falling back to mock response...)\n\n" + mock_ai_response(prompt, context_type)
    else:
        return mock_ai_response(prompt, context_type)

def mock_ai_response(prompt, context_type):
    prompt_lower = prompt.lower()
    
    if context_type == "study":
        if "inheritance" in prompt_lower:
            return "Inheritance is a core concept in Object-Oriented Programming (OOP). Think of it like a family tree: just as a child inherits traits (like eye color) from their parents, a new class (child/subclass) can inherit properties and behaviors (methods) from an existing class (parent/superclass). This promotes code reuse!"
        return f"Here is a simple explanation for your question about {prompt}: \n\nThis is a simulated response. In a fully connected app, the AI would explain this topic step-by-step."
        
    elif context_type == "planner":
        return f"Suggested Study Plan:\n\n1. Day 1: Focus on the fundamentals of the topic (1.5 hours).\n2. Day 2: Dive into advanced concepts and examples (2 hours).\n3. Day 3: Practice questions and review (1 hour).\n\nGood luck with your exam!"
        
    elif context_type == "assignment":
        return f"Assignment Guide:\n\n- **Objective:** Understand the core requirements.\n- **Key Points to Cover:** Ensure you define the main concepts.\n- **Approach:** Start with an introduction, follow up with examples, and end with a strong conclusion.\n- **Tip:** Do not copy directly, use this outline to structure your own thoughts."
        
    elif context_type == "exam":
        return f"Revision Notes:\n\n- Remember the key definitions.\n- Practice solving previous year questions.\n- **Important Concepts:** Focus on the main topics you mentioned.\n- Take regular breaks while studying!"
        
    return "AI Response: I am ready to assist you!"



# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/study')
def study():
    return render_template('study.html')

@app.route('/planner')
def planner():
    return render_template('planner.html')

@app.route('/assignment')
def assignment():
    return render_template('assignment.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

# --- API ENDPOINTS ---

@app.route('/api/ask', methods=['POST'])
def api_ask():
    data = request.json
    subject = data.get('subject', '')
    topic = data.get('topic', '')
    question = data.get('question', '')
    
    prompt = f"Subject: {subject}, Topic: {topic}, Question: {question}"
    response_text = generate_ai_response(prompt, "study")
    
    return jsonify({"answer": response_text})

@app.route('/api/plan', methods=['POST'])
def api_plan():
    data = request.json
    subject = data.get('subject', '')
    topics = data.get('topics', '')
    exam_date = data.get('examDate', '')
    hours = data.get('hours', '')
    difficulty = data.get('difficulty', '')
    
    prompt = f"Create a study plan for {subject} covering {topics} before {exam_date}. I have {hours} hours available. Difficulty: {difficulty}."
    response_text = generate_ai_response(prompt, "planner")
    
    return jsonify({"plan": response_text})

@app.route('/api/assignment', methods=['POST'])
def api_assignment():
    data = request.json
    subject = data.get('subject', '')
    topic = data.get('topic', '')
    question = data.get('question', '')
    
    prompt = f"Help with assignment for {subject} on {topic}. Instructions: {question}"
    response_text = generate_ai_response(prompt, "assignment")
    
    return jsonify({"help": response_text})

@app.route('/api/exam', methods=['POST'])
def api_exam():
    data = request.json
    subject = data.get('subject', '')
    topic = data.get('topic', '')
    exam_date = data.get('examDate', '')
    
    prompt = f"Provide exam revision points for {subject}, topic {topic}. Exam is on {exam_date}."
    response_text = generate_ai_response(prompt, "exam")
    
    return jsonify({"revision": response_text})

@app.route('/api/progress', methods=['GET', 'POST'])
def api_progress():
    if request.method == 'GET':
        return jsonify(read_data())
    
    if request.method == 'POST':
        new_data = request.json
        # Format the received data and save it
        progress_data = read_data()
        
        # Simple update logic
        student_name = new_data.get('studentName', 'Student')
        subject = new_data.get('subject', '')
        marks = new_data.get('marks', '0')
        skill = new_data.get('skill', '')
        skill_level = new_data.get('skillLevel', 'Beginner')
        
        # Update progress dummy logic
        progress_data['progress']['overall_percentage'] = min(100, progress_data['progress']['overall_percentage'] + 10)
        progress_data['progress']['subjects'][subject] = f"Completed ({marks}% in Quiz)"
        if skill and skill not in [s['name'] for s in progress_data['progress']['skills']]:
            progress_data['progress']['skills'].append({"name": skill, "level": skill_level})
            
        write_data(progress_data)
        return jsonify({"status": "success", "message": "Progress updated successfully!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
