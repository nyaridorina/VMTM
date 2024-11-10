import sounddevice as sd
import numpy as np
import tempfile
import soundfile as sf
import pyttsx3
import queue
import threading
import time

# Initialize text-to-speech for alert
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Define list of Hungarian swear words
swear_words_hungarian = ["szitokszó1", "szitokszó2", "szitokszó3"]

# Queue to store audio data
audio_queue = queue.Queue()
swear_detected = False
detection_active = False

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
    audio_queue.put(indata.copy())

def start_detection():
    """Starts the audio detection process in a new thread."""
    global detection_active, swear_detected
    detection_active = True
    swear_detected = False

    def detection_task():
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav_file:
            with sd.InputStream(samplerate=16000, channels=1, callback=audio_callback):
                print("Listening for swear words...")
                while detection_active:
                    audio_data = audio_queue.get()
                    sf.write(temp_wav_file.name, audio_data, 16000, format='WAV')
                    
                    # Replace with an actual transcription API call here
                    fake_transcribed_text = "szitokszó1"  # Placeholder for testing
                    
                    if check_for_swear_words(fake_transcribed_text):
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
