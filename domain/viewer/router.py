from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import os

from database import get_db
from schemas import Viewer, ViewerFilter  # ViewerSchema → Viewer
from crud.viewer import (
    get_filtered_viewers,
)
from utils.excel import generate_excel_file

router = APIRouter(prefix="/api/viewer", tags=["Viewer"])


@router.get(
    "/",
    response_model=List[Viewer],
    summary="필터에 맞춘 Viewer 목록 조회",
)
def list_viewers(
    region_id:      Optional[str] = Query(None),
    agency_id:      Optional[str] = Query(None),
    audit_type_id:   Optional[str] = Query(None),
    category_id:    Optional[str] = Query(None),
    task_id:        Optional[str] = Query(None),
    keyword:       Optional[str] = Query(None),
    include_special: bool         = Query(False),
    db:            Session       = Depends(get_db),
    start_date:      Optional[date] = Query(None),
    end_date:        Optional[date] = Query(None),
):
    filters = ViewerFilter(
        region_id=region_id,
        agency_id=agency_id,
        audit_type_id=audit_type_id,
        category_id=category_id,
        task_id=task_id,
        keyword=keyword,
        include_special=include_special,
    )
    return get_filtered_viewers(db, filters)



@router.post(
    "/export",
    summary="필터에 맞춘 Viewer 목록을 엑셀(.xlsx)로 다운로드",
)
def export_excel(
    filters: ViewerFilter,
    db: Session = Depends(get_db),
):
    records = get_filtered_viewers(db, filters)
    file_path = generate_excel_file(records)
    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.get(
    "/{viewer_id}/original",
    summary="Viewer 원문(HWP) 다운로드",
)
def download_original(viewer_id: int):
    file_path = f"static/downloads/original/{viewer_id}.hwp"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path=file_path,
        filename=f"{viewer_id}.hwp",
        media_type="application/octet-stream",
    )


@router.get(
    "/{viewer_id}/combined",
    summary="Viewer 분석+원문 엑셀 다운로드",
)
def download_combined(viewer_id: int):
    file_path = f"static/downloads/combined/{viewer_id}.xlsx"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path=file_path,
        filename=f"{viewer_id}_combined.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )