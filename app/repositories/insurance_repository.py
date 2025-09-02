from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from app.models.insurance_policies import InsurancePolicy
from app.models.members import Member

def list_insurance_policies(db: Session):
    result = db.query(
        InsurancePolicy,
        Member.full_name.label('insured_name')
    ).join(
        Member,
        InsurancePolicy.insured_member_id == Member.member_id
    ).all()
    
    # Convert the result to match the schema
    return [
        {
            **vars(policy),
            'insured_name': insured_name,
            '_sa_instance_state': None  # Remove SQLAlchemy state
        }
        for policy, insured_name in result
    ]