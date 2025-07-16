# domain/viewer/router.py

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import os

from database import get_db
from schemas import ViewerSchema, ViewerFilter
from crud.viewer import (
    get_filtered_viewers,
    get_viewer_by_id,
    get_viewer_by_uuid,
)
from utils.excel import generate_excel_file

router = APIRouter(prefix="/api/viewer", tags=["Viewer"])


@router.get(
    "/",
    response_model=List[ViewerSchema],
    summary="필터에 맞춘 Viewer 목록 조회",
)
def list_viewers(
    regionId:      Optional[int]  = Query(None),
    agencyId:      Optional[int]  = Query(None),
    relatedAgencyId: Optional[int] = Query(None),
    auditTypeId:   Optional[int]  = Query(None),
    startDate:     Optional[date] = Query(None),
    endDate:       Optional[date] = Query(None),
    categoryId:    Optional[int]  = Query(None),
    taskId:        Optional[int]  = Query(None),
    keyword:       Optional[str]  = Query(None),
    includeSpecial: bool          = Query(None),
    db:            Session        = Depends(get_db),
):
    filters = ViewerFilter(
        regionId=regionId,
        agencyId=agencyId,
        relatedAgencyId = relatedAgencyId,
        auditTypeId=auditTypeId,
        startDate=startDate,
        endDate=endDate,
        categoryId=categoryId,
        taskId=taskId,
        keyword=keyword,
        includeSpecial=includeSpecial,
    )
    return get_filtered_viewers(db, filters)


@router.get(
    "/id/{viewer_id}",
    response_model=ViewerSchema,
    summary="PK(id)로 Viewer 상세 조회",
)
def read_by_id(viewer_id: int, db: Session = Depends(get_db)):
    viewer = get_viewer_by_id(db, viewer_id)
    if not viewer:
        raise HTTPException(status_code=404, detail="Viewer not found")
    return viewer


@router.get(
    "/uuid/{case_uuid}",
    response_model=ViewerSchema,
    summary="caseUuid로 Viewer 상세 조회",
)
def read_by_uuid(case_uuid: str, db: Session = Depends(get_db)):
    viewer = get_viewer_by_uuid(db, case_uuid)
    if not viewer:
        raise HTTPException(status_code=404, detail="Viewer not found")
    return viewer


@router.post(
    "/export",
    summary="필터에 맞춘 Viewer 목록을 엑셀(.xlsx)로 다운로드",
)
def export_excel(
    filters: ViewerFilter,
    db:      Session = Depends(get_db),
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
