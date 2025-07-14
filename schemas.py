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
    parentId: Optional[int] = None

    class Config:
        from_attributes = True

class AgencySchema(BaseModel):
    id: int
    name: str
    regionId: Optional[int] = None

    class Config:
        from_attributes = True

# 공통 필드 정의
class GamsaCaseBase(BaseModel):
    caseUuid: str
    agencyId: int
    relatedAgencyId: Optional[int] = None
    regionId: Optional[int] = None
    auditTypeId: int
    taskId: int
    fieldId: int
    specialCaseId: Optional[int] = None
    date: date  
    result: Optional[str] = None
    summary: Optional[str] = None
    originalText: Optional[str] = None
    analysisText: Optional[str] = None
    hwpPath: Optional[str] = None

    class Config:
        from_attributes = True

class ViewerCreate(GamsaCaseBase):
    pass

class Viewer(GamsaCaseBase):
    id: int
    agency: AgencySchema
    relatedAgency: Optional[AgencySchema] = None
    region: Optional[RegionSchema] = None
    auditType: AuditTypeSchema
    task: TaskSchema
    field: FieldSchema
    specialCase: Optional[SpecialCaseSchema] = None

    class Config:
        from_attributes = True

class ViewerFilter(BaseModel):
    regionId: Optional[int] = None
    agencyId: Optional[int] = None
    auditTypeId: Optional[int] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    fieldId: Optional[int] = None
    taskId: Optional[int] = None
    keyword: Optional[str] = None
    includeSpecial: Optional[bool] = False

class ViewerSchema(BaseModel):
    id: int
    caseUuid: str
    agencyId: int
    relatedAgencyId: Optional[int] = None
    regionId: Optional[int] = None
    auditTypeId: int
    taskId: int
    fieldId: int
    specialCaseId: Optional[int] = None
    date: date
    result: Optional[str] = None
    summary: Optional[str] = None
    originalText: Optional[str] = None
    analysisText: Optional[str] = None
    hwpPath: Optional[str] = None

    # Nested relations
    agency: AgencySchema
    relatedAgency: Optional[AgencySchema] = None
    region: Optional[RegionSchema] = None
    auditType: AuditTypeSchema
    task: TaskSchema
    field: FieldSchema
    specialCase: Optional[SpecialCaseSchema] = None

    class Config:
        from_attributes = True

class MapStat(BaseModel):
    region: str
    caseCount: int

    class Config:
        from_attributes = True
