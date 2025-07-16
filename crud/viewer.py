from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from models import Viewer as ViewerModel
from schemas import ViewerFilter

def get_filtered_viewers(db: Session, filters: ViewerFilter) -> List[ViewerModel]:
    query = db.query(ViewerModel)

    # 1) 지역 필터 (state: ex. 전라남도)
    if filters.region_id is not None:
        query = query.filter(ViewerModel.state == filters.region_id)

    # 2) 감사실시기관 필터
    if filters.agency_id is not None:
        query = query.filter(ViewerModel.inspection_agency.ilike(f"%{filters.agency_id}%"))

    # 3) 감사결과 종류 필터
    if filters.audit_type_id is not None:
        query = query.filter(ViewerModel.disposition_request == filters.audit_type_id)

    # 4) 분야(category) 필터
    if filters.category_id is not None:
        query = query.filter(ViewerModel.category == filters.category_id)

    # 5) 업무(task) 필터
    if filters.task_id is not None:
        query = query.filter(ViewerModel.task == filters.task_id)

    # 6) 키워드 검색 (summary, audit_result)
    if filters.keyword:
        kw = f"%{filters.keyword}%"
        query = query.filter(
            or_(
                ViewerModel.summary.ilike(kw),
                ViewerModel.audit_result.ilike(kw),
            )
        )

    # 7) 특이사례 포함 여부
    if not filters.include_special:
        query = query.filter(ViewerModel.special_case.is_(None))

    return query.all()