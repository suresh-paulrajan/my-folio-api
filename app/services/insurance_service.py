from sqlalchemy.orm import Session
from app.repositories import insurance_repository

def list_insurance_policies(db: Session) -> list:
    return insurance_repository.list_insurance_policies(db)