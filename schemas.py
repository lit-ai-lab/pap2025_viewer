from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date

# 필터용 스키마 (프론트 요청 시 사용)


# # 필터용 스키마 (프론트 요청 시 사용)
# class ViewerFilter(BaseModel):
#     region_id: Optional[str] = None  # 지역명 텍스트
#     agency_id: Optional[str] = None  # 감사실시기관 텍스트
#     audit_type_id: Optional[str] = None  # 감사결과종류 텍스트

# 단일 조회 시 응답
class Viewer(BaseModel):
    id: int
    state: Optional[str]
    inspection_agency: Optional[str]
    disposition_request: Optional[str]
    related_agency: Optional[str]
    audit_result: Optional[str]
    category: Optional[str]
    task: Optional[str]
    summary: Optional[str]
    special_case: Optional[str]

    class Config:
        orm_mode = True

class MapStat(BaseModel):
    region: str
    caseCount: int

    class Config:
        from_attributes = True
        

# 분야별 통계 (Top10)
class CategoryStats(BaseModel):
    category: str
    count: int
    task_count: int

# /maps/overview 응답용 스키마
class StatisticsOverview(BaseModel):
    top10_categories: List[CategoryStats]
    sunburst: Dict[str, Dict[str, int]]
    

class TaskStats(BaseModel):
    task: str
    count: int




class ViewerFilter(BaseModel):
    region_id: Optional[str] = None
    agency_id: Optional[str] = None
    audit_type_id: Optional[str] = None
    category_id: Optional[str] = None  # ← 이게 없으면 추가해야 함
    task_id: Optional[str] = None      # ← 이것도 사용 중이라면 같이 추가
    keyword: Optional[str] = None
    include_special: Optional[bool] = False
    start_date: Optional[date] = None
    end_date: Optional[date] = None