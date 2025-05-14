from fastapi import APIRouter, UploadFile, Depends, HTTPException
from app.auth import verify_password, create_token
from app.file_handler import save_file
from app.database import db
from app.security import encrypt_id
import os

router = APIRouter()

@router.post("/login")
def ops_login(email: str, password: str):
    user = db.users.find_one({"email": email, "role": "ops"})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": create_token({"sub": email, "role": "ops"})}

@router.post("/upload")
async def upload_file(file: UploadFile, token: str):
    # Validate extension
    if not file.filename.endswith((".pptx", ".docx", ".xlsx")):
        raise HTTPException(status_code=400, detail="Invalid file type")
    from app.auth import decode_token
    payload = decode_token(token)
    if payload["role"] != "ops":
        raise HTTPException(status_code=403, detail="Unauthorized")

    filename = await save_file(file)
    file_id = db.files.insert_one({"filename": filename, "uploader_email": payload["sub"]}).inserted_id
    return {"message": "uploaded", "download_id": encrypt_id(str(file_id))}
