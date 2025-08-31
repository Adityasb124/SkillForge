from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Simple login/registration"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        age = data.get('age', 8)
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        # Find or create user
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, age=age)
            db.session.add(user)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'level': user.level,
                'total_sessions': user.total_sessions,
                'average_score': user.average_score
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
