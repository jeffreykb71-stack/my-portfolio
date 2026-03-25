import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client.ProjectVault 

@app.route('/')
def index():
    try:
        projects = list(db.ideas.find().sort("_id", -1))
    except Exception as e:
        print(f"Database Error: {e}")
        projects = []
    
    bio = {
        "name": "Salman",
        "university": "Kristu Jayanti University",
        "degree": "B.Sc. AI & Machine Learning (1st Year)",
        "summary": "I am a 1st-year B.Sc. AI & ML student at Kristu Jayanti University. I have developed strong foundational skills in HTML and C programming. I am highly enthusiastic, a hard worker, and always open to learning and improving. I have also participated in several AI competitions, sharpening my problem-solving abilities.",
        "skills": ["Python / Flask", "C Programming", "HTML5 / CSS3", "AI Model Logic"]
    }
    return render_template('index.html', projects=projects, bio=bio)

@app.route('/add-idea', methods=['POST'])
def add_idea():
    title = request.form.get('title') or request.form.get('name')
    desc = request.form.get('description') or request.form.get('message')
    
    if title and desc:
        try:
            db.ideas.insert_one({
                "title": title,
                "description": desc,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        except Exception as e:
            print(f"Insert Error: {e}")
            
    return redirect('/')

# FIXED: Corrected the parenthesis closure here
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)