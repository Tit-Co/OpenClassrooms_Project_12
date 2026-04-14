from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(20), nullable=False, unique=True)

    def __repr__(self):
        return f'Role {self.name}'
