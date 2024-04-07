import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from stegano import lsb
import threading  

class SteganographyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Steganography Using LSB")
        self.geometry("900x600")
        self.current_image_path = None
        self.decoded_text = tk.StringVar()
        
        self.title_label = tk.Label(self, text="Image Steganography Using LSB", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=20)

        self.select_image_button = tk.Button(self, text="Select Image", command=self.select_image, font=("Helvetica", 14))
        self.select_image_button.pack()

        self.image_path_label = tk.Label(self, text="", font=("Helvetica",9))
        self.image_path_label.pack(pady=10)

        self.encode_button = tk.Button(self, text="Encode", command=self.open_encode_window, font=("Helvetica", 14))
        self.encode_button.pack(pady=10)

        self.decode_button = tk.Button(self, text="Decode", command=self.decode_image, font=("Helvetica", 14))
        self.decode_button.pack(pady=10)

        self.close_button = tk.Button(self, text="Close", command=self.quit, font=("Helvetica", 14))
        self.close_button.pack(side=tk.BOTTOM, pady=20)

    def select_image(self):
        self.current_image_path = filedialog.askopenfilename(title="Select Image File")
        if self.current_image_path:
            self.image_path_label.config(text="SELECTED IMAGE BY THE USER : \n" + self.current_image_path)

    def open_encode_window(self):
        if not self.current_image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return
        
        self.encode_window = EncodeWindow(self, self.current_image_path)
        self.encode_window.grab_set()

    def decode_image(self):
        if not self.current_image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return
        
        self.decoded_text.set("Decoding...")
        self.decode_thread = threading.Thread(target=self.decode_image_thread)
        self.decode_thread.start()

    def decode_image_thread(self):
        try:
            secret = lsb.reveal(self.current_image_path)
            self.decoded_text.set(secret)
            self.show_decode_window()
        except Exception as e:
            messagebox.showerror("Error", "An error occurred during decoding: {}".format(str(e)))

    def show_decode_window(self):
        self.decode_window = DecodeWindow(self, self.decoded_text, self.current_image_path)
        self.decode_window.grab_set()

class EncodeWindow(tk.Toplevel):
    def __init__(self, master, image_path):
        super().__init__(master)
        self.title("Encode Text Display")
        self.geometry("900x600")
        self.master = master
        self.image_path = image_path
        
        self.title_label = tk.Label(self, text="Encode Text Display", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=20)

        self.image_label = tk.Label(self, text="Original Image")
        self.image_label.pack()

        self.load_and_display_image()

        self.text_label = tk.Label(self, text="Enter Text to Hide:", font=("Helvetica", 14))
        self.text_label.pack(pady=10)

        self.text_entry = tk.Text(self, height=5, width=60)
        self.text_entry.pack(pady=10)

        self.encode_button = tk.Button(self, text="Encode Text", command=self.encode_text, font=("Helvetica", 14))
        self.encode_button.pack(pady=10)

        self.close_button = tk.Button(self, text="Close", command=self.destroy, font=("Helvetica", 14))
        self.close_button.pack(side=tk.BOTTOM, pady=20)

    def load_and_display_image(self):
        image = Image.open(self.image_path)
        image = image.resize((400, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def encode_text(self):
        text_to_hide = self.text_entry.get("1.0", tk.END)
        try:
            secret = lsb.hide(self.image_path, text_to_hide)
            encoded_image_path = self.image_path.replace('.', '_encoded.')
            secret.save(encoded_image_path)  # Save the encoded image
            messagebox.showinfo("Success", "Text encoded successfully!")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred during encoding: {}".format(str(e)))

class DecodeWindow(tk.Toplevel):
    def __init__(self, master, decoded_text, image_path):
        super().__init__(master)
        self.title("Decoded Text Display")
        self.geometry("900x600")
        self.master = master
        self.decoded_text = decoded_text
        self.image_path = image_path
        
        self.title_label = tk.Label(self, text="Decoded Text Display", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=20)

        self.image_label = tk.Label(self, text="Original Image")
        self.image_label.pack()

        self.load_and_display_image()

        self.text_label = tk.Label(self, text="Extracted Text:", font=("Helvetica", 14))
        self.text_label.pack(pady=10)

        self.text_display = tk.Text(self, height=5, width=60)
        self.text_display.pack(pady=10)
        self.text_display.insert(tk.END, decoded_text.get())

        self.copy_button = tk.Button(self, text="Copy Text", command=self.copy_text, font=("Helvetica", 14))
        self.copy_button.pack(pady=10)

        self.close_button = tk.Button(self, text="Close", command=self.destroy, font=("Helvetica", 14))
        self.close_button.pack(side=tk.BOTTOM, pady=20)

    def load_and_display_image(self):
        image = Image.open(self.image_path)
        image = image.resize((400, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def copy_text(self):
        text_to_copy = self.text_display.get("1.0", tk.END)
        self.clipboard_clear()
        self.clipboard_append(text_to_copy)
        self.update()
        messagebox.showinfo("Success", "Text copied to clipboard!")

if __name__ == "__main__":
    app = SteganographyApp()
    app.mainloop()


