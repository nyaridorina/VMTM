import os
from google.cloud import speech
from google.oauth2 import service_account
import sounddevice as sd
import soundfile as sf
import queue
import threading
import time
import tempfile

# Access API key from environment variable
API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")

# Configure Google Speech Client with API Key
client = speech.SpeechClient()

# Define list of Hungarian swear words
swear_words_hungarian = ["szar", "hülye", "kurva"]

# Queue to store audio data
audio_queue = queue.Queue()
swear_detected = False
detection_active = False

def transcribe_audio(file_path):
    """Transcribes the given audio file."""
    with open(file_path, "rb") as audio_file:
        audio_content = audio_file.read()
        
    # Set up request
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="hu-HU",
    )

    # Call the Speech-to-Text API
    response = client.recognize(config=config, audio=audio)

    # Collect transcription results
    for result in response.results:
        return result.alternatives[0].transcript

    return ""

# The rest of your code remains the same...
