class AudioRecorder {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.stream = null;
    }

    async requestPermissions() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                audio: true, 
                video: false 
            });
            return true;
        } catch (error) {
            console.error('Error accessing microphone:', error);
            alert('Please allow microphone access to use this feature!');
            return false;
        }
    }

    async startRecording() {
        if (!this.stream) {
            const hasPermission = await this.requestPermissions();
            if (!hasPermission) return false;
        }

        this.audioChunks = [];
        this.mediaRecorder = new MediaRecorder(this.stream);
        
        this.mediaRecorder.ondataavailable = (event) => {
            this.audioChunks.push(event.data);
        };

        this.mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
            await this.sendAudioToServer(audioBlob);
            this.audioChunks = [];
        };

        this.mediaRecorder.start();
        this.isRecording = true;
        return true;
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
        }
    }

    async sendAudioToServer(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob);
        
        try {
            const response = await fetch('/api/lessons/speech/recognize', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            
            if (data.success) {
                document.getElementById('transcription').textContent = data.transcription;
            }
        } catch (error) {
            console.error('Error sending audio:', error);
        }
    }

    onRecordingComplete(audioBlob) {
        // This will be overridden by the main application
        console.log('Recording completed:', audioBlob);
    }
}

// Global audio recorder instance
const audioRecorder = new AudioRecorder();

document.addEventListener('DOMContentLoaded', () => {
    // Request microphone access
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                await sendAudioToServer(audioBlob);
                audioChunks = [];
            };
        })
        .catch(error => console.error('Microphone access denied:', error));
});

function startRecording() {
    audioChunks = [];
    mediaRecorder.start();
    document.getElementById('startBtn').disabled = true;
    document.getElementById('stopBtn').disabled = false;
}

function stopRecording() {
    mediaRecorder.stop();
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
}