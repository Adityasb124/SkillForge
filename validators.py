import re

def validate_audio_file(file):
    """Validate uploaded audio file"""
    if not file:
        return False, "No file provided"
    
    if file.filename == '':
        return False, "No file selected"
    
    # Check file extension
    allowed_extensions = {'wav', 'mp3', 'ogg', 'webm', 'm4a'}
    if not ('.' in file.filename and 
            file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return False, "Invalid file type. Please upload audio files only."
    
    return True, "Valid file"

def validate_text_input(text):
    """Validate text input"""
    if not text or not text.strip():
        return False, "Text cannot be empty"
    
    if len(text) > 1000:
        return False, "Text is too long (max 1000 characters)"
    
    # Check for basic safety (no special characters that might cause issues)
    if re.search(r'[<>{}]', text):
        return False, "Text contains invalid characters"
    
    return True, "Valid text"
