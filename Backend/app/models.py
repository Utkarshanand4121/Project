from pydantic import BaseModel, EmailStr
from typing import List, Optional

class User(BaseModel):
    email: EmailStr
    password: str
    role: str  # "client" or "ops"
    verified: bool = False

class FileMeta(BaseModel):
    filename: str
    uploader_email: str
    download_id: str
