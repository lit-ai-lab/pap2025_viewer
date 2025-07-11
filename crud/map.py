from sqlalchemy.orm import Session
from models import Viewer
from schemas import MapStat
from sqlalchemy import func
from typing import List


def get_stat_by_region(db: Session, region: str = None):
    query = db.query(Viewer.기관명, func.count().label("감사건수"))
    if region:
        query = query.filter(Viewer.기관명.contains(region))

    return query.group_by(Viewer.기관명).order_by(func.count().desc()).limit(10).all()