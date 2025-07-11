from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from ...database import SessionLocal
from ...models import GamsaCase
from .schemas import GamsaViewerDetail
import os

router = APIRouter(prefix="/viewer", tags=["Viewer"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{viewer_id}", response_model=GamsaViewerDetail)
def get_viewer_detail(viewer_id: int, db: Session = Depends(get_db)):
    case = db.query(GamsaCase).filter(GamsaCase.id == viewer_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.get("/{viewer_id}/download/hwp")
def download_hwp(viewer_id: int, db: Session = Depends(get_db)):
    case = db.query(GamsaCase).filter(GamsaCase.id == viewer_id).first()
    if not case or not case.hwp_path:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=case.hwp_path, media_type='application/haansofthwp', filename=os.path.basename(case.hwp_path))

@router.get("/{viewer_id}/download/combined")
def download_combined(viewer_id: int):
    # dummy response: 실제로는 파일 생성 후 경로 반환
    return FileResponse("/path/to/generated/combined_file.txt", filename="combined_report.txt")
