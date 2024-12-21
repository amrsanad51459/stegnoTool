import tkinter as tk
from tkinter import messagebox
import subprocess

class StegToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("StegTools - Audio, Video, Image, Text")
        self.root.geometry("400x400")
        self.root.configure(bg="black")

        # Title Label
        self.title_label = tk.Label(root, text="StegTools", fg="#00FF00", bg="black", font=("Courier", 18, "bold"))
        self.title_label.pack(pady=20)

        # Buttons
        self.audio_button = tk.Button(root, text="Audio Steganography", command=self.audio_tool, fg="black", bg="#00FF00", font=("Courier", 12))
        self.audio_button.pack(pady=10)

        self.video_button = tk.Button(root, text="Video Steganography", command=self.video_tool, fg="black", bg="#00FF00", font=("Courier", 12))
        self.video_button.pack(pady=10)

        self.image_button = tk.Button(root, text="Image Steganography", command=self.image_tool, fg="black", bg="#00FF00", font=("Courier", 12))
        self.image_button.pack(pady=10)

        self.text_button = tk.Button(root, text="Text Steganography", command=self.text_tool, fg="black", bg="#00FF00", font=("Courier", 12))
        self.text_button.pack(pady=10)

    def audio_tool(self):
        """Runs the audio steganography tool."""
        try:
            subprocess.run(["python", "aud.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Error running audio tool: {e}")

    def video_tool(self):
        """Runs the video steganography tool."""
        try:
            subprocess.run(["python", "vd.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Error running video tool: {e}")

    def image_tool(self):
        """Runs the image steganography tool."""
        try:
            subprocess.run(["python", "img.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Error running image tool: {e}")

    def text_tool(self):
        """Runs the text steganography tool."""
        try:
            subprocess.run(["python", "txt.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Error running text tool: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StegToolsGUI(root)
    root.mainloop()
