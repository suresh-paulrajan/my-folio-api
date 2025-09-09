from app.utils.smtp_util import SMTPUtil
from app.models.email_payload import EmailPayload

class EmailService:
    @staticmethod
    def send_email(payload: EmailPayload):
        SMTPUtil.send_email(
            subject=payload.subject,
            body=payload.body,
            to=payload.to,
            cc=payload.cc
        )
        return {"status": "success", "message": "Email sent successfully"}