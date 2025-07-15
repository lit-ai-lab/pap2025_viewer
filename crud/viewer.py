# crud/viewer.py

from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from models import Viewer as ViewerModel
from schemas import ViewerFilter

def get_filtered_viewers(db: Session, filters: ViewerFilter) -> List[ViewerModel]:
    """
    ViewerFilter 에 담긴 모든 조건을 SQLAlchemy 쿼리로 적용해
    ViewerModel 목록을 반환합니다.
    """
    query = db.query(ViewerModel)

    # 1) 지역 필터
    if filters.regionId is not None:
        query = query.filter(ViewerModel.regionId == filters.regionId)

    # 2) 감사실시기관 필터
    if filters.agencyId is not None:
        query = query.filter(ViewerModel.agencyId == filters.agencyId)

    # 3) 감사종류 필터
    if filters.auditTypeId is not None:
        query = query.filter(ViewerModel.auditTypeId == filters.auditTypeId)

    # 4) 날짜 범위 필터
    if filters.startDate and filters.endDate:
        query = query.filter(ViewerModel.date.between(filters.startDate, filters.endDate))
    elif filters.startDate:
        query = query.filter(ViewerModel.date >= filters.startDate)
    elif filters.endDate:
        query = query.filter(ViewerModel.date <= filters.endDate)

    # 5) 분야(카테고리) 필터
    if filters.categoryId is not None:
        query = query.filter(ViewerModel.categoryId == filters.categoryId)

    # 6) 업무 필터
    if filters.taskId is not None:
        query = query.filter(ViewerModel.taskId == filters.taskId)

    # 7) 키워드 검색 (summary, result, originalText, analysisText 대상)
    if filters.keyword:
        kw = f"%{filters.keyword}%"
        query = query.filter(
            or_(
                ViewerModel.summary.ilike(kw),
                ViewerModel.result.ilike(kw),
                ViewerModel.originalText.ilike(kw),
                ViewerModel.analysisText.ilike(kw),
            )
        )

    # 8) 특이사례 포함 여부
    #    includeSpecial=False 면 특이사례 제외(specialCaseId IS NULL)
    #    includeSpecial=True 면 모든 결과(필터 없음)
    if not filters.includeSpecial:
        query = query.filter(ViewerModel.specialCaseId.is_(None))

    # 최신 순 정렬
    return query.order_by(ViewerModel.date.desc()).all()


def get_viewer_by_uuid(db: Session, case_uuid: str) -> Optional[ViewerModel]:
    """
    caseUuid 로 단일 ViewerModel 을 조회합니다.
    """
    return (
        db.query(ViewerModel)
          .filter(ViewerModel.caseUuid == case_uuid)
          .first()
    )


def get_viewer_by_id(db: Session, viewer_id: int) -> Optional[ViewerModel]:
    """
    PK(id) 로 단일 ViewerModel 을 조회합니다.
    """
    return (
        db.query(ViewerModel)
          .filter(ViewerModel.id == viewer_id)
          .first()
    )
