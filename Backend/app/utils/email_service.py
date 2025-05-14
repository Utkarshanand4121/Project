import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_verification_email(email, token):
    link = f"http://localhost:8000/client/verify-email?token={token}"
    msg = MIMEText(f"Click to verify your email: {link}")
    msg["Subject"] = "Verify your Email"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = email

    with smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        server.send_message(msg)
