from datetime import datetime

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class Contract(Base):
    __tablename__ = "contract"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=True)
    client = relationship('Client')
    commercial_id = Column(Integer, ForeignKey('commercial.id', ondelete="SET NULL"), nullable=True)
    commercial = relationship('Commercial')
    total_amount = Column(Float, nullable=True)
    bill_to_pay = Column(Float, nullable=True)
    creation_date = Column(DateTime, nullable=False, default=datetime.now())
    status = Column(Boolean, nullable=False, default=False)
    events = relationship(argument='Event', back_populates='contract')

    def __repr__(self):
        return f'Contract n° {self.id}'
