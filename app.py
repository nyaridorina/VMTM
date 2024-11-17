import speech_recognition as sr
import pygame
from gtts import gTTS
import os

# Initialize alert sound and TTS message
pygame.init()
alert_sound = "alert.wav"  # Ensure you have an alert sound file

# Generate TTS message
warning_message = "Ön beszéderkölcsi szabálysértést követett el."
tts = gTTS(warning_message, lang='hu')
tts.save("warning.mp3")

# List of Hungarian swear words
swear_words = ['hülye', 'kurva', 'szar']

def play_alert():
    pygame.mixer.music.load(alert_sound)
    pygame.mixer.music.play()

def play_warning():
    os.system("mpg123 warning.mp3")  # Use mpg123 for playing mp3 files

# Speech recognition setup
recognizer = sr.Recognizer()
microphone = sr.Microphone()

print("App is running. Say something...")

try:
    while True:
        with microphone as source:
            # Adjust for ambient noise and record
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

        # Recognize speech
        try:
            text = recognizer.recognize_google(audio, language="hu-HU")
            print(f"Recognized: {text}")

            # Check for swear words
            if any(swear in text.lower() for swear in swear_words):
                print("Swear word detected!")
                play_alert()
                play_warning()

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Speech Recognition error: {e}")

except KeyboardInterrupt:
    print("Program stopped.")
