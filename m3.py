import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import speech_recognition as sr
import threading
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class TranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Transcription App")
        self.root.geometry("600x400")

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.transcribing = False
        self.transcript = ""

        # Load GPT-2 model and tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')

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
        # Once transcription stops, generate a response
        self.generate_response()

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
                    text = self.recognizer.recognize_google(audio, language="en-US")
                    self.transcript += text + "\n"
                    self.text_area.insert(tk.END, text + "\n")
                    self.text_area.see(tk.END)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    self.text_area.insert(tk.END, "[Unrecognized speech]\n")
                except sr.RequestError as e:
                    self.text_area.insert(tk.END, f"[Error: {e}]\n")

    def generate_response(self):
        if self.transcript:
            input_ids = self.tokenizer.encode(self.transcript, return_tensors='pt')
            with torch.no_grad():
                output = self.model.generate(input_ids, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2)
            response = self.tokenizer.decode(output[0], skip_special_tokens=True)
            messagebox.showinfo("Response", f"Model response:\n{response}")
        else:
            messagebox.showwarning("Warning", "No transcript available!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()
