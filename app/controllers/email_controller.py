from fastapi import APIRouter, HTTPException
from app.models.email_payload import EmailPayload
from app.services.email_service import EmailService

router = APIRouter(prefix="/email", tags=["Email"])

@router.post("/send-poc")
def send_email(payload: EmailPayload):
    try:
        return EmailService.send_email(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))