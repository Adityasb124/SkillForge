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

        this.mediaRecorder.onstop = () => {
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
            this.onRecordingComplete(audioBlob);
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

    onRecordingComplete(audioBlob) {
        // This will be overridden by the main application
        console.log('Recording completed:', audioBlob);
    }
}

// Global audio recorder instance
const audioRecorder = new AudioRecorder();
