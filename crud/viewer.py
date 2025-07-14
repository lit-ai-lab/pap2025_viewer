from sqlalchemy.orm import Session
from models import Viewer as ViewerModel
from schemas import ViewerFilter
from typing import List, Optional


def getViewers(db: Session, filters: ViewerFilter) -> List[ViewerModel]:
    """
    Apply filters from ViewerFilter to retrieve matching ViewerModel records.
    """
    query = db.query(ViewerModel)

    # region filter (by regionId)
    if filters.regionId is not None:
        query = query.filter(ViewerModel.regionId == filters.regionId)

    # agency filter (by agencyId)
    if filters.agencyId is not None:
        query = query.filter(ViewerModel.agencyId == filters.agencyId)

    # audit type filter
    if filters.auditTypeId is not None:
        query = query.filter(ViewerModel.auditTypeId == filters.auditTypeId)

    # date range filter
    if filters.startDate and filters.endDate:
        query = query.filter(
            ViewerModel.date.between(filters.startDate, filters.endDate)
        )
    elif filters.startDate:
        query = query.filter(ViewerModel.date >= filters.startDate)
    elif filters.endDate:
        query = query.filter(ViewerModel.date <= filters.endDate)

    # field filter
    if filters.fieldId is not None:
        query = query.filter(ViewerModel.fieldId == filters.fieldId)

    # task filter
    if filters.taskId is not None:
        query = query.filter(ViewerModel.taskId == filters.taskId)

    # keyword in summary
    if filters.keyword:
        query = query.filter(ViewerModel.summary.contains(filters.keyword))

    # include only those with specialCaseId
    if filters.includeSpecial:
        query = query.filter(ViewerModel.specialCaseId.is_not(None))

    return query.all()


def getViewerByUuid(db: Session, viewerId: str) -> Optional[ViewerModel]:
    """Retrieve a single ViewerModel by its primary key ID."""
    return (
        db.query(ViewerModel)
          .filter(ViewerModel.id == viewerId)
          .first()
    )


def getViewerById(db: Session, viewerId: int) -> Optional[ViewerModel]:
    """
    Primary Key(id)로 Viewer 한 건 조회
    """
    return (
        db.query(ViewerModel)
          .filter(ViewerModel.id == viewerId)
          .first()
    )
