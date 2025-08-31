from app import db

def init_db():
    """Initialize database tables"""
    db.create_all()

def reset_db():
    """Reset database (use with caution!)"""
    db.drop_all()
    db.create_all()