# 🧠 OCR Project: Multi-Model Optical Character Recognition Pipeline

This project implements a robust three-stage OCR pipeline that evolves from traditional text extraction to an intelligent hybrid system using deep learning. It’s designed for structured document processing and is ideal for scanned PDFs, images, and forms.

All models run within a **Python virtual environment** for isolation and reproducibility.

## 📌 Models Overview

### ✅ Model 1: Tesseract OCR CLI Tool
A simple command-line tool using `pytesseract` for text extraction.

- Extracts plain text from images or PDFs
- Lightweight and easy to run

### ✅ Model 2: Tesseract Integrated with Flask Web App
A user-friendly web interface built with Flask that uses Tesseract OCR.

- Upload PDF or image files
- Web-based interaction
- Real-time OCR results on browser

### ✅ Model 3: Hybrid TrOCR + Tesseract System
A high-performance OCR system that combines Microsoft's TrOCR (transformers) with Tesseract for layout and accuracy.

- Transformer-based deep learning OCR
- Hybrid inference with fallback/combination strategy
- Best suited for scanned documents, handwritten text, or low-quality images

## 🧰 Environment Setup (For All Models)

### 🔄 Create Virtual Environment

```bash
python -m venv venv
# Activate the environment
source venv/bin/activate        # On macOS/Linux
venv\Scripts\activate           # On Windows
```

### 📦 Install Dependencies

Use this common `requirements.txt` (add other model-specific ones if needed):

```txt
flask
pytesseract
pdf2image
pillow
transformers
torch
```

Install via:

```bash
pip install -r requirements.txt
```

## ⚙️ Model-Specific Details

### 🚀 Model 1: Tesseract OCR CLI

#### 🛠️ Dependencies

- `pytesseract`
- `Pillow`
- Tesseract-OCR installed on system

#### 💻 Run

```bash
python model1_tesseract_ocr.py
```

#### 📥 Output

Extracted text is printed in the terminal or saved to a `.txt` file.

### 🌐 Model 2: Flask + Tesseract Web App

#### 🛠️ Dependencies

- `flask`
- `pytesseract`
- `pdf2image`
- `Pillow`
- `Werkzeug` (comes with Flask)

#### 💻 Run

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) to upload documents and view OCR results.

#### 📂 File Structure (Flask)

```
templates/
  └── index.html
static/
  └── style.css
uploads/
  └── (temporary user uploads)
```

### 🤖 Model 3: TrOCR + Tesseract Hybrid

#### 🛠️ Dependencies

- `transformers`
- `torch`
- `pytesseract`
- `pdf2image`
- `Pillow`

#### 💻 Run

```bash
python model3_hybrid_ocr.py
```

#### 📌 Features

- Uses `TrOCR` model from Hugging Face (`microsoft/trocr-base-stage1`)
- Performs multi-pass OCR for better accuracy
- Can process multiple page documents

## 🔧 Installing Tesseract OCR Engine

### 🪟 Windows

Download installer from:  
https://github.com/tesseract-ocr/tesseract

Add Tesseract path to environment variables, e.g.:

```txt
C:\Program Files\Tesseract-OCR\tesseract.exe
```

### 🐧 Linux (Ubuntu)

```bash
sudo apt update
sudo apt install tesseract-ocr
```

### 🍎 macOS

```bash
brew install tesseract
```

## 📁 Recommended Folder Structure

```
OCR-Project/
├── venv/
├── requirements.txt
├── model1_tesseract_ocr.py
├── model3_hybrid_ocr.py
├── app.py
├── templates/
├── static/
├── uploads/
└── README.md
```

## 📄 Sample Output

- **Model 1**: Outputs plain text
- **Model 2**: Web preview + downloadable text
- **Model 3**: Enhanced text output, may include layout-aware content

## ⚠️ Notes

- Always activate the virtual environment before running any model.
- Model 3 requires internet on first run (to download TrOCR).
- GPU usage (if available) can speed up TrOCR model inference.
- Make sure Tesseract is correctly installed and its path is set.

## 🤝 Contributions

Pull requests are welcome! Suggestions for layout-aware models, table extraction, or handwriting recognition modules are highly appreciated.
