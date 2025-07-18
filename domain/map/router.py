from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from crud.map import (
    get_top10_categories,
    get_sunburst_categories_only,
    get_top10_tasks_by_category,
    get_sunburst_task_detail
)

router = APIRouter(
    prefix="/api/maps",
    tags=["Map"]
)

@router.get("/overview/")
def overview_statistics(region: Optional[str] = Query(None), db: Session = Depends(get_db)):
    """
    ✅ [1] 지역 기반 통계
    - 분야 Top10 리스트
    - sunburst: 분야만 포함
    """
    top10_categories = get_top10_categories(db, region)
    sunburst = get_sunburst_categories_only(db, region)

    return {
        "top10_categories": top10_categories,
        "sunburst": sunburst
    }

@router.get("/overview/category_detail/")
def detail_by_category(
    region: Optional[str] = Query(None),
    category: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    ✅ [2] 선택된 분야(category)에 대한 업무 top10 + sunburst
    """
    top10_tasks = get_top10_tasks_by_category(db, region, category)
    sunburst = get_sunburst_task_detail(db, region, category)

    return {
        "top10_tasks": top10_tasks,
        "sunburst": sunburst
    }
