from PIL import Image, ImageOps
import pytesseract
import os
import datetime
import re

# Path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'

def preprocess_image(image_path):
    """Preprocess the image: convert to grayscale and upscale"""
    img = Image.open(image_path).convert("L")  # Grayscale
    img = ImageOps.invert(img)  # Optional: helpful for light text on dark background
    img = img.resize((img.width * 2, img.height * 2))  # Upscale to improve OCR
    return img

def clean_text(text):
    """Clean the OCR result for better readability"""
    text = text.strip()
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Remove excessive empty lines
    return text

def image_to_text(image_path):
    if not os.path.exists(image_path):
        print(f"[-] Error: File '{image_path}' not found.")
        return

    try:
        img = preprocess_image(image_path)
        text = pytesseract.image_to_string(img)
        text = clean_text(text)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"ocr_output_{timestamp}.txt"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"[+] Text successfully extracted to '{output_file}'")
    except Exception as e:
        print(f"[-] OCR failed: {e}")

# Set your image name here
image_to_text("s2.png")
