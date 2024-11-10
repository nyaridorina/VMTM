import speech_recognition as sr
import pyttsx3
import time

# Define a list of Hungarian swear words
swear_words_hungarian = [
    "szar", "kurva", "hülye"  # Replace with actual Hungarian swear words
]

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speaking rate if needed

def alert_sound():
    """Function to play an alert sound using text-to-speech."""
    engine.say("Figyelem! Nem megfelelő nyelvezet!")
    engine.runAndWait()

def check_for_swear_words(text):
    """Function to check if the text contains any swear words."""
    words = text.lower().split()  # Convert text to lowercase and split into words
    return any(word in swear_words_hungarian for word in words)

# Main loop to listen for swear words in real-time
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
    print("Hallgatózik csúnya szavakra...")

    while True:
        try:
            # Capture audio from microphone
            audio = recognizer.listen(source)
            # Convert audio to text in Hungarian
            text = recognizer.recognize_google(audio, language="hu-HU")
            print("Ezt mondta:", text)

            # Check if the text contains any Hungarian swear words
            if check_for_swear_words(text):
                alert_sound()  # Play alert if swear word is detected

            # Small delay before listening again
            time.sleep(0.5)

        except sr.UnknownValueError:
            # Speech was unintelligible
            print("Hallgatózik...")
        except sr.RequestError:
            # Issue with the speech recognition service
            print("Hiba a beszédfelismerő szolgáltatásban.")
            break
