import os
import pytesseract
from PIL import Image, ImageOps, UnidentifiedImageError
from fpdf import FPDF
from docx import Document
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
import datetime
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
POPDIR = r'D:/poppler/bin'  # Set this to your poppler bin path

pytesseract.pytesseract.tesseract_cmd = r'D:/tesseract/tesseract.exe'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

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

def extract_text_from_image(image_path, lang='eng'):
    img = preprocess_image(image_path)
    return pytesseract.image_to_string(img, lang=lang)

def extract_text_from_pdf(pdf_path, lang='eng'):
    images = convert_from_path(pdf_path, poppler_path=POPDIR)
    text = ""
    for img in images:
        img = img.convert("L")
        img = ImageOps.invert(img)
        img = img.resize((img.width * 2, img.height * 2))
        text += pytesseract.image_to_string(img, lang=lang) + "\n"
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        output_format = request.form['format']
        lang = request.form.get('lang', 'eng')

        if file:
            filename = secure_filename(file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(input_path)

            base_name = os.path.splitext(filename)[0]
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"{base_name}_{timestamp}.{output_format}"
            output_path = os.path.join(OUTPUT_FOLDER, output_name)

            try:
                if filename.lower().endswith('.pdf'):
                    text = extract_text_from_pdf(input_path, lang)
                else:
                    text = extract_text_from_image(input_path, lang)

                text = clean_text(text)

                if output_format == 'txt':
                    save_to_txt(text, output_path)
                elif output_format == 'pdf':
                    save_to_pdf(text, output_path)
                elif output_format == 'docx':
                    save_to_docx(text, output_path)
                else:
                    return "Unsupported output format", 400

                return send_file(output_path, as_attachment=True)

            except UnidentifiedImageError:
                return "The uploaded file is not a supported image or valid PDF.", 400
            except Exception as e:
                return f"Error: {str(e)}", 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
