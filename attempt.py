from datetime import datetime
from bson import ObjectId

class Attempt:
    def __init__(self, target_text, spoken_text, score, pronunciation_score=None, fluency_score=None):
        self._id = ObjectId()  # MongoDB unique identifier
        self.timestamp = datetime.utcnow()
        self.target_text = target_text
        self.spoken_text = spoken_text
        self.score = score
        self.pronunciation_score = pronunciation_score
        self.fluency_score = fluency_score
    
    def to_dict(self):
        return {
            "_id": self._id,
            "timestamp": self.timestamp,
            "target_text": self.target_text,
            "spoken_text": self.spoken_text,
            "score": self.score,
            "pronunciation_score": self.pronunciation_score,
            "fluency_score": self.fluency_score
        }
    
    @staticmethod
    def from_dict(data):
        attempt = Attempt(
            target_text=data["target_text"],
            spoken_text=data["spoken_text"],
            score=data["score"]
        )
        attempt._id = data.get("_id", ObjectId())
        attempt.pronunciation_score = data.get("pronunciation_score")
        attempt.fluency_score = data.get("fluency_score")
        attempt.timestamp = data.get("timestamp", datetime.utcnow())
        return attempt