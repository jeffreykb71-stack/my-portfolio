import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

app = Flask(__name__, template_folder='../templates')

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.ProjectVault

@app.route('/')
def index():
    try:
        # Fetching projects and sorting by newest first
        projects = list(db.ideas.find().sort("_id", -1))
    except Exception as e:
        print(f"DB Error: {e}")
        projects = []
    
    # Your Professional Bio
    bio = {
        "name": "Salman",
        "university": "Kristu Jayanti University",
        "degree": "B.Sc. AI & Machine Learning (1st Year)",
        "summary": "Forward-thinking AI/ML student with a core foundation in C programming and Web Technologies. I thrive in high-pressure AI competitions and am dedicated to engineering efficient, scalable solutions.",
        "skills": ["Python / Flask", "C Programming", "HTML5 / CSS3", "MongoDB Atlas"]
    }
    
    return render_template('index.html', projects=projects, bio=bio)

@app.route('/add-idea', methods=['POST'])
def add_idea():
    title = request.form.get('title')
    category = request.form.get('category')
    description = request.form.get('description')
    
    if title and description:
        db.ideas.insert_one({
            "title": title,
            "category": category,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    return redirect('/')

# This is required for Vercel 
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(debug=True)