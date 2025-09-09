import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment-specific .env file
env = os.getenv("ENV", "local")
if env == "prod":
	load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env.prod"))
else:
	load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env.local"))

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

class SMTPUtil:
    @staticmethod
    def send_email(subject: str, body: str, to: list[str], cc: list[str] = []):
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = ", ".join(to)
        if cc:
            msg["Cc"] = ", ".join(cc)
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        try:
            # Direct SSL connection (no starttls needed)
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                server.login(SMTP_USER, SMTP_PASS)

                recipients = to + cc
                server.sendmail(SMTP_USER, recipients, msg.as_string())

        except smtplib.SMTPException as e:
            raise Exception(f"SMTP error: {str(e)}")