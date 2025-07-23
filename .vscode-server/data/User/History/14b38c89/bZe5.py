from sqlalchemy import func, distinct
from sqlalchemy.orm import Session
from domain.viewer.models import Viewer

def get_home_metadata(db: Session) -> dict:
    return {
        "inspection_agency_count": (
            db.query(func.count(distinct(Viewer.inspection_agency))).scalar() or 0
        ),
        "related_agency_count": (
            db.query(func.count(distinct(Viewer.related_agency))).scalar() or 0
        ),
        "audit_note_count": (
            db.query(func.count(distinct(Viewer.audit_note))).scalar() or 0
        ),
        "case_uuid_count": (
            db.query(func.count(distinct(Viewer.case_uuid))).scalar() or 0
        ),
    }
