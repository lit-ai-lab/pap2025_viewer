from pydantic import BaseModel
from datetime import date

class GamsaViewerDetail(BaseModel):
    id: int
    title: str
    region: str
    subregion: str
    organization: str
    date: date
    original_text: str
    analysis_text: str

    class Config:
        orm_mode = True