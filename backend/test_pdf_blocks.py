import pymupdf
from PIL import Image
from io import BytesIO
import pytesseract

file_path = "uploads/Episode-01 - Intro to Node JS.pdf"
pdf_document = pymupdf.open(file_path)
page = pdf_document[2]
page_data = page.get_text("dict")
blocks = page_data["blocks"]

# Sort blocks from top to bottom. bbox = (x0, y0, x1, y1)- bbox[1] gives us y0.
blocks = sorted(blocks, key = lambda block:block["bbox"][1])
orderedText = ""

for block in blocks:
    # TEXT BLOCK
    if block["type"] == 0:
        # A text block contains lines.
        for line in block["lines"]:
            # Each line contains spans.
            for span in line["spans"]:
                # Get actual text.
                span_text = span["text"]
                # Add it to final ordered text.
                if span_text.strip():
                    orderedText += span_text + "\n"
    # IMAGE BLOCK
    elif block["type"] == 1:
        # Get image bytes directly from the image block.
        image_bytes = block["image"]
        # Convert bytes into a PIL Image.
        image = Image.open(BytesIO(image_bytes))
        # OCR the image.
        ocr_text = pytesseract.image_to_string(image)
        # Add OCR text only if meaningful.
        orderedText += ocr_text + "\n"

print("Final Ordered Text")
print(orderedText)

