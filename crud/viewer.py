from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from models import Viewer as ViewerModel
from schemas import ViewerFilter

def get_filtered_viewers(db: Session, filters: ViewerFilter) -> List[ViewerModel]:
    query = db.query(ViewerModel)

    # 1) 지역 필터 (state: ex. 전라남도)
    if filters.regionId is not None:
        query = query.filter(ViewerModel.state == filters.regionId)

    # 2) 감사실시기관 필터
    if filters.agencyId is not None:
        query = query.filter(ViewerModel.inspectionAgency == filters.agencyId)

    # 3) 감사결과 종류 필터
    if filters.auditTypeId is not None:
        query = query.filter(ViewerModel.dispositionRequest == filters.auditTypeId)

    # 4) 분야(category) 필터
    if filters.categoryId is not None:
        query = query.filter(ViewerModel.category == filters.categoryId)

    # 5) 업무(task) 필터
    if filters.taskId is not None:
        query = query.filter(ViewerModel.task == filters.taskId)

    # 6) 키워드 검색 (summary, auditResult)
    if filters.keyword:
        kw = f"%{filters.keyword}%"
        query = query.filter(
            or_(
                ViewerModel.summary.ilike(kw),
                ViewerModel.auditResult.ilike(kw),
            )
        )

    # 7) 특이사례 포함 여부
    if not filters.includeSpecial:
        query = query.filter(ViewerModel.specialCase.is_(None))

    return query.all()
