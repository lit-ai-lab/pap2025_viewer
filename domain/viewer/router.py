from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import Viewer, ViewerFilter, ViewerSchema
from crud import viewer
from utils.excel import generate_excel_file
from fastapi.responses import FileResponse
from fastapi import HTTPException
from typing import List
import os

router = APIRouter(prefix="/viewer", tags=["Viewer"])


@router.post("/filter", response_model=List[Viewer])
def filter_viewers(filters: ViewerFilter, db: Session = Depends(get_db)):
    return viewer.get_viewers(db, filters)

@router.get("/id/{viewer_id}", response_model=ViewerSchema)
def read_viewer_by_id(viewer_id: int, db: Session = Depends(get_db)):
    """
    정수형 PK(id)로 Viewer 조회
    """
    result = viewer.get_viewer_by_id(db, viewer_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Viewer not found")
    return result

@router.get("/{case_uuid}", response_model=Viewer)
def read_viewer(case_uuid: str, db: Session = Depends(get_db)):
    result = viewer.get_viewer_by_uuid(db, case_uuid)
    if result is None:
        raise HTTPException(status_code=404, detail="Viewer not found")
    return result


@router.post("/filter/excel")
def download_excel(filters: ViewerFilter, db: Session = Depends(get_db)):
    records = viewer.get_viewers(db, filters)
    file_path = generate_excel_file(records)
    return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='application/vnd.ms-excel')