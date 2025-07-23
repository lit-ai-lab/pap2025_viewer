from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import MetaData
from schemas import MetaData as MD
from crud.metadata import get_home_metadata

router = APIRouter(prefix="", tags=["Metadata"],)

@router.get(
    "/metadata",
    response_model=MD.MetaDataOut,
    summary="홈 메타데이터 조회"
)
def read_home_metadata(db: Session = Depends(get_db)):
    return get_home_metadata(db)
