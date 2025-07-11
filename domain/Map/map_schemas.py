from pydantic import BaseModel
from typing import Optional
from datetime import date

class GamsaCaseBase(BaseModel):
    title: str
    region: str
    subregion: Optional[str] = None
    organization: str
    date: date

class GamsaCaseResponse(GamsaCaseBase):
    id: int
    class Config:
        orm_mode = True

class GamsaMapStats(BaseModel):
    region: str
    count: int