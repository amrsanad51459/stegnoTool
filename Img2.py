import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

END_MARKER = "#####END#####"  # Marker to detect the end of the hidden message


# LSB Steganography
def lsb_hide(image_path, message, output_path):
    """Hide the message using LSB in PNG images."""
    message += END_MARKER
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    img = Image.open(image_path)
    pixels = list(img.getdata())

    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Message too large to hide in this image.")

    data_index = 0
    new_pixels = []
    for pixel in pixels:
        if data_index < len(binary_message):
            new_pixel = list(pixel)
            for i in range(3):  # R, G, B channels
                if data_index < len(binary_message):
                    new_pixel[i] = (new_pixel[i] & ~1) | int(binary_message[data_index])
                    data_index += 1
            new_pixels.append(tuple(new_pixel))
        else:
            new_pixels.append(pixel)

    img.putdata(new_pixels)
    img.save(output_path, format="PNG")
    messagebox.showinfo("Success", f"Message hidden successfully in {output_path}")


def lsb_extract(image_path):
    """Extract the hidden message using LSB."""
    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_message = ""
    for pixel in pixels:
        for color in pixel[:3]:  # Extract R, G, B channels
            binary_message += str(color & 1)

    hidden_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))
    end_index = hidden_message.find(END_MARKER)
    if end_index != -1:
        return hidden_message[:end_index]
    return "No hidden message found!"


# Parity Steganography
def parity_hide(image_path, message, output_path):
    """Hide the message using parity bit manipulation in PNG images."""
    message += END_MARKER
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    img = Image.open(image_path)
    pixels = list(img.getdata())

    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Message too large to hide in this image.")

    data_index = 0
    new_pixels = []
    for pixel in pixels:
        if data_index < len(binary_message):
            new_pixel = list(pixel)
            for i in range(3):  # R, G, B channels
                if data_index < len(binary_message):
                    # Adjust parity: even or odd
                    current_bit = int(binary_message[data_index])
                    new_pixel[i] = (new_pixel[i] & ~1) | current_bit
                    data_index += 1
            new_pixels.append(tuple(new_pixel))
        else:
            new_pixels.append(pixel)

    img.putdata(new_pixels)
    img.save(output_path, format="PNG")
    messagebox.showinfo("Success", f"Message hidden successfully with parity in {output_path}")


def parity_extract(image_path):
    """Extract the hidden message using parity bit manipulation."""
    img = Image.open(image_path)
    pixels = list(img.getdata())

    # Initialize the binary message
    binary_message = ""

    # Loop through all the pixels and all color channels (R, G, B)
    for pixel in pixels:
        for color in pixel[:3]:  # Check only R, G, B channels
            binary_message += str(color & 1)  # Extract the LSB (parity bit) of each color channel

    # Convert the binary message to string
    hidden_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

    # Check for the end marker and return the message
    end_index = hidden_message.find(END_MARKER)
    if end_index != -1:
        return hidden_message[:end_index]
    return "No hidden message found!"


# GUI Application
class ImageSteganoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography Tool")
        self.root.configure(bg="black")
        self.file_path = ""

        # Title
        self.title_label = tk.Label(root, text="Image Steganography Tool", fg="#00FF00", bg="black",
                                    font=("Courier", 18, "bold"))
        self.title_label.pack(pady=10)

        # File Section
        self.file_frame = tk.Frame(root, bg="black")
        self.file_frame.pack(pady=5)

        self.file_label = tk.Label(self.file_frame, text="Image File:", fg="#00FF00", bg="black")
        self.file_label.grid(row=0, column=0)
        self.file_entry = tk.Entry(self.file_frame, width=40)
        self.file_entry.grid(row=0, column=1)
        self.file_button = tk.Button(self.file_frame, text="Browse", command=self.load_file, fg="black", bg="#00FF00")
        self.file_button.grid(row=0, column=2)

        # Message Section
        self.msg_label = tk.Label(root, text="Secret Message:", fg="#00FF00", bg="black")
        self.msg_label.pack()
        self.msg_entry = tk.Text(root, height=5, width=50)
        self.msg_entry.pack()

        # Technique Selection
        self.technique_label = tk.Label(root, text="Select Technique:", fg="#00FF00", bg="black")
        self.technique_label.pack(pady=5)
        self.technique_var = tk.StringVar(value="LSB")

        self.lsb_rb = tk.Radiobutton(root, text="LSB", variable=self.technique_var, value="LSB", fg="#00FF00",
                                     bg="black")
        self.lsb_rb.pack()
        self.parity_rb = tk.Radiobutton(root, text="Parity", variable=self.technique_var, value="PARITY", fg="#00FF00",
                                        bg="black")
        self.parity_rb.pack()

        # Buttons
        self.encrypt_button = tk.Button(root, text="Hide Message", command=self.encrypt, fg="black", bg="#00FF00")
        self.encrypt_button.pack(pady=5)
        self.decrypt_button = tk.Button(root, text="Retrieve Message", command=self.decrypt, fg="black", bg="#00FF00")
        self.decrypt_button.pack(pady=5)

        # Result Section
        self.result_label = tk.Label(root, text="", fg="#00FF00", bg="black", font=("Courier", 12, "bold"))
        self.result_label.pack()

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if self.file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, self.file_path)

    def encrypt(self):
        if not self.file_path:
            messagebox.showerror("Error", "No image file selected!")
            return
        message = self.msg_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "No secret message entered!")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if not output_path:
            return

        technique = self.technique_var.get()
        try:
            if technique == "LSB":
                lsb_hide(self.file_path, message, output_path)
            elif technique == "PARITY":
                parity_hide(self.file_path, message, output_path)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt(self):
        if not self.file_path:
            messagebox.showerror("Error", "No image file selected!")
            return

        technique = self.technique_var.get()
        try:
            if technique == "LSB":
                message = lsb_extract(self.file_path)
            elif technique == "PARITY":
                message = parity_extract(self.file_path)
            self.result_label.config(text=f"Hidden Message: {message}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSteganoApp(root)
    root.mainloop()
