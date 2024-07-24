import tkinter as tk
from tkinter import scrolledtext, messagebox

class TranscriptionAppView:
    def __init__(self, root, controller):
        self.root = root
        self.root.title("Real-Time Transcription App")
        self.root.geometry("600x400")
        self.controller = controller

        self.create_widgets()

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20)
        self.text_area.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Recording", command=self.controller.start_recording)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.controller.stop_recording)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(self.root, text="Save Transcript", command=self.controller.save_transcript)
        self.save_button.pack(side=tk.LEFT, padx=10)

    def update_transcript(self, text):
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)

    def clear_transcript(self):
        self.text_area.delete(1.0, tk.END)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_warning(self, title, message):
        messagebox.showwarning(title, message)
