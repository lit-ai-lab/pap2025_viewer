from sqlalchemy import Column, Integer, String, Date, Boolean, Text
from database import Base

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'categorys'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    # cases = relationship('Viewer', back_populates='category')

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    # cases = relationship('Viewer', back_populates='task')

class AuditType(Base):
    __tablename__ = 'audit_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    # cases = relationship('Viewer', back_populates='auditType')

class special_case(Base):
    __tablename__ = 'special_cases'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    # cases = relationship('Viewer', back_populates='special_case')

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    parentId = Column(Integer, ForeignKey('regions.id'))
    parent = relationship('Region', remote_side=[id], backref='subregions')

    agencies = relationship('Agency', back_populates='region')
    # cases = relationship('Viewer', back_populates='region')

class Agency(Base):
    __tablename__ = 'agencies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=True)

    region = relationship('Region', back_populates='agencies')
    # cases = relationship('Viewer', back_populates='agency', foreign_keys='Viewer.agency_id', overlaps="relatedCases")
    # relatedCases = relationship('Viewer', back_populates='related_agency', foreign_keys='Viewer.related_agency_id', overlaps="cases")



class Viewer(Base):
    __tablename__ = 'viewer'

    id = Column(Integer, primary_key=True, index=True)

    # 직접 저장하는 단순 텍스트 필드들
    state = Column(String, nullable=True)                # 지역명 (ex. 전라남도)
    inspection_agency = Column(String, nullable=True)     # 감사실시기관
    disposition_request = Column(Text, nullable=True)     # 처분요구 및 조치사항
    related_agency = Column(String, nullable=True)        # 관련기관
    audit_result = Column(Text, nullable=True)            # 감사결과 종류
    category = Column(String, nullable=True)             # 분야 (auto_분야)
    task = Column(String, nullable=True)                 # 업무 (auto_업무)
    summary = Column(Text, nullable=True)                # auto_요약
    special_case = Column(Text, nullable=True)         # 특이사례 여부
    date = Column(String, nullable=True)
    inspection_type = Column(String, nullable=True)


class MapStatistic(Base):
    __tablename__ = "map_statistics"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, index=True)
    category = Column(String, index=True)
    task = Column(String, index=True)