import os
from pathlib import Path

import pytesseract
from PIL import Image
from pypdf import PdfReader


tesseract_cmd = os.getenv("TESSERACT_CMD")

if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


def extract_text_from_image(file_path: str) -> str:
    with Image.open(file_path) as image:
        image = image.convert("RGB")
        return pytesseract.image_to_string(
            image,
            config="--psm 6",
        )


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    if len(reader.pages) > 10:
        raise ValueError("PDF contains too many pages.")

    extracted_pages = []

    for page in reader.pages:
        extracted_pages.append(page.extract_text() or "")

    return "\n".join(extracted_pages)


def extract_receipt_text(file_path: str, mime_type: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("Receipt file not found.")

    if mime_type == "application/pdf":
        text = extract_text_from_pdf(file_path)

        # Scanned PDFs may contain no embedded text.
        # OCR fallback for scanned PDFs is a later enhancement.
        if not text.strip():
            raise ValueError(
                "No readable PDF text found. Scanned PDF OCR is not yet supported."
            )

        return text

    if mime_type in {"image/jpeg", "image/png"}:
        return extract_text_from_image(file_path)

    raise ValueError("Unsupported receipt type.")