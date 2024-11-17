import speech_recognition as sr
import sounddevice as sd
import numpy as np
import pygame
from gtts import gTTS
import os

# Initialize alert sound and TTS message
pygame.init()
alert_sound = "audio/alert.wav"  # Ensure you have an alert sound file in 'audio/'

# Generate TTS message
warning_message = "Ön beszéderkölcsi szabálysértést követett el."
tts = gTTS(warning_message, lang='hu')
tts.save("audio/warning.mp3")

# Load swear words from file
with open("config/swear_words.txt", "r", encoding="utf-8") as f:
    swear_words = [line.strip().lower() for line in f]

def play_alert():
    pygame.mixer.music.load(alert_sound)
    pygame.mixer.music.play()

def play_warning():
    os.system("mpg123 audio/warning.mp3")  # Use mpg123 for playing mp3 files

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="hu-HU")
        print(f"Recognized: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Speech Recognition error: {e}")
        return ""

def main():
    print("App is running. Say something...")
    while True:
        text = recognize_speech()
        if any(swear in text for swear in swear_words):
            print("Swear word detected!")
            play_alert()
            play_warning()

if __name__ == "__main__":
    main()
