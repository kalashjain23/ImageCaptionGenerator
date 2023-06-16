from model import get_captions
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox


class CaptionGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Image Caption Generator")
        master.configure(background='white')

        self.image_path = None
        self.captions = []

        self.image_label = tk.Label(master, bg='white')
        self.select_button = tk.Button(master, text="Select Image", command=self.select_image)
        self.limits_label = tk.Label(master, text="Number of Captions: ", bg='white')
        self.limits_entry = tk.Entry(master, width=12)
        self.generate_button = tk.Button(master, text="Generate Captions",
                                         command=self.generate_captions,
                                         height=2, bg='lightblue')

        self.image_label.pack(pady=5)
        self.select_button.pack(pady=5)
        self.limits_label.pack(side=tk.LEFT, padx=15, pady=10)
        self.limits_entry.pack(side=tk.LEFT,pady=10)
        self.generate_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def select_image(self): 
        self.image_path = filedialog.askopenfilename(filetypes=[('All files', "*.*")])
        try:
            if self.image_path:
                image = Image.open(self.image_path).resize((450, 450))
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo
                self.master.geometry('550x600')
            else:
                messagebox.showerror("Error", "No image selected")
        except:
            messagebox.showerror("Error", "Invalid image")

    def generate_captions(self):
        try:
            if self.image_path:
                self.captions = get_captions(self.image_path, int(self.limits_entry.get()))
                self.show_captions()
            else:
                messagebox.showerror("Error", "No captions generated")
        except:
            messagebox.showerror("Error", "Invalid number of captions")

    def show_captions(self):
        if self.captions:
            self.caption_window = tk.Toplevel(self.master)
            self.caption_window.title("Generated Captions")
            self.caption_window.geometry('500x300')
            self.caption_window.protocol("WM_DELETE_WINDOW", self.clear_captions)

            caption_frame = tk.Frame(self.caption_window)
            caption_frame.pack(fill=tk.BOTH, expand=True)

            self.caption_text = tk.Text(caption_frame, height=10, width=50)
            self.caption_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            for i, caption in enumerate(self.captions):
                self.caption_text.insert(tk.END, f"{i+1}) {caption}\n")
        else:
            messagebox.showerror("Error", "No captions generated.")

    def clear_captions(self):
        self.captions.clear()
        self.caption_text.delete('1.0', tk.END)
        self.caption_window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('550x150')
    root.resizable(False, False)
    app = CaptionGenerator(root)
    root.mainloop()
