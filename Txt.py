import tkinter as tk
from tkinter import filedialog, messagebox
import re

# Utility Functions for Steganography

def comment_insert(html_content, secret_message):
    """Insert the message into an HTML comment."""
    # Ensure no duplicate comments
    return html_content + f"\n<!-- {secret_message} -->"

#khaled fadel comment
def comment_extract(html_content):
    """Extract hidden message from an HTML comment."""
    comments = re.findall(r'<!--(.*?)-->', html_content, re.DOTALL)
    if comments:
        return "\n".join([comment.strip() for comment in comments])
    return "No hidden message found in comments!"


def invisible_tag_insert(html_content, secret_message):
    """Hide the message in an invisible HTML span."""
    hidden_tag = f'<div style="display:none;">{secret_message}</div>'
    # Ensure it gets added before the closing body tag
    if "</body>" in html_content:
        return html_content.replace("</body>", f"{hidden_tag}\n</body>")
    else:
        return html_content + f"\n{hidden_tag}"


def invisible_tag_extract(html_content):
    """Extract hidden message from an invisible HTML tag."""
    matches = re.findall(r'<div style="display:none;">(.*?)</div>', html_content, re.DOTALL)
    if matches:
        return "\n".join(matches)
    return "No hidden message found in invisible tags!"


# Main GUI Application
class HTMLSteganoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Stegano Tool")
        self.root.configure(bg="black")
        self.html_content = ""
        self.file_path = ""

        # Title
        self.title_label = tk.Label(root, text="HTML Steganography Tool", fg="#00FF00", bg="black", font=("Courier", 18, "bold"))
        self.title_label.pack(pady=10)

        # File Section
        self.file_frame = tk.Frame(root, bg="black")
        self.file_frame.pack(pady=5)

        self.file_label = tk.Label(self.file_frame, text="HTML File:", fg="#00FF00", bg="black")
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
        self.technique_var = tk.StringVar(value="COMMENT")

        self.comment_rb = tk.Radiobutton(root, text="HTML Comments", variable=self.technique_var, value="COMMENT", fg="#00FF00", bg="black")
        self.comment_rb.pack()
        self.invisible_rb = tk.Radiobutton(root, text="Invisible Tags", variable=self.technique_var, value="INVISIBLE", fg="#00FF00", bg="black")
        self.invisible_rb.pack()

        # Buttons
        self.encrypt_button = tk.Button(root, text="Hide Message", command=self.encrypt, fg="black", bg="#00FF00")
        self.encrypt_button.pack(pady=5)
        self.decrypt_button = tk.Button(root, text="Retrieve Message", command=self.decrypt, fg="black", bg="#00FF00")
        self.decrypt_button.pack(pady=5)

        # Result Section
        self.result_label = tk.Label(root, text="", fg="#00FF00", bg="black", font=("Courier", 12, "bold"))
        self.result_label.pack()

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
        if self.file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, self.file_path)
            with open(self.file_path, 'r') as file:
                self.html_content = file.read()

    def save_file(self, content):
        save_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        if save_path:
            with open(save_path, 'w') as file:
                file.write(content)
            messagebox.showinfo("Success", f"File saved at: {save_path}")

    def encrypt(self):
        if not self.html_content:
            messagebox.showerror("Error", "No HTML file loaded!")
            return
        secret_message = self.msg_entry.get("1.0", tk.END).strip()
        if not secret_message:
            messagebox.showerror("Error", "No secret message entered!")
            return

        technique = self.technique_var.get()
        if technique == "COMMENT":
            stego_html = comment_insert(self.html_content, secret_message)
        elif technique == "INVISIBLE":
            stego_html = invisible_tag_insert(self.html_content, secret_message)
        else:
            messagebox.showerror("Error", "Invalid technique selected!")
            return

        self.save_file(stego_html)
        self.result_label.config(text="Message hidden successfully!")

    def decrypt(self):
        if not self.html_content:
            messagebox.showerror("Error", "No HTML file loaded!")
            return

        technique = self.technique_var.get()
        if technique == "COMMENT":
            secret_message = comment_extract(self.html_content)
        elif technique == "INVISIBLE":
            secret_message = invisible_tag_extract(self.html_content)
        else:
            messagebox.showerror("Error", "Invalid technique selected!")
            return

        self.result_label.config(text=f"Hidden Message: {secret_message}")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HTMLSteganoApp(root)
    root.mainloop()
