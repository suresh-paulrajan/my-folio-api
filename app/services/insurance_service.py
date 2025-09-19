from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from app.models.insurance_policies import InsurancePolicy
from app.models.members import Member
from dateutil.relativedelta import relativedelta
from app.repositories import (insurance_repository)
from app.repositories.insurance_repository import (
    create_policy as repo_create_policy,
    get_policy as repo_get_policy,
    update_policy as repo_update_policy,
    get_reminder_by_policy,
    create_reminder,
    update_reminder
)

FREQ_MAP = {
    'MONTHLY': {'months': 1},
    'QUARTERLY': {'months': 3},
    'HALFYEARLY': {'months': 6},
    'YEARLY': {'months': 12},
    'SINGLE': None
}

def list_insurance_policies(db: Session, user_id: int) -> list:
    return insurance_repository.list_insurance_policies(db, user_id)

def _to_date(d):
    if d is None:
        return None
    if isinstance(d, datetime):
        return d.date()
    if isinstance(d, date):
        return d
    # assume iso str
    return date.fromisoformat(d)

def compute_next_due_from_start(start_date: date, freq: str) -> date:
    """
    If a start_date is given but next_premium_due_date not set,
    compute the next due as start_date + frequency interval.
    For monthly/quarterly/yearly: assume the first due is start_date if recurring,
    or next occurrence after today if start_date in past.
    """
    if start_date is None:
        return None

    today = date.today()

    if freq == 'SINGLE' or FREQ_MAP.get(freq) is None:
        # For single premium, use start_date as next_premium_due_date (or None)
        return start_date

    # compute next occurrence >= today
    delta_kwargs = FREQ_MAP[freq]
    candidate = start_date
    # if past, keep adding until >= today
    while candidate < today:
        candidate = candidate + relativedelta(**delta_kwargs)
    return candidate

def compute_reminder_next_run(next_premium_due_date: date, lead_days: int):
    if not next_premium_due_date:
        return None
    # schedule at midnight of that date minus lead_days (or preserve time as 00:00)
    return datetime.combine(next_premium_due_date - timedelta(days=lead_days), datetime.min.time())

def create_insurance_policy(db: Session, payload: dict) -> InsurancePolicy:
    """
    payload: already validated dict from Pydantic (create)
    Steps:
    - compute next_premium_due_date if missing using start_date + frequency
    - write policy
    - create reminder_tasks record with next_run_at = next_premium_due_date - lead_days
    """
    # normalize dates
    if payload.get('start_date'):
        payload['start_date'] = _to_date(payload['start_date'])
    if payload.get('next_premium_due_date'):
        payload['next_premium_due_date'] = _to_date(payload['next_premium_due_date'])
    if payload.get('maturity_date'):
        payload['maturity_date'] = _to_date(payload['maturity_date'])

    # compute missing next_premium_due_date
    if not payload.get('next_premium_due_date'):
        payload['next_premium_due_date'] = compute_next_due_from_start(payload.get('start_date'), payload.get('premium_frequency'))

    policy = repo_create_policy(db, payload)
    # create reminder
    next_run = compute_reminder_next_run(policy.next_premium_due_date, policy.lead_days or 7)
    # Get interval months from FREQ_MAP based on premium frequency
    freq_info = FREQ_MAP.get(policy.premium_frequency, {})
    interval_months = freq_info.get('months') if freq_info else None
    
    reminder_payload = {
        'user_id': policy.user_id,
        'policy_id': policy.policy_id,
        'task_kind': 'POLICY_PREMIUM',
        'next_run_at': next_run,
        'interval_months': interval_months,
        'active': True
    }
    create_reminder(db, reminder_payload)

    db.commit()
    db.refresh(policy)

    # Fetch the member and attach insured_name so response includes it ---
    member = db.query(Member).filter(Member.member_id == policy.insured_member_id).first()
    insured_name = None
    if member:
        # pick the right attribute; it might be `full_name` or `name` in your Member model
        insured_name = getattr(member, "full_name", None)

    # attach dynamic attribute on ORM instance — Pydantic's orm_mode will include it
    setattr(policy, "insured_name", insured_name)

    return policy

def update_insurance_policy(db: Session, policy_id: int, updates: dict) -> InsurancePolicy:
    policy = repo_get_policy(db, policy_id)
    if not policy:
        return None

    # normalize date inputs
    if updates.get('start_date'):
        updates['start_date'] = _to_date(updates['start_date'])
    if updates.get('next_premium_due_date'):
        updates['next_premium_due_date'] = _to_date(updates['next_premium_due_date'])
    if updates.get('maturity_date'):
        updates['maturity_date'] = _to_date(updates['maturity_date'])

    # If next_premium_due_date not provided but start_date/premium_frequency changed, recompute
    if not updates.get('next_premium_due_date'):
        new_start = updates.get('start_date', policy.start_date)
        new_freq = updates.get('premium_frequency', policy.premium_frequency)
        updates['next_premium_due_date'] = compute_next_due_from_start(new_start, new_freq)

    policy = repo_update_policy(db, policy, updates)

    # Get interval months from FREQ_MAP based on premium frequency
    freq_info = FREQ_MAP.get(policy.premium_frequency, {})
    interval_months = freq_info.get('months') if freq_info else None

    # sync reminder task
    r = get_reminder_by_policy(db, policy.policy_id)
    next_run = compute_reminder_next_run(policy.next_premium_due_date, policy.lead_days or 7)
    if r:
        update_reminder(db, r, {'next_run_at': next_run, 'is_active': True})
    else:
        create_reminder(db, {
            'user_id': policy.user_id,
            'policy_id': policy.policy_id,
            'task_kind': 'POLICY_PREMIUM',
            'next_run_at': next_run,
            'interval_months': interval_months,
            'active': True
        })

    db.commit()
    db.refresh(policy)
    return policy