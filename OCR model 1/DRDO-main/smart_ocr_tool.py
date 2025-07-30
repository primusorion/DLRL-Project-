import os
import pytesseract
from PIL import Image, ImageOps
from fpdf import FPDF
from docx import Document
from tkinter import Tk, filedialog, messagebox, simpledialog
import datetime
import re

# Set your Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'

def preprocess_image(image_path):
    img = Image.open(image_path).convert("L")
    img = ImageOps.invert(img)
    img = img.resize((img.width * 2, img.height * 2))
    return img

def clean_text(text):
    text = text.strip()
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text

def save_to_txt(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def save_to_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)

def save_to_docx(text, filename):
    doc = Document()
    for line in text.split('\n'):
        doc.add_paragraph(line)
    doc.save(filename)

def process_image(image_path, output_format, lang='eng'):
    try:
        img = preprocess_image(image_path)
        raw_text = pytesseract.image_to_string(img, lang=lang)
        text = clean_text(raw_text)

        base = os.path.splitext(os.path.basename(image_path))[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        if output_format == 'txt':
            filename = f"{base}_{timestamp}.txt"
            save_to_txt(text, filename)
        elif output_format == 'pdf':
            filename = f"{base}_{timestamp}.pdf"
            save_to_pdf(text, filename)
        elif output_format == 'docx':
            filename = f"{base}_{timestamp}.docx"
            save_to_docx(text, filename)
        else:
            raise ValueError("Invalid output format selected.")

        print(f"[✓] Processed: {image_path}")
        print(f"    └─ {filename}")
    except Exception as e:
        print(f"[X] Failed: {image_path} — {e}")

def process_folder(folder_path, output_format, lang='eng'):
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            full_path = os.path.join(folder_path, file)
            process_image(full_path, output_format, lang)

def launch_gui():
    root = Tk()
    root.withdraw()

    choice = messagebox.askyesno("OCR Tool", "Do you want to scan a folder? (Yes = Folder, No = Single Image)")

    lang_choice = simpledialog.askstring("Language", "Enter Tesseract language code (e.g. 'eng', 'hin', 'eng+hin'):")
    lang = lang_choice.strip() if lang_choice else 'eng'

    # Ask user for output format
    output_format = None
    while output_format not in ['txt', 'pdf', 'docx']:
        output_format = simpledialog.askstring(
            "Output Format", 
            "Choose output format:\nType 'txt' for Text file\nType 'pdf' for PDF\nType 'docx' for Word document"
        )
        if output_format:
            output_format = output_format.strip().lower()
        else:
            messagebox.showerror("Error", "No output format selected. Exiting.")
            root.quit()
            return

    if choice:
        folder = filedialog.askdirectory(title="Select Folder of Images")
        if folder:
            process_folder(folder, output_format, lang)
    else:
        image_path = filedialog.askopenfilename(
            title="Select Image", 
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")]
        )
        if image_path:
            process_image(image_path, output_format, lang)

    messagebox.showinfo("Done", "OCR processing complete!")
    root.quit()

if __name__ == "__main__":
    launch_gui()
