import tkinter as tk
from controller.transcription_app_controller import TranscriptionAppController

if __name__ == "__main__":
    root = tk.Tk()
    controller = TranscriptionAppController(root)
    root.mainloop()