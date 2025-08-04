from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Optional

from models import Viewer as ViewerModel, OriginalText, DetailView
from schemas import ViewerFilter
from sqlalchemy import or_, and_

def get_filtered_viewers(db: Session,
                         filters: ViewerFilter) -> List[ViewerModel]:
    query = db.query(ViewerModel)

    print(filters.region_id)
    # 1) 지역 필터 (state: ex. 전라남도)1
    if filters.region_id is not None:
        query = query.filter(ViewerModel.state == filters.region_id)

    # 2) 감사실시기관 필터
    if filters.agency_id is not None:
        query = query.filter(
            ViewerModel.inspection_agency.ilike(f"%{filters.agency_id}%"))

    # 3) 감사결과 종류 필터
    if filters.audit_type_id is not None:
        query = query.filter(
            ViewerModel.inspection_type == filters.audit_type_id)

    # 4) 날짜 필터
    if filters.start_date and filters.end_date:
        print("start_date")
        # date 컬럼이 'YYYY-MM-DD' 문자열이면 lexicographical 비교가 날짜 비교와 동일합니다
        query = query.filter(
            ViewerModel.date >= filters.start_date.isoformat(),
            ViewerModel.date <= filters.end_date.isoformat(),
        )

    # 5) 분야(category) 필터
    if filters.category_id is not None:
        query = query.filter(ViewerModel.category == filters.category_id)

    # 6) 업무(task) 필터
    if filters.task_id is not None:
        query = query.filter(ViewerModel.task.ilike(f"%{filters.task_id}%"))

    
    # 7) 키워드 검색 (summary, audit_result → preprocessed_text 기준)
    if filters.keyword or filters.keyword_extras:
        query = query.join(
            DetailView, ViewerModel.detail_view_id == DetailView.id
        ).join(
            OriginalText, OriginalText.detail_view_id == DetailView.id
        )

        # FastAPI 쿼리에서 리스트가 문자열로 오는 경우 처리
        if isinstance(filters.keyword_extras, str):
            filters.keyword_extras = filters.keyword_extras.split(",")

        # keyword + extras 병합
        keywords = []
        if filters.keyword:
            keywords.append(filters.keyword.strip())
        if filters.keyword_extras:
            keywords.extend([kw.strip() for kw in filters.keyword_extras if kw.strip()])

        # 필터링 조건
        if keywords:
            conditions = [
                OriginalText.preprocessed_text.ilike(f"%{kw}%")
                for kw in keywords
            ]

            mode = (filters.keyword_mode or "AND").upper()
            if mode == "AND":
                for cond in conditions:
                    query = query.filter(cond)
            elif mode == "OR":
                query = query.filter(or_(*conditions))


        # 특이사례 필터
    if filters.include_special is True:
        # 특이사례 있는 것만
        query = query.filter(ViewerModel.special_case.isnot(None))
    elif filters.include_special is False:
        # 특이사례 없는 것만
        query = query.filter(ViewerModel.special_case.is_(None))
    # 이러면 None이면 전체 조회 가능

    return query.all()
