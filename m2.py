# chatgpt 3.5
import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
import threading


class TranscriptionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Real-time Interview Transcription App")

        self.is_recording = False
        self.transcript = ""

        self.text_widget = tk.Text(master, wrap=tk.WORD, height=20, width=60)
        self.text_widget.pack(padx=10, pady=10)

        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(master, text="Save Transcript", command=self.save_transcript, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.stop_listening = None

    def start_recording(self):
        self.is_recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.transcript = ""
        self.text_widget.delete(1.0, tk.END)

        self.stop_listening = self.recognizer.listen_in_background(self.microphone, self.process_audio)

    def stop_recording(self):
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)

        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)

    def save_transcript(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.transcript)

    def process_audio(self, recognizer, audio_data):
        try:
            text = recognizer.recognize_google(audio_data, language="he-IL")
            if text:
                self.update_transcript(text)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def update_transcript(self, text):
        # Add dot and new line only if there's a pause between sentences
        if self.transcript and text:
            last_char = self.transcript[-1]
            if last_char != "." and last_char != "\n":
                self.transcript += ".\n"  # End previous sentence and start new line

        self.transcript += text + " "
        self.text_widget.insert(tk.END, text + " ")
        self.text_widget.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()
