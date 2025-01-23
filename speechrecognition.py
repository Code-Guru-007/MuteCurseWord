import speech_recognition as sr

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        response = recognizer.recognize_google(audio, show_all=True)
        print(response)
        word_timings = []
        if "alternative_transcripts" in response:
            for alt in response["alternative_transcripts"]:
                for word_info in alt["words"]:
                    word_timings.append((word_info['word'], word_info['start_time'], word_info['end_time']))
        return word_timings
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio."
    except sr.RequestError:
        return "Could not request results from Sphinx."

# Usage
transcription = transcribe_audio("temp_audio.wav")
print(transcription)
