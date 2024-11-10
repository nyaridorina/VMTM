import os
import json
from google.cloud import speech
from google.oauth2 import service_account

# Access the JSON credentials from the environment variable
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if not credentials_path:
    raise ValueError("Google service account credentials not found. Please set the GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable to the path of the credentials file.")

# Check if the provided path is a valid file
if not os.path.isfile(credentials_path):
    raise ValueError(f"The provided GOOGLE_APPLICATION_CREDENTIALS_JSON path '{credentials_path}' is not a valid file.")

# Load the credentials from the JSON file
with open(credentials_path, 'r') as file:
    try:
        credentials_info = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in the credentials file: {e}")

credentials = service_account.Credentials.from_service_account_info(credentials_info)

# Create the SpeechClient using the credentials
client = speech.SpeechClient(credentials=credentials)

# Define list of Hungarian swear words
swear_words_hungarian = ["szar", "hülye", "kurva"]

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
    try:
        response = client.recognize(config=config, audio=audio)
    except Exception as e:
        print(f"Error during speech recognition: {e}")
        return ""

    # Collect transcription results
    if not response.results:
        return ""

    for result in response.results:
        return result.alternatives[0].transcript

    return ""

def detect_swear_words_in_audio(file_path):
    """Detects swear words in the provided audio file."""
    transcribed_text = transcribe_audio(file_path)
    if check_for_swear_words(transcribed_text):
        alert_sound()

def check_for_swear_words(text):
    """Checks if the recognized text contains any swear words."""
    words = text.lower().split()
    return any(word in swear_words_hungarian for word in words)

def alert_sound():
    """Function to handle alert when a swear word is detected."""
    print("Figyelem! Nem megfelelő nyelvezet!")
