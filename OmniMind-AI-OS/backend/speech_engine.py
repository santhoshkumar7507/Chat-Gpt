import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error (no speakers?): {e}")

def listen():
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            # Added a timeout so it doesn't hang forever if there's silence
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        return recognizer.recognize_google(audio)
    except Exception as e:
        print(f"Microphone error: {e}")
        return "Voice Error"

def transcribe_audio(file_path):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except Exception as e:
        print(f"File transcription error: {e}")
        return f"Voice Error: {str(e)}"
