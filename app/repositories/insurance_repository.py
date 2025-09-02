from sqlalchemy.orm import Session
from app.models.insurance_policies import InsurancePolicy

def list_insurance_policies(db: Session):
    return db.query(InsurancePolicy).all()