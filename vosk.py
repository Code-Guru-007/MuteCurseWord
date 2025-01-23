import os
import wave
from vosk import Model, KaldiRecognizer

def transcribe_audio_with_vosk(audio_path):
    # Load Vosk model (you can download it from their website)
    model = Model("model")
    
    with wave.open(audio_path, "rb") as audio_file:
        recognizer = KaldiRecognizer(model, audio_file.getframerate())
        audio_data = audio_file.readframes(audio_file.getnframes())
        
        if recognizer.AcceptWaveform(audio_data):
            result = recognizer.Result()
            print(result)
        else:
            print("Could not transcribe audio.")

# Example usage
audio_path = "your_audio_file.wav"
transcribe_audio_with_vosk(audio_path)
