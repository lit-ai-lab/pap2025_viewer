from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import Viewer, ViewerFilter
from crud import viewer
from utils.excel import generate_excel_file
from fastapi.responses import FileResponse
from typing import List
import os

router = APIRouter(prefix="/viewer", tags=["Viewer"])


@router.post("/filter", response_model=List[Viewer])
def filter_viewers(filters: ViewerFilter, db: Session = Depends(get_db)):
    return viewer.get_viewers(db, filters)


@router.get("/{viewer_id}", response_model=Viewer)
def read_viewer(viewer_id: int, db: Session = Depends(get_db)):
    return viewer.get_viewer_by_id(db, viewer_id)


@router.post("/filter/excel")
def download_excel(filters: ViewerFilter, db: Session = Depends(get_db)):
    records = viewer.get_viewers(db, filters)
    file_path = generate_excel_file(records)
    return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='application/vnd.ms-excel')
