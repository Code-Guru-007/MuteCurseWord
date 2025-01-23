from openai import OpenAI
client = OpenAI(api_key="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")

audio_file = open("temp_audio.wav", "rb")
transcription = client.audio.transcriptions.create(
    file=audio_file,
    model="whisper-1",
    response_format="verbose_json",
    timestamp_granularities=["word"]
)

print(transcription.words)