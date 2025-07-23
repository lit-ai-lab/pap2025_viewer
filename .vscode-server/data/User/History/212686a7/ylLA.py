from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import MetaData
from schemas import MetaData    
from crud.metadata import get_home_metadata(db) 

router = APIRouter()

@router.get(
    "/metadata",
    response_model=schemas.MetaDataOut,
    summary="홈 메타데이터 조회"
)
def read_home_metadata(db: Session = Depends(get_db)):
    return get_home_metadata(db)
