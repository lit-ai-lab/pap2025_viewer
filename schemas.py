# 📁 schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class FieldSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TaskSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class AuditTypeSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SpecialCaseSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RegionSchema(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]

    class Config:
        from_attributes = True


class AgencySchema(BaseModel):
    id: int
    name: str
    region_id: int

    class Config:
        from_attributes = True


class GamsaCaseBase(BaseModel):
    case_uuid: str
    agency_id: int
    related_agency_id: Optional[int] = None
    region_id: Optional[int] = None
    audit_type_id: int
    task_id: int
    field_id: int
    special_case_id: Optional[int] = None
    date: Optional[date] = None
    result: Optional[str] = None
    summary: Optional[str] = None
    original_text: Optional[str] = None
    analysis_text: Optional[str] = None
    hwp_path: Optional[str] = None

class ViewerCreate(GamsaCaseBase):
    pass

class Viewer(GamsaCaseBase):
    id: int
    agency: AgencySchema
    related_agency: Optional[AgencySchema] = None
    region: Optional[RegionSchema] = None
    audit_type: AuditTypeSchema
    task: TaskSchema
    field: FieldSchema
    special_case: Optional[SpecialCaseSchema] = None

    class Config:
        from_attributes = True


class ViewerFilter(BaseModel):
    region_id: Optional[int] = None
    agency_id: Optional[int] = None
    audit_type_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    field_id: Optional[int] = None
    task_id: Optional[int] = None
    keyword: Optional[str] = None
    include_special: Optional[bool] = False

class MapStat(BaseModel):
    region: str
    case_count: int

    class Config:
        from_attributes = True

#기존과 다른 변수 이름바꾸기
