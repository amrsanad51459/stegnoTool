import numpy as np
import imageio
import tkinter as tk
from tkinter import filedialog, messagebox

END_MARKER = "#####END#####"  # Marker to indicate the end of the hidden message


# Convert video to frames using imageio
def video_to_frames(video_path):
    """Convert video file to a list of frames."""
    reader = imageio.get_reader(video_path)
    frames = []
    for frame in reader:
        frames.append(frame)
    return frames


# Convert frames back to video using imageio
def frames_to_video(frames, output_path, fps=30):
    """Convert list of frames back to a video file."""
    writer = imageio.get_writer(output_path, fps=fps)
    for frame in frames:
        writer.append_data(frame)
    writer.close()


# LSB Steganography for Video using imageio
def lsb_hide_video(video_path, message, output_path):
    """Hide a message in a video file using LSB."""
    message += END_MARKER
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    frames = video_to_frames(video_path)

    if len(binary_message) > len(frames) * frames[0].shape[0] * frames[0].shape[1]:
        raise ValueError("Message too large to hide in this video.")

    binary_message_index = 0
    for i, frame in enumerate(frames):
        for x in range(frame.shape[0]):
            for y in range(frame.shape[1]):
                for c in range(frame.shape[2]):  # Loop through RGB channels
                    if binary_message_index < len(binary_message):
                        frame[x, y, c] = (frame[x, y, c] & 0xFE) | int(binary_message[binary_message_index])
                        binary_message_index += 1

    frames_to_video(frames, output_path)
    messagebox.showinfo("Success", f"Message hidden successfully in {output_path}")


def lsb_extract_video(video_path):
    """Extract the hidden message from a video file using LSB."""
    frames = video_to_frames(video_path)

    binary_message = ""
    for frame in frames:
        for x in range(frame.shape[0]):
            for y in range(frame.shape[1]):
                for c in range(frame.shape[2]):
                    binary_message += str(frame[x, y, c] & 1)  # Extract the LSB

    hidden_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

    end_index = hidden_message.find(END_MARKER)
    if end_index != -1:
        return hidden_message[:end_index]
    return "No hidden message found!"


# GUI Application
class VideoSteganoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Steganography Tool")
        self.root.configure(bg="black")
        self.file_path = ""
        self.message_file_path = ""

        # Title
        self.title_label = tk.Label(root, text="Video Steganography Tool", fg="#00FF00", bg="black",
                                    font=("Courier", 18, "bold"))
        self.title_label.pack(pady=10)

        # File Section
        self.file_frame = tk.Frame(root, bg="black")
        self.file_frame.pack(pady=5)

        self.file_label = tk.Label(self.file_frame, text="Video File (AVI):", fg="#00FF00", bg="black")
        self.file_label.grid(row=0, column=0)
        self.file_entry = tk.Entry(self.file_frame, width=40)
        self.file_entry.grid(row=0, column=1)
        self.file_button = tk.Button(self.file_frame, text="Browse", command=self.load_video_file, fg="black",
                                     bg="#00FF00")
        self.file_button.grid(row=0, column=2)

        # Message Section
        self.message_frame = tk.Frame(root, bg="black")
        self.message_frame.pack(pady=5)

        self.message_label = tk.Label(self.message_frame, text="Select Text File for Hidden Message:", fg="#00FF00",
                                      bg="black")
        self.message_label.grid(row=0, column=0)
        self.message_button = tk.Button(self.message_frame, text="Browse", command=self.load_message_file, fg="black",
                                        bg="#00FF00")
        self.message_button.grid(row=0, column=1)

        # Buttons
        self.encrypt_button = tk.Button(root, text="Hide Message", command=self.encrypt, fg="black", bg="#00FF00")
        self.encrypt_button.pack(pady=5)
        self.decrypt_button = tk.Button(root, text="Retrieve Message", command=self.decrypt, fg="black", bg="#00FF00")
        self.decrypt_button.pack(pady=5)

        # Result Section
        self.result_label = tk.Label(root, text="", fg="#00FF00", bg="black", font=("Courier", 12, "bold"))
        self.result_label.pack()

    def load_video_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.avi")])
        if self.file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, self.file_path)

    def load_message_file(self):
        self.message_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.message_file_path:
            messagebox.showinfo("File Selected", f"Message File: {self.message_file_path}")

    def encrypt(self):
        if not self.file_path:
            messagebox.showerror("Error", "No video file selected!")
            return
        if not self.message_file_path:
            messagebox.showerror("Error", "No message file selected!")
            return

        with open(self.message_file_path, 'r') as file:
            message = file.read().strip()

        if not message:
            messagebox.showerror("Error", "No message found in the file!")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI", "*.avi")])
        lsb_hide_video(self.file_path, message, output_path)

    def decrypt(self):
        if not self.file_path:
            messagebox.showerror("Error", "No video file selected!")
            return

        hidden_message = lsb_extract_video(self.file_path)

        self.result_label.config(text=f"Hidden Message: {hidden_message}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoSteganoApp(root)
    root.mainloop()
