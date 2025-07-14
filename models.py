from sqlalchemy import Column, Integer, String, Date, Boolean, Text
from database import Base

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'categorys'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    cases = relationship('Viewer', back_populates='category')

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    cases = relationship('Viewer', back_populates='task')

class AuditType(Base):
    __tablename__ = 'audit_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    cases = relationship('Viewer', back_populates='auditType')

class SpecialCase(Base):
    __tablename__ = 'special_cases'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    cases = relationship('Viewer', back_populates='specialCase')

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    parentId = Column(Integer, ForeignKey('regions.id'))
    parent = relationship('Region', remote_side=[id], backref='subregions')

    agencies = relationship('Agency', back_populates='region')
    cases = relationship('Viewer', back_populates='region')

class Agency(Base):
    __tablename__ = 'agencies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    regionId = Column(Integer, ForeignKey('regions.id'), nullable=True)

    region = relationship('Region', back_populates='agencies')
    cases = relationship('Viewer', back_populates='agency', foreign_keys='Viewer.agencyId', overlaps="relatedCases")
    relatedCases = relationship('Viewer', back_populates='relatedAgency', foreign_keys='Viewer.relatedAgencyId', overlaps="cases")

class Viewer(Base):
    __tablename__ = 'viewer'

    id = Column(Integer, primary_key=True, index=True)
    caseUuid = Column(String, nullable=False, unique=True, index=True)

    agencyId = Column(Integer, ForeignKey('agencies.id'), nullable=False)
    agency = relationship('Agency', back_populates='cases', foreign_keys=[agencyId], overlaps="relatedAgency")

    relatedAgencyId = Column(Integer, ForeignKey('agencies.id'))
    relatedAgency = relationship('Agency', back_populates='relatedCases', foreign_keys=[relatedAgencyId], overlaps="agency")

    regionId = Column(Integer, ForeignKey('regions.id'), nullable=True)
    region = relationship('Region', back_populates='cases')

    auditTypeId = Column(Integer, ForeignKey('audit_types.id'), nullable=False)
    auditType = relationship('AuditType', back_populates='cases')

    taskId = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    task = relationship('Task', back_populates='cases')

    categoryId = Column(Integer, ForeignKey('categorys.id'), nullable=False)
    category = relationship('Category', back_populates='cases')

    specialCaseId = Column(Integer, ForeignKey('special_cases.id'))
    specialCase = relationship('SpecialCase', back_populates='cases')

    date = Column(Date)
    result = Column(Text)
    summary = Column(Text)
    originalText = Column(Text)
    analysisText = Column(Text)
    hwpPath = Column(String)

class MapStatistic(Base):
    __tablename__ = "map_statistics"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String)
    subregion = Column(String, nullable=True)
    value = Column(Integer)
    year = Column(Integer)
