from transformers import DonutProcessor, VisionEncoderDecoderModel
from pdf2image import convert_from_path
from PIL import Image
import torch

# Load model and processor
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Convert PDF to image
pdf_path = "China_Janes_Fighting_Ships_2023-2024.pdf"  # your uploaded file
images = convert_from_path(pdf_path, dpi=200, first_page=1, last_page=1)  # Only page 1 for testing

for img in images:
    # Preprocess image
    pixel_values = processor(img, return_tensors="pt").pixel_values.to(device)

    # Use the default task for this model: visual question answering
    task_prompt = "<s_docvqa><s_question>what is shown in this document?</s_question><s_answer>"

    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
    outputs = model.generate(
        pixel_values,
        decoder_input_ids=decoder_input_ids.to(device),
        max_length=512,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id
    )

    result = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    print("\n📄 Extracted Content:")
    print(result)
