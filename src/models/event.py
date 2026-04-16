from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(200), nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    location = Column(String(200), nullable=True)
    attendees = Column(Integer, nullable=True)
    notes = Column(String(500), nullable=True)
    contract_id = Column(Integer, ForeignKey('contract.id'), nullable=True)
    contract = relationship('Contract')
    technician_id = Column(Integer, ForeignKey('technician.id'), nullable=True)
    technician = relationship('Technician')

    def __repr__(self):
        return f'Event {self.name}'
