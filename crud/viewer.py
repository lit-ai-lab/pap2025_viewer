from sqlalchemy.orm import Session
from models import Viewer
from schemas import ViewerCreate, ViewerFilter
from typing import List
from sqlalchemy import and_, or_


def get_viewers(db: Session, filters: ViewerFilter) -> List[Viewer]:
    query = db.query(Viewer)

    if filters.지역:
        query = query.filter(Viewer.기관명.contains(filters.지역))
    if filters.감사실시기관:
        query = query.filter(Viewer.기관명 == filters.감사실시기관)
    if filters.감사종류:
        query = query.filter(Viewer.감사결과 == filters.감사종류)
    if filters.시작일자 and filters.종료일자:
        query = query.filter(Viewer.감사실시일자.between(filters.시작일자, filters.종료일자))
    if filters.분야:
        query = query.filter(Viewer.분야 == filters.분야)
    if filters.업무:
        query = query.filter(Viewer.업무 == filters.업무)
    if filters.키워드:
        query = query.filter(Viewer.요약.contains(filters.키워드))
    if filters.특이사례포함:
        query = query.filter(Viewer.특이사례 == True)

    return query.all()


def get_viewer_by_id(db: Session, viewer_id: int) -> Viewer:
    return db.query(Viewer).filter(Viewer.id == viewer_id).first()