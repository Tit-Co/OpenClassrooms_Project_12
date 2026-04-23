from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Client(Base):
    __tablename__ = "client"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False)
    company = Column(String(200), nullable=False)
    creation_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime, nullable=False)
    commercial_id = Column(Integer, ForeignKey('commercial.id', ondelete="SET NULL"), nullable=True)
    commercial = relationship("Commercial")

    is_active = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'Client {self.name}'
