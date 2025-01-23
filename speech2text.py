import whisper

def transcribe_audio_with_whisper(audio_path):
    model = whisper.load_model("small")  # You can also use 'small', 'medium', or 'large' models
    res = model.transcribe(audio_path, word_timestamps=True)
    # with open("test.txt", "w") as file:
    # # Write "Hello world" to the file
    #     file.write(str(res))
    print(res["text"])
    result = []
    for segment in res['segments']:
        for word_info in segment['words']:
            result.append({
                'word': word_info['word'],
                'start': word_info['start'],
                'end': word_info['end']
            })
    return result

# Example usage
# audio_path = "./temp_audio.wav"
# transcribe_audio_with_whisper(audio_path)