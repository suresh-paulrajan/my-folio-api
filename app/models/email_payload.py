from pydantic import BaseModel, EmailStr
from typing import List

class EmailPayload(BaseModel):
    subject: str
    body: str
    to: List[EmailStr]
    cc: List[EmailStr] = []