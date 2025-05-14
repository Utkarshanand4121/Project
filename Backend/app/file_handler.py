import os
from fastapi import UploadFile

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

async def save_file(file: UploadFile):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    return file.filename
