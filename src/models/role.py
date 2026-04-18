from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Role(Base):
    __tablename__ = "role"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), nullable=False, unique=True)

    def __repr__(self):
        return f'Role {self.name}'
