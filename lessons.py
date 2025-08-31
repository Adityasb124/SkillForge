from flask import Blueprint, jsonify, request
import random
import os
from ..services.speech_analyzer import SpeechAnalyzer

lessons_bp = Blueprint('lessons', __name__)
analyzer = SpeechAnalyzer()

# Sample sentences for practice
PRACTICE_SENTENCES = {
    'beginner': [
        "The cat sits on the mat.",
        "I like to play in the park.",
        "Please open the window.",
        "The sun is shining bright.",
        "Can you help me please?"
    ],
    'intermediate': [
        "Yesterday I went to the museum with my friends.",
        "The weather forecast predicts rain tomorrow.",
        "She enjoys reading books in the library."
    ]
}

@lessons_bp.route('/sentences/<level>')
def get_sentences(level):
    """Get practice sentences for given level"""
    if level not in PRACTICE_SENTENCES:
        return jsonify({'error': 'Invalid level'}), 400
        
    # Return random sentence from the level
    sentences = PRACTICE_SENTENCES[level]
    return jsonify([random.choice(sentences)])

@lessons_bp.route('/speech/recognize', methods=['POST'])
def speech_recognition():
    """Handle speech recognition requests"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        target_sentence = request.form.get('target_sentence', '').strip()
        
        # Save audio temporarily
        temp_dir = "temp_audio"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        temp_path = os.path.join(temp_dir, "temp_audio.wav")
        audio_file.save(temp_path)
        
        # Analyze the speech
        try:
            analysis_result = analyzer.analyze(temp_path, target_sentence)
            
            # Clean up temp file
            os.remove(temp_path)
            
            return jsonify({
                'success': True,
                'analysis': analysis_result
            })
            
        except Exception as e:
            # If full analysis fails, try basic analysis
            basic_result = analyzer.analyze_speech(
                target_sentence, 
                analysis_result.get('transcribed_text', '')
            )
            return jsonify({
                'success': True,
                'analysis': basic_result
            })
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Speech recognition failed'
        }), 500
