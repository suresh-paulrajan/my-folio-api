from typing import Optional
from sqlalchemy.orm import Session
from app.models.insurance_policies import InsurancePolicy
from app.models.members import Member
from app.models.reminder_tasks import ReminderTask

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

def create_policy(db: Session, policy_create: dict) -> InsurancePolicy:
    policy = InsurancePolicy(**policy_create)
    db.add(policy)
    db.flush()  # get policy.policy_id
    return policy

def get_policy(db: Session, policy_id: int) -> Optional[InsurancePolicy]:
    return db.query(InsurancePolicy).filter(InsurancePolicy.policy_id == policy_id).first()

def update_policy(db: Session, policy: InsurancePolicy, updates: dict) -> InsurancePolicy:
    for k, v in updates.items():
        setattr(policy, k, v)
    db.add(policy)
    return policy

# reminder repo
def get_reminder_by_policy(db: Session, policy_id: int) -> Optional[ReminderTask]:
    return db.query(ReminderTask).filter(ReminderTask.policy_id == policy_id).first()

def create_reminder(db: Session, reminder: dict) -> ReminderTask:
    r = ReminderTask(**reminder)
    db.add(r)
    return r

def update_reminder(db: Session, r: ReminderTask, updates: dict) -> ReminderTask:
    for k, v in updates.items():
        setattr(r, k, v)
    db.add(r)
    return r