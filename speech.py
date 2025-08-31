from flask import Blueprint, request, jsonify
from app.services.speech_analyzer import SpeechAnalyzer
from app.services.feedback_generator import FeedbackGenerator
import os
import tempfile

speech_bp = Blueprint('speech', __name__)
speech_analyzer = SpeechAnalyzer()
feedback_generator = FeedbackGenerator()

@speech_bp.route('/analyze', methods=['POST'])
def analyze_speech():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        expected_text = request.form.get('expected_text', '')
        
        if not expected_text:
            return jsonify({'error': 'Expected text is required'}), 400
        
        # Save audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            audio_file.save(tmp_file.name)
            
            # Analyze speech
            analysis_result = speech_analyzer.analyze(tmp_file.name, expected_text)
            
            # Generate feedback
            feedback = feedback_generator.generate_feedback(analysis_result)
            
            # Clean up
            os.unlink(tmp_file.name)
            
            return jsonify({
                'analysis': analysis_result,
                'feedback': feedback,
                'success': True
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500