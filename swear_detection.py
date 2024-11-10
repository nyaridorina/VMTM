import os
import subprocess
from google.cloud import speech

# Initialize the SpeechClient without specifying credentials
client = speech.SpeechClient()

# Define list of Hungarian swear words
swear_words_hungarian = ["szar", "hülye", "kurva"]

def convert_audio(input_path, output_path):
    """Converts the audio file to the required format for speech recognition."""
    command = [
        'ffmpeg', '-y', '-i', input_path,
        '-ar', '16000',    # Sample rate
        '-ac', '1',        # Mono channel
        '-f', 'wav',
        output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def transcribe_audio(file_path):
    """Transcribes the given audio file."""
    with open(file_path, "rb") as audio_file:
        audio_content = audio_file.read()

    # Set up the request
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="hu-HU",
    )

    # Call the Speech-to-Text API
    try:
        response = client.recognize(config=config, audio=audio)
    except Exception as e:
        print(f"Error during speech recognition: {e}")
        return ""

    # Collect transcription results
    if not response.results:
        return ""

    return response.results[0].alternatives[0].transcript

def detect_swear_words_in_audio(file_path):
    """Detects swear words in the provided audio file."""
    transcribed_text = transcribe_audio(file_path)
    if check_for_swear_words(transcribed_text):
        alert_sound()
        return True
    return False

def check_for_swear_words(text):
    """Checks if the recognized text contains any swear words."""
    words = text.lower().split()
    return any(word in swear_words_hungarian for word in words)

def alert_sound():
    """Handles the alert when a swear word is detected."""
    print("Figyelem! Nem megfelelő nyelvezet!")
