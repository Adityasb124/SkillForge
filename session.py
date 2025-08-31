from app import db
from datetime import datetime

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    sentences_completed = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float, default=0.0)
    level = db.Column(db.String(20), default='beginner')
    
    def __repr__(self):
        return f'<Session {self.id}: {self.user_id}>'