import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

# Load the connection string from .env
load_dotenv()

app = Flask(__name__)

# Connect to MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.PortfolioDB

@app.route('/')
def index():
    # Requirement 1: Connect with the Database through the Backend
    # Use a try-except block to handle potential connection timeouts gracefully
    try:
        public_msgs = list(db.shoutouts.find().sort("_id", -1))
    except Exception as e:
        print(f"Database error: {e}")
        public_msgs = []
    return render_template('index.html', public_msgs=public_msgs)

@app.route('/post-public', methods=['POST'])
def post_public():
    name = request.form.get('name')
    message = request.form.get('message')
    db.shoutouts.insert_one({
        "name": name, 
        "message": message, 
        "date": datetime.now()
    })
    return redirect('/')

@app.route('/post-private', methods=['POST'])
def post_private():
    feedback = request.form.get('feedback')
    db.feedback.insert_one({
        "content": feedback, 
        "date": datetime.now()
    })
    return redirect('/')

# FIX: Added dynamic port binding for Render deployment
if __name__ == "__main__":
    # Render assigns a port via environment variable; local defaults to 5000
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' is required for Render to see the application
    app.run(host='0.0.0.0', port=port, debug=True)