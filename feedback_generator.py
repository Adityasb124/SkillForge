import random

class FeedbackGenerator:
    def __init__(self):
        self.positive_messages = [
            "Great job! You're doing amazing! 🌟",
            "Fantastic reading! Keep it up! 🎉",
            "You're getting better every time! 👏",
            "Wonderful pronunciation! 🎊",
            "You're a reading superstar! ⭐"
        ]
        
        self.encouragement_messages = [
            "Don't worry, practice makes perfect! 💪",
            "You're learning so well! Try again! 🎯",
            "Almost there! One more try! 🚀",
            "Great effort! Let's practice together! 🤝",
            "You're on the right track! Keep going! 📈"
        ]
    
    def generate_feedback(self, analysis_result):
        """Generate kid-friendly feedback"""
        score = analysis_result['overall_score']
        feedback = {
            'score': round(score, 1),
            'message': self._get_main_message(score),
            'specific_feedback': [],
            'encouragement': random.choice(self.positive_messages if score >= 70 else self.encouragement_messages)
        }
        
        # Add specific feedback for pronunciation issues
        if 'pronunciation_score' in analysis_result:
            feedback['specific_feedback'].extend(
                self._generate_pronunciation_feedback(analysis_result['pronunciation_score'])
            )
        
        # Add fluency feedback
        if 'fluency_analysis' in analysis_result:
            feedback['specific_feedback'].extend(
                self._generate_fluency_feedback(analysis_result['fluency_analysis'])
            )
        
        return feedback
    
    def _get_main_message(self, score):
        """Get main feedback message based on score"""
        if score >= 90:
            return "Perfect! You nailed it! 🏆"
        elif score >= 80:
            return "Excellent work! Almost perfect! 🥇"
        elif score >= 70:
            return "Good job! Just a little more practice! 🥈"
        elif score >= 60:
            return "Nice try! Let's work on a few words! 🥉"
        else:
            return "Great effort! Let's practice together! 💝"
    
    def _generate_pronunciation_feedback(self, pronunciation_data):
        """Generate pronunciation-specific feedback"""
        feedback = []
        if 'mispronounced_words' in pronunciation_data:
            for word in pronunciation_data['mispronounced_words'][:3]:  # Limit to 3 words
                feedback.append(f"Try saying '{word}' a bit clearer! 🗣️")
        return feedback
    
    def _generate_fluency_feedback(self, fluency_data):
        """Generate fluency-specific feedback"""
        feedback = []
        if fluency_data.get('hesitations', 0) > 2:
            feedback.append("Try reading a bit more smoothly! Take your time! ⏰")
        if fluency_data.get('speaking_rate', 0) < 100:
            feedback.append("You can speak a little faster! 🏃‍♀️")
        elif fluency_data.get('speaking_rate', 0) > 200:
            feedback.append("Try slowing down just a little! 🐌")
        return feedback
