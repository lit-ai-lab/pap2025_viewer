from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import os
from models import DetailView
from database import get_db
from schemas import Viewer, ViewerFilter,DetailViewOut  # ViewerSchema → Viewer
from crud.viewer import (
    get_filtered_viewers,
)


router = APIRouter(prefix="/api/viewer", tags=["Viewer"])


@router.get(
    "/",
    response_model=List[Viewer],
    summary="필터에 맞춘 Viewer 목록 조회",
)
def list_viewers(
    region_id:      Optional[str] = Query(None,alias="regionId"),
    agency_id:      Optional[str] = Query(None, alias="agencyId"),
    audit_type_id:   Optional[str] = Query(None, alias="auditTypeId"),
    category_id:    Optional[str] = Query(None, alias="categoryId"),
    task_id:        Optional[str] = Query(None, alias="taskId"),
    keyword:       Optional[str] = Query(None, alias="keyword"),
    include_special: Optional[bool] = Query(False, alias="includeSpecial"),
    start_date:      Optional[str] = Query(None, alias="startDate"),
    end_date:        Optional[str] = Query(None, alias="endDate"),
    db:            Session       = Depends(get_db),

):
    filters = ViewerFilter(
        region_id=region_id,
        agency_id=agency_id,
        audit_type_id=audit_type_id,
        category_id=category_id,
        task_id=task_id,
        keyword=keyword,
        include_special=include_special,
        start_date=start_date,   
        end_date=end_date, 
    )
    return get_filtered_viewers(db, filters)

@router.get("/{detail_view_id}", response_model=DetailViewOut,summary="상세보기 -> 분석탭 조회",)
def get_detail_view(detail_view_id: int, db: Session = Depends(get_db)):
    detail = db.query(DetailView).filter(DetailView.id == detail_view_id).first()
    if not detail:
        raise HTTPException(status_code=404, detail="해당 상세 정보가 존재하지 않습니다.")
    return detail

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from .service import ViewerService
from schemas import ViewerFilter, DetailViewOut
from typing import Optional, List

router = APIRouter()

@router.get("/")
async def get_viewers(
    regionId: Optional[str] = None,
    agencyId: Optional[str] = None,
    auditTypeId: Optional[str] = None,
    startDate: Optional[str] = None,
    endDate: Optional[str] = None,
    categoryId: Optional[str] = None,
    taskId: Optional[str] = None,
    keyword: Optional[str] = None,
    includeSpecial: bool = False,
    db: Session = Depends(get_db)
):
    """Get filtered viewer data"""
    try:
        service = ViewerService(db)
        filters = ViewerFilter(
            regionId=regionId,
            agencyId=agencyId,
            auditTypeId=auditTypeId,
            startDate=startDate,
            endDate=endDate,
            categoryId=categoryId,
            taskId=taskId,
            keyword=keyword,
            includeSpecial=includeSpecial
        )
        return service.get_filtered_data(filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))