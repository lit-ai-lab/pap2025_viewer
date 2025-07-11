# 📁 schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class ViewerBase(BaseModel):
    기관명: str
    처리요구명: str
    관련기관: Optional[str]
    감사결과: Optional[str]
    분야: Optional[str]
    업무: Optional[str]
    요약: Optional[str]
    특이사례: Optional[bool] = False
    내용분석: Optional[str]
    감사실시일자: Optional[date]


class ViewerCreate(ViewerBase):
    pass


class Viewer(ViewerBase):
    id: int

    class Config:
        orm_mode = True


class ViewerFilter(BaseModel):
    지역: Optional[str] = None
    감사실시기관: Optional[str] = None
    감사종류: Optional[str] = None
    시작일자: Optional[date] = None
    종료일자: Optional[date] = None
    분야: Optional[str] = None
    업무: Optional[str] = None
    키워드: Optional[str] = None
    특이사례포함: Optional[bool] = False


class MapStat(BaseModel):
    지역: str
    감사건수: int
