from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from ...database import SessionLocal
from ...models import GamsaCase
from .schemas import GamsaCaseResponse, GamsaMapStats

router = APIRouter(prefix="/maps", tags=["Maps"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[GamsaMapStats])
def get_national_stats(db: Session = Depends(get_db)):
    results = db.query(GamsaCase.region, func.count(GamsaCase.id)).group_by(GamsaCase.region).all()
    return [GamsaMapStats(region=r[0], count=r[1]) for r in results]

@router.get("/{region}", response_model=List[GamsaMapStats])
def get_subregion_stats(region: str, db: Session = Depends(get_db)):
    results = db.query(GamsaCase.subregion, func.count(GamsaCase.id)).filter(GamsaCase.region == region).group_by(GamsaCase.subregion).all()
    return [GamsaMapStats(region=r[0], count=r[1]) for r in results]

@router.get("/{region}/{subregion}", response_model=List[GamsaCaseResponse])
def get_cases_by_subregion(region: str, subregion: str, db: Session = Depends(get_db)):
    return db.query(GamsaCase).filter(GamsaCase.region == region, GamsaCase.subregion == subregion).all()
