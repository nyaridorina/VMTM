import os
import json
from google.cloud import speech
from google.oauth2 import service_account

# Access the JSON credentials from the environment variable
credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if not credentials_json:
    raise ValueError("Google service account credentials not found. Please set the GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable.")

# Load the credentials from the JSON string
credentials_info = json.loads(credentials_json)
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

# Flask application
def start_flask_app():
    from flask import Flask, request, jsonify
    import tempfile

    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Welcome to the Swear Word Detection API!"

    @app.route('/upload-audio', methods=['POST'])
    def upload_audio():
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Save the uploaded audio to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            audio_file.save(temp_audio.name)
            temp_audio_path = temp_audio.name
        
        try:
            # Detect swear words in the provided audio file
            detect_swear_words_in_audio(temp_audio_path)
        finally:
            os.unlink(temp_audio_path)
        
        return jsonify({'message': 'Audio file processed successfully'}), 200

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
