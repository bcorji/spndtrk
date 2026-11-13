import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status


ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "application/pdf": ".pdf",
}

MAX_SIZE = int(os.getenv("MAX_RECEIPT_SIZE_MB", "10")) * 1024 * 1024

STORAGE_DIR = Path(
    os.getenv("RECEIPT_STORAGE_DIR", "storage/receipts")
).resolve()


def validate_signature(content: bytes, mime_type: str) -> bool:
    if mime_type == "image/jpeg":
        return content.startswith(b"\xff\xd8\xff")

    if mime_type == "image/png":
        return content.startswith(b"\x89PNG\r\n\x1a\n")

    if mime_type == "application/pdf":
        return content.startswith(b"%PDF-")

    return False


async def save_receipt(file: UploadFile) -> dict:
    mime_type = file.content_type or ""

    if mime_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only JPEG, PNG and PDF receipts are supported.",
        )

    content = await file.read(MAX_SIZE + 1)

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(content) > MAX_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Receipt exceeds the maximum allowed size.",
        )

    if not validate_signature(content, mime_type):
        raise HTTPException(
            status_code=400,
            detail="File content does not match its declared type.",
        )

    extension = ALLOWED_TYPES[mime_type]
    stored_filename = f"{uuid.uuid4().hex}{extension}"

    STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    destination = STORAGE_DIR / stored_filename
    destination.write_bytes(content)

    return {
        "original_filename": (file.filename or "receipt")[:255],
        "stored_filename": stored_filename,
        "mime_type": mime_type,
        "file_path": str(destination),
        "size": len(content),
    }