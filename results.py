import json
from flask import Blueprint, request, jsonify
from app.models.result import Result
from app import db

results_bp = Blueprint('results', __name__)

@results_bp.route('/save', methods=['POST'])
def save_result():
    """Save analysis result"""
    try:
        data = request.get_json()
        
        result = Result(
            user_id=data.get('user_id', 'anonymous'),
            sentence=data['sentence'],
            transcribed_text=data['transcribed_text'],
            overall_score=data['overall_score'],
            pronunciation_score=data.get('pronunciation_score', 0),
            fluency_score=data.get('fluency_score', 0),
            analysis_data=json.dumps(data.get('analysis_data', {}))
        )
        
        db.session.add(result)
        db.session.commit()
        
        return jsonify({'success': True, 'result_id': result.id})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@results_bp.route('/history/<user_id>')
def get_user_history(user_id):
    """Get user's practice history"""
    try:
        results = Result.query.filter_by(user_id=user_id).order_by(Result.created_at.desc()).limit(20).all()
        
        history = []
        for result in results:
            history.append({
                'id': result.id,
                'sentence': result.sentence,
                'score': result.overall_score,
                'date': result.created_at.isoformat(),
                'pronunciation_score': result.pronunciation_score,
                'fluency_score': result.fluency_score
            })
        
        return jsonify(history)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
