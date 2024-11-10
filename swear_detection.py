import speech_recognition as sr
import time

# Define the list of Hungarian swear words
swear_words_hungarian = [
    "szitokszó1", "szitokszó2", "szitokszó3"  # Replace with actual Hungarian swear words
]

# Initialize SpeechRecognition
recognizer = sr.Recognizer()

# Global variable to control detection and track if a swear word was detected
detection_active = False
swear_detected = False

def start_detection():
    """Listens for audio input and checks for swear words."""
    global swear_detected

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        print("Listening for swear words...")

        try:
            # Capture audio
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            # Convert audio to text in Hungarian
            text = recognizer.recognize_google(audio, language="hu-HU")
            print("Detected speech:", text)

            # Check if the text contains any Hungarian swear words
            if check_for_swear_words(text):
                print("Swear word detected!")
                swear_detected = True  # Update status if swear word is detected

        except sr.UnknownValueError:
            # Audio was unintelligible
            print("Could not understand audio.")
        except sr.RequestError as e:
            # Issue with the speech recognition service
            print("Could not request results; {0}".format(e))

def stop_detection():
    """Stops the detection process."""
    global detection_active
    detection_active = False

def is_swear_detected():
    """Checks if a swear word was detected and resets status."""
    global swear_detected
    if swear_detected:
        # Reset the detected flag after checking
        swear_detected = False
        return True
    return False

def check_for_swear_words(text):
    """Checks if the text contains any swear words."""
    words = text.lower().split()
    return any(word in swear_words_hungarian for word in words)
