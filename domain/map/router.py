# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from database import get_db
# from crud.map import get_top10_categories_with_task_count, get_sunburst_data
# from typing import List
# from schemas import MapStat

# router = APIRouter(prefix="/maps", tags=["Map"])


# @router.get("", response_model=List[MapStat])
# def read_national_stats(db: Session = Depends(get_db)):
#     return get_stat_by_region(db)


# @router.get("/{region}", response_model=List[MapStat])
# def read_province_stats(region: str, db: Session = Depends(get_db)):
#     return get_stat_by_region(db, region=region)


# @router.get("/{region}/{subregion}", response_model=List[MapStat])
# def read_local_stats(region: str, subregion: str, db: Session = Depends(get_db)):
#     return get_stat_by_region(db, region=f"{region} {subregion}")

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional,List

from database import get_db
from crud.map import get_top10_categories_with_task_count, get_sunburst_data, get_top10_tasks_by_category
from schemas import MapStat, StatisticsOverview, TaskStats

router = APIRouter(
    prefix="/maps",
    tags=["Map"]
)

@router.get("/overview", response_model=StatisticsOverview)
def get_map_statistics_overview(region: Optional[str] = None, db: Session = Depends(get_db)):
    """
    지도용 통합 통계 API
    - Top10 분야(category) + 업무 수(task_count)
    - 분야별 업무 수 분포 (Sunburst용)
    - 지역(region) 쿼리로 필터링 가능 (없으면 전국)
    """
    top10 = get_top10_categories_with_task_count(db, region=region)
    sunburst = get_sunburst_data(db, region=region)
    return {
        "top10_categories": top10,
        "sunburst": sunburst
    }




@router.get("/top10-tasks", response_model=List[TaskStats])
def get_top10_tasks(region: Optional[str] = None, category: str = Query(...), db: Session = Depends(get_db)):
    """
    지역 + 분야(category)에 해당하는 업무(task) Top10 조회
    """
    return get_top10_tasks_by_category(db, region=region, category=category)
