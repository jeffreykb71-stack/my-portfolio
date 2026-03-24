import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.PortfolioDB

@app.route('/')
def index():
    try:
        public_msgs = list(db.shoutouts.find().sort("_id", -1))
    except Exception as e:
        print(f"Database error: {e}")
        public_msgs = []
    
    # You can keep your 'About' details here or hardcode in HTML
    bio = {
        "name": "Salman",
        "role": "Full Stack Developer",
        "description": "Passionate about building robust backend systems and clean, aggressive front-end interfaces. I specialize in Python, Flask, and NoSQL databases."
    }
    
    return render_template('index.html', public_msgs=public_msgs, bio=bio)

# ... (keep your /post-public and /post-private routes the same) ...

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)