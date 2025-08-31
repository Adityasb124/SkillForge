import numpy as np

class PronunciationChecker:
    def __init__(self):
        self.common_mistakes = {
            'th': ['d', 't', 'f', 's'],
            'v': ['w', 'b', 'f'],
            'w': ['v', 'u'],
            'r': ['l', 'w'],
            'l': ['r', 'w']
        }
    
    def check(self, audio_path, expected_text, transcribed_text):
        """Check pronunciation accuracy"""
        try:
            # If no transcribed text, return low score
            if not transcribed_text or transcribed_text.strip() == "":
                return {
                    'score': 20,
                    'word_scores': {},
                    'mispronounced_words': expected_text.split(),
                    'phonetic_accuracy': 20
                }
            
            # Compare words
            word_scores = self._compare_words(expected_text, transcribed_text)
            
            # Identify mispronounced words
            mispronounced = self._identify_mispronounced_words(word_scores)
            
            # Calculate overall pronunciation score
            overall_score = self._calculate_pronunciation_score(word_scores, len(mispronounced))
            
            return {
                'score': overall_score,
                'word_scores': word_scores,
                'mispronounced_words': mispronounced,
                'phonetic_accuracy': overall_score
            }
        
        except Exception as e:
            return self._fallback_scoring(expected_text, transcribed_text)
    
    def _compare_words(self, expected, transcribed):
        """Compare expected vs transcribed words"""
        expected_words = expected.lower().split()
        transcribed_words = transcribed.lower().split()
        
        word_scores = {}
        
        for i, expected_word in enumerate(expected_words):
            if i < len(transcribed_words):
                transcribed_word = transcribed_words[i]
                similarity = self._calculate_word_similarity(expected_word, transcribed_word)
                word_scores[expected_word] = similarity
            else:
                word_scores[expected_word] = 0  # Missing word
        
        return word_scores
    
    def _calculate_word_similarity(self, word1, word2):
        """Calculate similarity between two words"""
        if word1 == word2:
            return 100
        
        # Handle empty strings
        if not word1 or not word2:
            return 0
        
        # Simple character-based similarity
        max_len = max(len(word1), len(word2))
        if max_len == 0:
            return 100
        
        # Count matching characters in order
        matches = 0
        min_len = min(len(word1), len(word2))
        
        for i in range(min_len):
            if word1[i] == word2[i]:
                matches += 1
        
        # Calculate similarity score
        similarity = (matches / max_len) * 100
        
        # Bonus for same length
        if len(word1) == len(word2):
            similarity += 10
        
        return min(100, similarity)
    
    def _identify_mispronounced_words(self, word_scores):
        """Identify words that were mispronounced"""
        mispronounced = []
        threshold = 70  # Words with score below 70% are considered mispronounced
        
        for word, score in word_scores.items():
            if score < threshold:
                mispronounced.append(word)
        
        return mispronounced
    
    def _calculate_pronunciation_score(self, word_scores, num_mispronounced):
        """Calculate overall pronunciation score"""
        if not word_scores:
            return 50
        
        avg_word_score = np.mean(list(word_scores.values()))
        
        # Penalty for mispronounced words
        penalty = min(num_mispronounced * 8, 40)
        
        final_score = max(0, avg_word_score - penalty)
        return round(final_score, 1)
    
    def _fallback_scoring(self, expected, transcribed):
        """Fallback scoring when analysis fails"""
        # Basic word count comparison
        expected_words = expected.lower().split() if expected else []
        transcribed_words = transcribed.lower().split() if transcribed else []
        
        if not expected_words:
            return {'score': 50, 'word_scores': {}, 'mispronounced_words': [], 'phonetic_accuracy': 50}
        
        # Simple word matching
        matches = 0
        word_scores = {}
        
        for word in expected_words:
            if word in transcribed_words:
                matches += 1
                word_scores[word] = 100
            else:
                word_scores[word] = 0
        
        score = (matches / len(expected_words)) * 100 if expected_words else 0
        mispronounced = [word for word, s in word_scores.items() if s < 70]
        
        return {
            'score': round(score, 1),
            'word_scores': word_scores,
            'mispronounced_words': mispronounced,
            'phonetic_accuracy': round(score, 1)
        }
