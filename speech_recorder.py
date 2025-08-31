import wave
import pyaudio
import whisper
import numpy as np
from .speech_analyzer import SpeechAnalyzer

class SpeechRecorder:
    def __init__(self):
        self.analyzer = SpeechAnalyzer()
        self.model = whisper.load_model("base")
        
    def record_audio(self, duration=5):
        CHUNK = 1024
        FORMAT = pyaudio.paFloat32
        CHANNELS = 1
        RATE = 16000
        
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
        
        frames = []
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        return b''.join(frames)
    
    def analyze_recording(self, audio_data, target_text):
        # Save temporary WAV file
        with wave.open("temp.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(4)
            wf.setframerate(16000)
            wf.writeframes(audio_data)
        
        # Transcribe using Whisper
        result = self.model.transcribe("temp.wav")
        transcription = result["text"]
        
        # Analyze speech
        analysis = self.analyzer.analyze_speech(target_text, transcription)
        
        return {
            "transcription": transcription,
            "analysis": analysis
        }