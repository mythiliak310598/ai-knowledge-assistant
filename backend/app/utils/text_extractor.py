from docx import Document as DocumentReader
from pathlib import Path
from io import BytesIO
from PIL import Image
import pymupdf
import pytesseract 


def extract_text(file_path: str) -> str:
    extension = Path(file_path).suffix.lower()
    pdf_document = None
    if extension == ".pdf":
        try:
            pdf_document = pymupdf.open(file_path)
            orderedText = ""

            for page in pdf_document:
                page_data = page.get_text("dict")
                blocks = page_data["blocks"]
                blocks = sorted(blocks, key = lambda block:block["bbox"][1])

                for block in blocks:
                    if block["type"] == 0:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                line_text = span["text"]
                                if line_text.strip():
                                    orderedText += line_text.strip() + "\n"
                    elif block["type"] == 1:
                        image_bytes = block["image"]
                        image = Image.open(BytesIO(image_bytes))
                        ocr_text = pytesseract.image_to_string(image)
                        orderedText += ocr_text.strip() + "\n"

            return orderedText
        finally:
            if pdf_document is not None:
                pdf_document.close()

    elif extension == ".docx":
        # Open the DOCX document
        document = DocumentReader(file_path)
        text = ""

        # XML namespaces used by Microsoft Word
        # Namespace for WordprocessingML
        W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        # Namespace for DrawingML
        A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
        # Namespace for Office relationships
        R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

        # Go through the document body in its original order

        for element in document.element.body:
            # Check whether this element is a Word paragraph
            if element.tag == f"{{{W_NS}}}p":
                # Process everything inside this paragraph
                for child in element.iter():
                    # 1. Check whether the child is normal text
                    if child.tag == f"{{{W_NS}}}t":
                        # Get the text stored inside <w:t>
                        paragraph_text = child.text

                        # Add it to our final document text
                        if paragraph_text:
                            text += paragraph_text
                    # 2. Check whether the child is an image
                    elif child.tag == f"{{{A_NS}}}blip":

                        # <a:blip> contains the relationship ID
                        #
                        # Example:
                        # <a:blip r:embed="rId5"/>
                        #
                        # rId5 tells us which image belongs here.

                        relationship_id = child.get(
                            f"{{{R_NS}}}embed"
                        )

                        # Make sure an image relationship exists
                        if relationship_id:

                            # Find the actual image part using rId
                            image_part = document.part.related_parts[
                                relationship_id
                            ]

                            # Get the image as raw bytes
                            image_bytes = image_part.blob

                            # Convert bytes into a PIL Image
                            image = Image.open(
                                BytesIO(image_bytes)
                            )

                            # Send the image to Tesseract
                            ocr_text = pytesseract.image_to_string(
                                image
                            )

                            # Add OCR text immediately at this position
                            #
                            # This is the important part:
                            #
                            # Text → Image OCR → Text → Image OCR
                            #
                            # instead of:
                            #
                            # All Text → All Images
                            if ocr_text.strip():
                                text += "\n" + ocr_text + "\n"

                # Add a newline after each paragraph
                text += "\n"
            elif element.tag == f"{{{W_NS}}}tbl":
                for row in element.findall(f"{{{W_NS}}}tr"):
                    cells = row.findall(f"{{{W_NS}}}tc")
                    row_cells=[]

                    for cell in cells:
                        cell_text_parts = []
                        for text_element in cell.iter(f"{{{W_NS}}}t"):
                            if text_element.text:
                                cell_text_parts.append(text_element.text)

                        cell_text = " ".join(cell_text_parts).strip()

                        if cell_text:
                            row_cells.append(cell_text)
                    row_text = " | ".join(row_cells)
                    if row_text:
                        text += row_text + "\n"
        return text
    else:
        raise ValueError("Unsupported File Type")