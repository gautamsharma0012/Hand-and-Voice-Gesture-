import speech_recognition as sr
import webbrowser
import os
import platform

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, phrase_time_limit=5)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"Recognized: {command}")
                return command
            except sr.UnknownValueError:
                print("Could not understand.")
                return None
            except sr.RequestError:
                print("No internet connection.")
                return None

    def run_command(self, command):
        if 'open browser' in command:
            webbrowser.open('https://www.google.com')
        elif 'open notepad' in command:
            if platform.system() == "Windows":
                os.system('notepad')
            else:
                print("Notepad only works on Windows.")
        elif 'close app' in command:
            print("Closing app...")
            os._exit(0)
        else:
            print(f"Unrecognized command: {command}")
