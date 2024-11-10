import os
from google.cloud import speech
from google.oauth2 import service_account
import soundfile as sf
import queue
import threading
import time
import tempfile


# Access API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
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

def start_detection():
    """Starts the audio detection process in a new thread."""
    global detection_active, swear_detected
    detection_active = True
    swear_detected = False

    def detection_task():
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav_file:
            while detection_active:
                # Assuming you have a pre-recorded or real-time captured audio file at `temp_wav_file.name`
                # This is where you handle getting new audio data (e.g., from a recording device)
                
                transcribed_text = transcribe_audio(temp_wav_file.name)
                
                if check_for_swear_words(transcribed_text):
                    swear_detected = True
                    alert_sound()
                    break  # Stop detection after detecting a swear word
                time.sleep(0.5)

    detection_thread = threading.Thread(target=detection_task)
    detection_thread.start()

def stop_detection():
    """Stops the detection process."""
    global detection_active
    detection_active = False

def is_swear_detected():
    """Checks if a swear word was detected and resets status."""
    global swear_detected
    if swear_detected:
        swear_detected = False
        return True
    return False

def check_for_swear_words(text):
    """Checks if the recognized text contains any swear words."""
    words = text.lower().split()
    return any(word in swear_words_hungarian for word in words)

def alert_sound():
    """Function to play an alert sound using text-to-speech."""
    print("Figyelem! Nem megfelelő nyelvezet!")
