from sqlalchemy import Column, Integer, String, Text, Date
from .database import Base

class GamsaCase(Base):
    __tablename__ = "gamsa_cases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    region = Column(String, index=True)
    subregion = Column(String, index=True)
    organization = Column(String, index=True)
    date = Column(Date)
    original_text = Column(Text)
    analysis_text = Column(Text)
    hwp_path = Column(String)