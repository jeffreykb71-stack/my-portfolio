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
    public_msgs = list(db.shoutouts.find().sort("_id", -1))
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

if __name__ == "__main__":
    app.run(debug=True)