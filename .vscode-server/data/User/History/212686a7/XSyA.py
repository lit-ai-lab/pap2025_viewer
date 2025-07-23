from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.metadata import crud, schemas
from dependencies import get_db

router = APIRouter()

@router.get(
    "/metadata",
    response_model=schemas.MetaDataOut,
    summary="홈 메타데이터 조회"
)
def read_home_metadata(db: Session = Depends(get_db)):
    return crud.get_home_metadata(db)
