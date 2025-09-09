from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from typing import List
from app.services import insurance_service
from app.services.insurance_service import create_insurance_policy, update_insurance_policy
from app.models.insurance_policies import InsurancePolicyCreate, InsurancePolicyOut, InsurancePolicyUpdate

router = APIRouter(prefix="/insurance", tags=["Insurance"])

@router.get("/list", response_model=List[InsurancePolicyOut])
def fetch_insurance_list(db: Session = Depends(get_db)):
    return insurance_service.list_insurance_policies(db)

@router.post("/create", response_model=InsurancePolicyOut, status_code=status.HTTP_201_CREATED)
def create_policy_endpoint(payload: InsurancePolicyCreate, db: Session = Depends(get_db)):
    policy_dict = payload.dict()
    # call service
    policy = create_insurance_policy(db, policy_dict)
    # ensure we return ORM -> Pydantic mapping; InsurancePolicyOut.orm_mode = True
    return policy

@router.put("/{policy_id}", response_model=InsurancePolicyOut)
def update_policy_endpoint(policy_id: int, payload: InsurancePolicyUpdate, db: Session = Depends(get_db)):
    updates = payload.dict(exclude_unset=True)
    policy = update_insurance_policy(db, policy_id, updates)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy