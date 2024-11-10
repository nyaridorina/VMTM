import sounddevice as sd
import numpy as np
import queue
import tempfile
import soundfile as sf
import pyttsx3

# Initialize text-to-speech for alert
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speaking rate if needed

# Define list of Hungarian swear words
swear_words_hungarian = ["szar", "kurva", "hülye"]

# Queue to store audio data
audio_queue = queue.Queue()

def alert_sound():
    """Function to play an alert sound using text-to-speech."""
    engine.say("Figyelem! Nem megfelelő nyelvezet!")
    engine.runAndWait()

def check_for_swear_words(text):
    """Checks if the recognized text contains any swear words."""
    words = text.lower().split()
    return any(word in swear_words_hungarian for word in words)

def audio_callback(indata, frames, time, status):
    """Callback function to process each audio chunk."""
    if status:
        print(status)
    # Put the audio data in the queue
    audio_queue.put(indata.copy())

def start_detection():
    """Function to start real-time audio detection."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav_file:
        # Open an input audio stream
        with sd.InputStream(samplerate=16000, channels=1, callback=audio_callback):
            print("Listening for swear words...")
            while True:
                # Get audio data from the queue
                audio_data = audio_queue.get()

                # Write the audio data to a temporary WAV file
                sf.write(temp_wav_file.name, audio_data, 16000, format='WAV')

                # Here you could send `temp_wav_file.name` to a speech-to-text API
                # For example, use Google Speech-to-Text or another provider to transcribe audio
                # Example transcription response (replace this with actual API call result)
                fake_transcribed_text = "szitokszó1 például"  # Replace with actual API response

                # Check for swear words in the transcribed text
                if check_for_swear_words(fake_transcribed_text):
                    alert_sound()  # Play alert if a swear word is detected
                    break
