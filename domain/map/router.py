from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud.map import get_stat_by_region
from typing import List
from schemas import MapStat

router = APIRouter(prefix="/maps", tags=["Map"])


@router.get("", response_model=List[MapStat])
def read_national_stats(db: Session = Depends(get_db)):
    return get_stat_by_region(db)


@router.get("/{region}", response_model=List[MapStat])
def read_province_stats(region: str, db: Session = Depends(get_db)):
    return get_stat_by_region(db, region=region)


@router.get("/{region}/{subregion}", response_model=List[MapStat])
def read_local_stats(region: str, subregion: str, db: Session = Depends(get_db)):
    return get_stat_by_region(db, region=f"{region} {subregion}")
