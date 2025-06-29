import smtplib
from email.mime.text import MIMEText
import requests

# --- Email config ---
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your.email@gmail.com'  # change this
SMTP_PASSWORD = 'your-app-password'     # change this
FROM_EMAIL = SMTP_USERNAME

def send_email(to_email, subject, message):
    msg = MIMEText(message)
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            smtp.send_message(msg)
        print(f"[Notifier] Email sent to {to_email}")
    except Exception as e:
        print(f"[Notifier] Failed to send email: {e}")

# --- Webhook ---
def send_webhook(url, payload):
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"[Notifier] Webhook sent to {url}")
    except Exception as e:
        print(f"[Notifier] Failed to send webhook: {e}")
