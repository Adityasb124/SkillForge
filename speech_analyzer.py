import speech_recognition as sr
import tempfile
import os
import difflib
import re
from typing import Dict, List
from app.services.pronunciation_checker import PronunciationChecker
from app.services.fluency_analyzer import FluencyAnalyzer

class SpeechAnalyzer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Try to load Whisper, fallback to Google Speech Recognition if not available
        self.whisper_model = None
        self.use_whisper = False
        
        try:
            import whisper
            self.whisper_model = whisper.load_model("base")
            self.use_whisper = True
            print("✅ Using OpenAI Whisper for speech recognition")
        except Exception as e:
            print(f"⚠️ Whisper not available, using Google Speech Recognition: {e}")
            self.use_whisper = False
        
        self.pronunciation_checker = PronunciationChecker()
        self.fluency_analyzer = FluencyAnalyzer()
    
    def analyze(self, audio_path, expected_text):
        """Main analysis orchestrator"""
        try:
            # Transcribe audio using available method
            if self.use_whisper:
                transcribed_text = self._transcribe_with_whisper(audio_path)
            else:
                transcribed_text = self._transcribe_with_google(audio_path)
            
            # Check pronunciation
            pronunciation_score = self.pronunciation_checker.check(
                audio_path, expected_text, transcribed_text
            )
            
            # Analyze fluency
            fluency_analysis = self.fluency_analyzer.analyze(audio_path, transcribed_text)
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(
                pronunciation_score, fluency_analysis
            )
            
            return {
                'transcribed_text': transcribed_text,
                'expected_text': expected_text,
                'pronunciation_score': pronunciation_score,
                'fluency_analysis': fluency_analysis,
                'overall_score': overall_score,
                'word_accuracy': self._calculate_word_accuracy(expected_text, transcribed_text),
                'recognition_method': 'whisper' if self.use_whisper else 'google'
            }
        
        except Exception as e:
            # Fallback to basic analysis
            return self._fallback_analysis(expected_text, str(e))
    
    def _transcribe_with_whisper(self, audio_path):
        """Transcribe audio using Whisper"""
        try:
            result = self.whisper_model.transcribe(audio_path)
            return result["text"].strip()
        except Exception as e:
            print(f"Whisper transcription failed: {e}")
            return self._transcribe_with_google(audio_path)
    
    def _transcribe_with_google(self, audio_path):
        """Transcribe audio using Google Speech Recognition"""
        try:
            # Convert audio file to AudioFile
            with sr.AudioFile(audio_path) as source:
                audio_data = self.recognizer.record(source)
                
            # Use Google Speech Recognition (free tier)
            try:
                text = self.recognizer.recognize_google(audio_data)
                return text.strip()
            except sr.UnknownValueError:
                return ""  # Could not understand audio
            except sr.RequestError as e:
                print(f"Google Speech Recognition error: {e}")
                return ""
        
        except Exception as e:
            print(f"Audio transcription failed: {e}")
            return ""
    
    def _calculate_word_accuracy(self, expected, transcribed):
        """Calculate word-level accuracy"""
        if not transcribed or not expected:
            return 0
            
        expected_words = expected.lower().split()
        transcribed_words = transcribed.lower().split()
        
        if not expected_words:
            return 100
        
        correct = 0
        total = len(expected_words)
        
        # Simple word matching
        for i, word in enumerate(expected_words):
            if i < len(transcribed_words):
                if word == transcribed_words[i]:
                    correct += 1
                elif self._words_similar(word, transcribed_words[i]):
                    correct += 0.7  # Partial credit for similar words
        
        return (correct / total * 100) if total > 0 else 0
    
    def _words_similar(self, word1, word2):
        """Check if two words are similar (basic similarity)"""
        if len(word1) != len(word2):
            return False
        
        differences = sum(1 for a, b in zip(word1, word2) if a != b)
        return differences <= 1  # Allow 1 character difference
    
    def _calculate_overall_score(self, pronunciation_score, fluency_analysis):
        """Calculate overall proficiency score"""
        pronunciation_weight = 0.6
        fluency_weight = 0.4
        
        p_score = pronunciation_score.get('score', 0)
        f_score = fluency_analysis.get('score', 0)
        
        return round(p_score * pronunciation_weight + f_score * fluency_weight, 1)
    
    def _fallback_analysis(self, expected_text, error_msg):
        """Fallback analysis when everything fails"""
        print(f"Analysis failed, using fallback: {error_msg}")
        
        return {
            'transcribed_text': "Could not process audio",
            'expected_text': expected_text,
            'pronunciation_score': {'score': 50, 'mispronounced_words': [], 'phonetic_accuracy': 50},
            'fluency_analysis': {
                'score': 50, 
                'speaking_rate': 120, 
                'pause_count': 0, 
                'hesitations': 0,
                'stuttering_detected': False,
                'recommendations': ["Try speaking more clearly!"]
            },
            'overall_score': 50.0,
            'word_accuracy': 0,
            'recognition_method': 'fallback',
            'error': 'Audio processing failed, please try again'
        }
    
    def analyze_speech(self, target_text: str, spoken_text: str) -> Dict:
        # Normalize texts
        target_words = target_text.lower().split()
        spoken_words = spoken_text.lower().split()
        
        # Find differences
        matcher = difflib.SequenceMatcher(None, target_words, spoken_words)
        differences = list(matcher.get_opcodes())
        
        # Analyze results
        missed_words = []
        mispronounced = []
        score = 0
        
        for tag, i1, i2, j1, j2 in differences:
            if tag == 'delete':
                missed_words.extend(target_words[i1:i2])
            elif tag == 'replace':
                mispronounced.extend(zip(target_words[i1:i2], spoken_words[j1:j2]))
        
        # Calculate basic score (can be enhanced)
        total_words = len(target_words)
        correct_words = total_words - len(missed_words) - len(mispronounced)
        score = int((correct_words / total_words) * 100)
        
        # Generate kid-friendly feedback
        feedback = self._generate_feedback(score, missed_words, mispronounced)
        
        return {
            'score': score,
            'missed_words': missed_words,
            'mispronounced': dict(mispronounced),
            'feedback': feedback
        }
    
    def _generate_feedback(self, score: int, missed: List[str], mispronounced: List[tuple]) -> str:
        if score >= 90:
            message = "Amazing job! 🌟 "
        elif score >= 70:
            message = "Great effort! 👍 "
        else:
            message = "Keep practicing! 💪 "
        
        if missed:
            message += f"Try not to skip: {', '.join(missed)}. "
        
        if mispronounced:
            words_to_practice = [original for original, _ in mispronounced]
            message += f"Let's practice these words: {', '.join(words_to_practice)}"
        
        return message
