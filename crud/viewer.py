# crud/viewer.py
from sqlalchemy.orm import Session
from models import Viewer as ViewerModel
from schemas import ViewerFilter
from typing import List, Optional


def get_viewers(db: Session, filters: ViewerFilter) -> List[ViewerModel]:
    """
    Apply filters from ViewerFilter to retrieve matching ViewerModel records.
    """
    query = db.query(ViewerModel)

    # region filter (by region_id)
    if filters.region_id is not None:
        query = query.filter(ViewerModel.region_id == filters.region_id)

    # agency filter (by agency_id)
    if filters.agency_id is not None:
        query = query.filter(ViewerModel.agency_id == filters.agency_id)

    # audit type filter
    if filters.audit_type_id is not None:
        query = query.filter(ViewerModel.audit_type_id == filters.audit_type_id)

    # date range filter
    if filters.start_date and filters.end_date:
        query = query.filter(
            ViewerModel.date.between(filters.start_date, filters.end_date)
        )
    elif filters.start_date:
        query = query.filter(ViewerModel.date >= filters.start_date)
    elif filters.end_date:
        query = query.filter(ViewerModel.date <= filters.end_date)

    # field filter
    if filters.field_id is not None:
        query = query.filter(ViewerModel.field_id == filters.field_id)

    # task filter
    if filters.task_id is not None:
        query = query.filter(ViewerModel.task_id == filters.task_id)

    # keyword in summary
    if filters.keyword:
        query = query.filter(ViewerModel.summary.contains(filters.keyword))

    # include only those with special_case
    if filters.include_special:
        query = query.filter(ViewerModel.special_case_id.is_not(None))

    return query.all()


def get_viewer_by_uuid(db: Session, viewer_id: str) -> Optional[ViewerModel]:
    """Retrieve a single ViewerModel by its primary key ID."""
    return (
        db.query(ViewerModel)
          .filter(ViewerModel.id == viewer_id)
          .first()
    )


def get_viewer_by_id(db: Session, viewer_id: int) -> Optional[ViewerModel]:
    """
    Primary Key(id)로 Viewer 한 건 조회
    """
    return (
        db.query(ViewerModel)
          .filter(ViewerModel.id == viewer_id)
          .first()
    )