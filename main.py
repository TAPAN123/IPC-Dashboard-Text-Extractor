# main.py

import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, Text
from config import EXCEL_FILE
from utils import preview_and_crop, extract_text_from_cropped, save_to_excel
import os

class IPCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📸 IPC Alert Extractor")
        self.root.geometry("750x550")

        self.selected_image_paths = []
        self.cropped_images = {}

        tk.Label(root, text="Select IPC Images", font=("Arial", 14)).pack(pady=10)

        self.select_btn = tk.Button(root, text="Choose Images", command=self.select_images, font=("Arial", 12))
        self.select_btn.pack(pady=5)

        frame = tk.Frame(root)
        frame.pack(pady=10)
        self.image_list = Listbox(frame, width=80, height=8)
        self.image_list.pack(side="left", fill="y")
        scrollbar = Scrollbar(frame, orient="vertical")
        scrollbar.config(command=self.image_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.image_list.config(yscrollcommand=scrollbar.set)

        self.crop_btn = tk.Button(root, text="Crop Image Only", command=self.crop_images, font=("Arial", 12))
        self.crop_btn.pack(pady=5)

        self.ocr_btn = tk.Button(root, text="Run OCR & Save", command=self.ocr_and_save, font=("Arial", 12))
        self.ocr_btn.pack(pady=5)

        output_frame = tk.Frame(root)
        output_frame.pack(pady=10)
        self.output_text = Text(output_frame, width=90, height=10, wrap="word", font=("Arial", 10))
        self.output_text.pack(side="left", fill="y")
        out_scroll = Scrollbar(output_frame, orient="vertical")
        out_scroll.config(command=self.output_text.yview)
        out_scroll.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=out_scroll.set)

        self.result_label = tk.Label(root, text="", wraplength=700, font=("Arial", 11), fg="green")
        self.result_label.pack(pady=10)

    def select_images(self):
        files = filedialog.askopenfilenames(
            title="Select IPC Images",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")]
        )
        if files:
            self.selected_image_paths = list(files)
            self.image_list.delete(0, tk.END)
            for file in files:
                self.image_list.insert(tk.END, file)

    def crop_images(self):
        if not self.selected_image_paths:
            messagebox.showwarning("No Images", "Please select images first.")
            return

        self.cropped_images.clear()
        for img_path in self.selected_image_paths:
            cropped = preview_and_crop(img_path)
            self.cropped_images[img_path] = cropped

        messagebox.showinfo("Done", f"{len(self.cropped_images)} image(s) cropped.")

    def ocr_and_save(self):
        if not self.cropped_images:
            messagebox.showwarning("No Cropped Images", "Please crop images first.")
            return

        results = []
        self.output_text.delete("1.0", tk.END)

        for img_path, cropped_img in self.cropped_images.items():
            text = extract_text_from_cropped(cropped_img)
            name = os.path.basename(img_path)
            results.append((name, text))
            self.output_text.insert(tk.END, f"{name}:\n{text}\n\n")

        save_to_excel(results, EXCEL_FILE)
        self.result_label.config(text=f"✅ {len(results)} image(s) processed & saved.")
        messagebox.showinfo("Success", f"{len(results)} image(s) processed and saved.")

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = IPCApp(root)
    root.mainloop()
