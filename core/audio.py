import os


def transcribe_audio(audio_bytes: bytes) -> str:
    from groq import Groq
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    transcription = client.audio.transcriptions.create(
        file=("recording.wav", audio_bytes),
        model="whisper-large-v3",
        response_format="text",
    )
    return transcription.strip()
