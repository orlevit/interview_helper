# claude 3.5
import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
import threading
import pyaudio
import wave
import os
import time

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
        self.audio_queue = []

    def start_recording(self):
        self.is_recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.transcript = ""
        self.text_widget.delete(1.0, tk.END)
        threading.Thread(target=self.record_audio).start()
        threading.Thread(target=self.process_audio).start()

    def stop_recording(self):
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)

    def save_transcript(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.transcript)

    def record_audio(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        RECORD_SECONDS = 0.1

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        while self.is_recording:
            frames = []
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            audio_data = b''.join(frames)
            self.audio_queue.append(audio_data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def process_audio(self):
        while self.is_recording or self.audio_queue:
            if self.audio_queue:
                audio_data = self.audio_queue.pop(0)
                self.transcribe_audio(audio_data)
            else:
                time.sleep(0.1)

    def transcribe_audio(self, audio_data):
        audio_file = "temp_audio.wav"
        with wave.open(audio_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(audio_data)

        with sr.AudioFile(audio_file) as source:
            audio = self.recognizer.record(source)

        try:
            text = self.recognizer.recognize_google(audio, language="he-IL")
            if text:
                self.transcript += text + " "
                self.text_widget.insert(tk.END, text + " ")
                self.text_widget.see(tk.END)
        except sr.UnknownValueError:
            pass  # Silence was detected or speech wasn't recognized
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        os.remove(audio_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()