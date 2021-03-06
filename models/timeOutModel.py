from sqlalchemy import Integer, String, DateTime, text, Time
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class TimeOut(Base):
    __tablename__ = 'time_outs'

    id = Column(String(36), primary_key=True, default=text('UUID()'))
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    time_log = Column(Time, nullable=False)
    active_status = Column(String(255), nullable=False, server_default=text("'Active'"))
    created_at = Column(DateTime, server_default=text('NOW()'))
    updated_at = Column(DateTime, server_onupdate=text('NOW()'))

    employees = relationship('Employee', back_populates='time_outs', lazy='joined')
    attendances = relationship('Attendance', back_populates='time_outs')
