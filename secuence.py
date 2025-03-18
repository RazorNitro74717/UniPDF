import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import datetime as dat
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
import fitz

def PDFConv(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    img_path = f"{os.path.splitext(pdf_path)[0]}.png"
    image.save(img_path)
    return img_path

def Convertion():
    try:
        root = tk.Tk()
        root.withdraw()

        files = filedialog.askopenfilenames(title= "Select PDF files (Maximum = 4 files)", filetypes= [("Files", "*")], multiple = True)
        files = files[:4]

        if not files:
            messagebox.show("No files selected!")
            return
        d = dat.datetime.now()
        tDate = f"{d.month}-{d.year}"
        output_filename = f"print-{tDate}.pdf"
        can = canvas.Canvas(output_filename, pagesize= A4)

        width, height = A4
        r_width = width/2
        r_height = height/2

        pos = [(0, r_height),
               (r_width, r_height),
               (0,0),
               (r_width, 0)]
        
        for i, file in enumerate(files):
            ext = os.path.splitext(file)[1].lower()
            if ext == ".pdf":
                img_path = PDFConv(file)
            elif ext in [".jpg", ".jpeg", ".png"]:
                img_path = file
                
            # img.save(img_path, "PNG")

            can.drawImage(img_path, *pos[i], r_width, r_height)

        can.showPage()
        can.save()

        messagebox.showinfo(message = f"PDF Saved at{output_filename}")

    except (ValueError, TypeError) as e: messagebox.showerror (message =  e)
    finally: pass



Convertion()