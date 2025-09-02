from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List
from app.services import insurance_service
from app.models.insurance_policies import InsurancePolicyOut

router = APIRouter(prefix="/insurance", tags=["Insurance"])

@router.get("/list", response_model=List[InsurancePolicyOut])
def fetch_insurance_list(db: Session = Depends(get_db)):
    return insurance_service.list_insurance_policies(db)