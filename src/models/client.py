from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(Integer, nullable=False)
    company = Column(String(200), nullable=False)
    creation_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime, nullable=False)
    commercial_id = Column(Integer, ForeignKey('commercial.id'), nullable=True)
    commercial = relationship("Commercial")

    def __repr__(self):
        return f'Client {self.name}'
