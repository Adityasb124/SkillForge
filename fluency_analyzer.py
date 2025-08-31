import librosa
import numpy as np
from scipy import signal

class FluencyAnalyzer:
    def __init__(self):
        self.silence_threshold = 0.01
        self.min_pause_duration = 0.3
        self.expected_speaking_rate = 150  # words per minute
    
    def analyze(self, audio_path, transcribed_text):
        """Analyze speech fluency"""
        try:
            # Load audio
            y, sr = librosa.load(audio_path)
            
            # Detect pauses and hesitations
            pauses = self._detect_pauses(y, sr)
            
            # Calculate speaking rate
            speaking_rate = self._calculate_speaking_rate(transcribed_text, len(y) / sr)
            
            # Detect stuttering patterns
            stuttering_score = self._detect_stuttering(y, sr, transcribed_text)
            
            # Calculate fluency score
            fluency_score = self._calculate_fluency_score(
                pauses, speaking_rate, stuttering_score
            )
            
            return {
                'score': fluency_score,
                'speaking_rate': speaking_rate,
                'pause_count': len(pauses),
                'hesitations': len(pauses),
                'stuttering_detected': stuttering_score < 80,
                'recommendations': self._generate_recommendations(
                    speaking_rate, len(pauses), stuttering_score
                )
            }
        
        except Exception as e:
            return self._fallback_fluency_analysis(transcribed_text)
    
    def _detect_pauses(self, audio, sr):
        """Detect pauses in speech"""
        # Calculate RMS energy
        frame_length = int(0.025 * sr)  # 25ms frames
        hop_length = int(0.01 * sr)     # 10ms hop
        
        rms = librosa.feature.rms(y=audio, frame_length=frame_length, hop_length=hop_length)[0]
        
        # Find silent regions
        silent_frames = rms < self.silence_threshold
        
        # Convert frame indices to time
        times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)
        
        # Group consecutive silent frames into pauses
        pauses = []
        pause_start = None
        
        for i, is_silent in enumerate(silent_frames):
            if is_silent and pause_start is None:
                pause_start = times[i]
            elif not is_silent and pause_start is not None:
                pause_duration = times[i] - pause_start
                if pause_duration >= self.min_pause_duration:
                    pauses.append({
                        'start': pause_start,
                        'end': times[i],
                        'duration': pause_duration
                    })
                pause_start = None
        
        return pauses
    
    def _calculate_speaking_rate(self, text, duration):
        """Calculate words per minute"""
        if duration == 0:
            return 0
        
        word_count = len(text.split())
        return (word_count / duration) * 60
    
    def _detect_stuttering(self, audio, sr, text):
        """Detect stuttering patterns"""
        # Simple stuttering detection based on repetitive patterns
        words = text.lower().split()
        
        # Count repeated words
        repeated_words = 0
        for i in range(len(words) - 1):
            if words[i] == words[i + 1]:
                repeated_words += 1
        
        # Calculate stuttering score (higher is better)
        total_words = len(words)
        if total_words == 0:
            return 100
        
        repetition_rate = repeated_words / total_words
        stuttering_score = max(0, 100 - (repetition_rate * 200))
        
        return stuttering_score
    
    def _calculate_fluency_score(self, pauses, speaking_rate, stuttering_score):
        """Calculate overall fluency score"""
        # Rate score (optimal range: 120-180 WPM)
        if 120 <= speaking_rate <= 180:
            rate_score = 100
        elif speaking_rate < 120:
            rate_score = max(0, (speaking_rate / 120) * 100)
        else:
            rate_score = max(0, 100 - ((speaking_rate - 180) / 50) * 20)
        
        # Pause score (fewer pauses = better)
        pause_penalty = min(len(pauses) * 10, 40)
        pause_score = max(0, 100 - pause_penalty)
        
        # Combine scores
        fluency_score = (rate_score * 0.4 + pause_score * 0.3 + stuttering_score * 0.3)
        
        return round(fluency_score, 1)
    
    def _generate_recommendations(self, speaking_rate, pause_count, stuttering_score):
        """Generate recommendations for improvement"""
        recommendations = []
        
        if speaking_rate < 100:
            recommendations.append("Try speaking a little faster")
        elif speaking_rate > 200:
            recommendations.append("Try speaking a little slower")
        
        if pause_count > 3:
            recommendations.append("Practice reading more smoothly")
        
        if stuttering_score < 80:
            recommendations.append("Take your time with each word")
        
        return recommendations
    
    def _fallback_fluency_analysis(self, text):
        """Fallback analysis when audio processing fails"""
        word_count = len(text.split())
        
        return {
            'score': 75,  # Default neutral score
            'speaking_rate': word_count * 2,  # Rough estimate
            'pause_count': 0,
            'hesitations': 0,
            'stuttering_detected': False,
            'recommendations': ["Keep practicing!"]
        }
