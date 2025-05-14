from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate
from app.auth import hash_password, create_token, decode_token
from app.email_service import send_verification_email
from app.security import decrypt_id
from app.database import db
from bson import ObjectId

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate):
    existing = db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email exists")
    db.users.insert_one({
        "email": user.email,
        "password": hash_password(user.password),
        "role": "client",
        "verified": False
    })
    token = create_token({"sub": user.email})
    send_verification_email(user.email, token)
    return {"message": "Check your email for verification link"}

@router.get("/verify-email")
def verify_email(token: str):
    data = decode_token(token)
    db.users.update_one({"email": data["sub"]}, {"$set": {"verified": True}})
    return {"message": "Email verified"}

@router.post("/login")
def login(email: str, password: str):
    user = db.users.find_one({"email": email, "role": "client"})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid")
    if not user["verified"]:
        raise HTTPException(status_code=401, detail="Verify email first")
    return {"token": create_token({"sub": email, "role": "client"})}

@router.get("/download-file/{enc_id}")
def download_file(enc_id: str, token: str):
    payload = decode_token(token)
    if payload["role"] != "client":
        raise HTTPException(status_code=403, detail="Unauthorized")
    file_id = decrypt_id(enc_id)
    file = db.files.find_one({"_id": ObjectId(file_id)})
    if not file:
        raise HTTPException(status_code=404, detail="Not Found")
    return {
        "download-link": f"/uploads/{file['filename']}",
        "message": "success"
    }

@router.get("/list")
def list_files():
    files = list(db.files.find({}, {"filename": 1}))
    return {"files": files}
