import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

root = tk.Tk()
root.title("PDF Page Rotator")
root.geometry("500x450")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        load_pages(file_path)

def load_pages(file_path):
    listbox.delete(0, tk.END)
    pdf_reader = PdfReader(file_path)
    for page_num in range(len(pdf_reader.pages)):
        listbox.insert(tk.END, f"Page {page_num + 1}")

    global selected_pdf
    selected_pdf = file_path

listbox = tk.Listbox(root, selectmode='extended', width=50, height=15, exportselection=False)
listbox.pack(side='left', fill='y', pady=20)

# Create a scrollbar and configure it
scrollbar = tk.Scrollbar(root, orient='vertical')
scrollbar.pack(side='right', fill='y')
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

open_file_button = tk.Button(root, text="Open PDF", command=open_file)
open_file_button.pack(pady=10)

def rotate_pages():
    try:
        rotation_angle = int(rotation_angle_entry.get())
        if rotation_angle not in [90, 180, 270, -90]:
            raise ValueError("Invalid rotation angle")
    except ValueError as e:
        messagebox.showerror("Error", "Please enter a valid rotation angle (90, 180, 270, -90)")
        return

    pdf_reader = PdfReader(selected_pdf)
    pdf_writer = PdfWriter()

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        if page_num in listbox.curselection():
            page.rotate(rotation_angle)  # Rotate by the specified angle
        pdf_writer.add_page(page)

    output_filename = os.path.splitext(selected_pdf)[0] + "_rotated.pdf"
    with open(output_filename, "wb") as out:
        pdf_writer.write(out)

    messagebox.showinfo("Done", f"Pages rotated! Saved as {output_filename}")

# Instruction label
instruction_label = tk.Label(root, text="Select pages on the left.")
instruction_label.pack(pady=(10, 0))

tk.Label(root, text="Rotation Angle:").pack(pady=(20, 0))
rotation_angle_entry = tk.Entry(root)
rotation_angle_entry.pack()
rotation_angle_entry.insert(0, "90")  # Default value

rotate_button = tk.Button(root, text="Rotate Selected Pages", command=rotate_pages)
rotate_button.pack(pady=10)

root.mainloop()
