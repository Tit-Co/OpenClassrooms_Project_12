from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), primary_key=True, nullable=False)
    client = relationship('Client')
    commercial_id = Column(Integer, ForeignKey('commercial.id'), primary_key=True, nullable=False)
    commercial = relationship('Commercial')
    total_amount = Column(Float, nullable=False)
    bill_to_pay = Column(Float, nullable=False)
    events = relationship(argument='Event', backref='events', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Contract n° {self.id}'
