from fastapi import HTTPException
from sqlalchemy.orm import Session
from crud import viewer as viewer_crud
from schemas import ViewerFilter, ViewerDetailResponse
from utils.excel import generate_excel_from_viewers

def filter_viewers(db: Session, filters: ViewerFilter):
    return viewer_crud.get_filtered_viewers(db, filters)

def get_viewer_detail(db: Session, viewer_id: int) -> ViewerDetailResponse:
    detail = viewer_crud.get_viewer_by_id(db, viewer_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Viewer not found")
    return detail

def download_filtered_viewers_excel(db: Session, filters: ViewerFilter):
    data = viewer_crud.get_filtered_viewers(db, filters)
    return generate_excel_from_viewers(data)

def download_viewer_original(viewer_id: int):
    # 이 함수는 파일 경로를 반환하는 것으로 가정
    file_path = f"static/downloads/original/{viewer_id}.hwp"
    return file_path

def download_viewer_combined(viewer_id: int):
    # 분석 + 원문 엑셀 생성
    return f"static/downloads/combined/{viewer_id}.xlsx"