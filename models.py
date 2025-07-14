from sqlalchemy import Column, Integer, String, Date, Boolean, Text
from database import Base

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Field(Base):
    __tablename__ = 'fields'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    cases = relationship('Viewer', back_populates='field')

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    cases = relationship('Viewer', back_populates='task')

class AuditType(Base):
    __tablename__ = 'audit_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    cases = relationship('Viewer', back_populates='audit_type')

class SpecialCase(Base):
    __tablename__ = 'special_cases'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    cases = relationship('Viewer', back_populates='special_case')

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey('regions.id'))
    parent = relationship('Region', remote_side=[id], backref='subregions')

    agencies = relationship('Agency', back_populates='region')
    cases = relationship('Viewer', back_populates='region')

class Agency(Base):
    __tablename__ = 'agencies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)

    region = relationship('Region', back_populates='agencies')
    cases = relationship('Viewer', back_populates='agency', foreign_keys='Viewer.related_agency_id')

class Viewer(Base):
    __tablename__ = 'gamsa_cases'

    id = Column(Integer, primary_key=True, index=True)
    case_uuid = Column(String, nullable=False, unique=True, index=True)

    agency_id = Column(Integer, ForeignKey('agencies.id'), nullable=False)
    agency = relationship('Agency', back_populates='cases', foreign_keys=[agency_id])

    related_agency_id = Column(Integer, ForeignKey('agencies.id'))
    related_agency = relationship('Agency', foreign_keys=[related_agency_id])

    region_id = Column(Integer, ForeignKey('regions.id'))
    region = relationship('Region', back_populates='cases')

    audit_type_id = Column(Integer, ForeignKey('audit_types.id'), nullable=False)
    audit_type = relationship('AuditType', back_populates='cases')

    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    task = relationship('Task', back_populates='cases')

    field_id = Column(Integer, ForeignKey('fields.id'), nullable=False)
    field = relationship('Field', back_populates='cases')

    special_case_id = Column(Integer, ForeignKey('special_cases.id'))
    special_case = relationship('SpecialCase', back_populates='cases')

    date = Column(Date)
    result = Column(Text)
    summary = Column(Text)
    original_text = Column(Text)
    analysis_text = Column(Text)
    hwp_path = Column(String)


class MapStatistic(Base):
    __tablename__ = "map_statistics"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String)
    subregion = Column(String, nullable=True)
    value = Column(Integer)
    year = Column(Integer)
