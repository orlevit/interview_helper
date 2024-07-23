#copilot
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import speech_recognition as sr
import threading

class TranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Transcription App")
        self.root.geometry("600x400")

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.transcribing = False
        self.transcript = ""

        self.create_widgets()

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(self.root, text="Save Transcript", command=self.save_transcript)
        self.save_button.pack(side=tk.LEFT, padx=10)

    def start_recording(self):
        self.transcribing = True
        self.transcript = ""
        self.text_area.delete(1.0, tk.END)
        threading.Thread(target=self.transcribe).start()

    def stop_recording(self):
        self.transcribing = False

    def save_transcript(self):
        if self.transcript:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.transcript)
                messagebox.showinfo("Success", "Transcript saved successfully!")
        else:
            messagebox.showwarning("Warning", "No transcript to save!")

    def transcribe(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.transcribing:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio, language="he-IL")
                    self.transcript += text + "\n"
                    self.text_area.insert(tk.END, text + "\n")
                    self.text_area.see(tk.END)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    self.text_area.insert(tk.END, "[Unrecognized speech]\n")
                except sr.RequestError as e:
                    self.text_area.insert(tk.END, f"[Error: {e}]\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()
