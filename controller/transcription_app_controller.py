import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import speech_recognition as sr
from model.gpt2_text_generator import TextGenerator
from view.transcription_app_view import TranscriptionAppView

class TranscriptionAppController:
    def __init__(self, root):
        self.view = TranscriptionAppView(root, self)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.transcribing = False
        self.transcript = ""
        self.generator = TextGenerator()

    def start_recording(self):
        self.transcribing = True
        self.transcript = ""
        self.view.clear_transcript()
        threading.Thread(target=self.transcribe).start()

    def stop_recording(self):
        self.transcribing = False

    def save_transcript(self):
        if self.transcript:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(self.transcript)
                    self.view.show_message("Success", "Transcript saved successfully!")
                except Exception as e:
                    self.view.show_warning("Error", f"Failed to save transcript: {e}")
        else:
            self.view.show_warning("Warning", "No transcript to save!")

    def transcribe(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.transcribing:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio, language="en-US")
                    self.transcript += text + "\n"
                    self.view.update_transcript(text)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    self.view.update_transcript("[Unrecognized speech]")
                except sr.RequestError as e:
                    self.view.update_transcript(f"[Error: {e}]")

    def generate_response(self):
        if self.transcript:
            # Generate response using TextGenerator instance
            response = self.generator.generate_text(self.transcript)
            self.view.show_message("Response", f"Model response:\n{response}")
        else:
            self.view.show_warning("Warning", "No transcript available!")
