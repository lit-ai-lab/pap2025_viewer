from sqlalchemy import Column, Integer, String, Date, Boolean, Text
from database import Base

class Viewer(Base):
    __tablename__ = "viewers"

    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String)
    subject = Column(String)
    related_agency = Column(String)
    result = Column(String)
    field = Column(String)
    duty = Column(String)
    summary = Column(Text)
    has_case = Column(Boolean)
    original_text = Column(Text)
    analysis_text = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)

class MapStatistic(Base):
    __tablename__ = "map_statistics"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String)
    subregion = Column(String, nullable=True)
    value = Column(Integer)
    year = Column(Integer)
