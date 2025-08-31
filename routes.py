from flask import Blueprint, render_template, send_from_directory, current_app
from pymongo import MongoClient
import os

main = Blueprint('main', __name__)
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client.skillforge

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(main.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@main.route('/')  # Add root path route
def home():
    """Homepage"""
    return render_template('index.html')

@main.route('/templates/')
def index():
    """Main learning interface"""
    return render_template('index.html')  # Remove '../' from path

@main.route('/dashboard')
def dashboard():
    """Progress dashboard"""
    # Get all attempts
    attempts = list(db.attempts.find().sort("timestamp", -1).limit(10))
    
    # Calculate statistics
    total_attempts = db.attempts.count_documents({})
    pipeline = [{"$group": {"_id": None, "avg": {"$avg": "$score"}}}]
    avg_result = list(db.attempts.aggregate(pipeline))
    average_score = avg_result[0]["avg"] if avg_result else 0
    
    stats = {
        'total_attempts': total_attempts,
        'average_score': round(average_score, 2)
    }
    
    return render_template('dashboard.html', attempts=attempts, stats=stats)

@main.route('/results')
def results():
    """Results page"""
    return render_template('results.html')