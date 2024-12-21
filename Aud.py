import wave
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

END_MARKER = "#####END#####"  # Marker to indicate the end of the hidden message


def lsb_hide_audio(wav_path, txt_path, output_path):
    """Hide a message from a .txt file into a WAV file using LSB."""
    # Read the text message from the txt file
    with open(txt_path, 'r') as file:
        message = file.read().strip()

    message += END_MARKER
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    try:
        # Open the WAV file
        with wave.open(wav_path, 'rb') as wav:
            params = wav.getparams()
            print("WAV Params:", params)  # Debugging output
            frames = wav.readframes(params.nframes)

            # Check if the WAV file has a compatible format (16-bit PCM)
            if params.sampwidth != 2:  # sampwidth 2 means 16-bit PCM audio
                raise ValueError("Unsupported sample width. This program works only with 16-bit PCM WAV files.")

            audio_data = np.frombuffer(frames, dtype=np.int16)

    except Exception as e:
        messagebox.showerror("Error", f"Error reading WAV file: {e}")
        print(f"Error reading WAV file: {e}")  # Debugging output
        return

    if len(binary_message) > len(audio_data):
        raise ValueError("Message too large to hide in this audio file.")

    # Embed the message in the LSB
    binary_message_index = 0
    for i in range(len(audio_data)):
        if binary_message_index < len(binary_message):
            # Modify the least significant bit
            audio_data[i] = (audio_data[i] & 0xFFFE) | int(binary_message[binary_message_index])
            binary_message_index += 1

    try:
        # Write the modified audio data back to a new WAV file
        with wave.open(output_path, 'wb') as output_wav:
            output_wav.setparams(params)
            output_wav.writeframes(audio_data.tobytes())
        messagebox.showinfo("Success", f"Message hidden successfully in {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error writing WAV file: {e}")
        print(f"Error writing WAV file: {e}")  # Debugging output
        return


def lsb_extract_audio(wav_path):
    """Extract the hidden message from a WAV file using LSB."""
    try:
        with wave.open(wav_path, 'rb') as wav:
            params = wav.getparams()
            print("WAV Params (Extract):", params)  # Debugging output
            frames = wav.readframes(params.nframes)
            audio_data = np.frombuffer(frames, dtype=np.int16)

    except Exception as e:
        messagebox.showerror("Error", f"Error reading WAV file: {e}")
        print(f"Error reading WAV file: {e}")  # Debugging output
        return "Error reading file"

    binary_message = ""
    for sample in audio_data:
        binary_message += str(sample & 1)  # Extract the LSB

    hidden_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

    end_index = hidden_message.find(END_MARKER)
    if end_index != -1:
        return hidden_message[:end_index]
    return "No hidden message found!"


# GUI Application
class AudioSteganoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Steganography Tool")
        self.root.configure(bg="black")
        self.file_path = ""
        self.message_file_path = ""

        # Title
        self.title_label = tk.Label(root, text="Audio Steganography Tool", fg="#00FF00", bg="black",
                                    font=("Courier", 18, "bold"))
        self.title_label.pack(pady=10)

        # File Section
        self.file_frame = tk.Frame(root, bg="black")
        self.file_frame.pack(pady=5)

        self.file_label = tk.Label(self.file_frame, text="Audio File (WAV):", fg="#00FF00", bg="black")
        self.file_label.grid(row=0, column=0)
        self.file_entry = tk.Entry(self.file_frame, width=40)
        self.file_entry.grid(row=0, column=1)
        self.file_button = tk.Button(self.file_frame, text="Browse", command=self.load_audio_file, fg="black",
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

    def load_audio_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if self.file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, self.file_path)

    def load_message_file(self):
        self.message_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.message_file_path:
            messagebox.showinfo("File Selected", f"Message File: {self.message_file_path}")

    def encrypt(self):
        if not self.file_path:
            messagebox.showerror("Error", "No audio file selected!")
            return
        if not self.message_file_path:
            messagebox.showerror("Error", "No message file selected!")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV", "*.wav")])
        try:
            lsb_hide_audio(self.file_path, self.message_file_path, output_path)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt(self):
        if not self.file_path:
            messagebox.showerror("Error", "No audio file selected!")
            return

        hidden_message = lsb_extract_audio(self.file_path)

        self.result_label.config(text=f"Hidden Message: {hidden_message}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSteganoApp(root)
    root.mainloop()
