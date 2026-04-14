from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Collaborator(Base):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    role = relationship("Role")


class Technician(Collaborator):
    __tablename__ = "technician"

    def __repr__(self):
        return f'Technician {self.name}'


class Commercial(Collaborator):
    __tablename__ = "commercial"

    def __repr__(self):
        return f'Commercial {self.name}'


class Administrator(Collaborator):
    __tablename__ = "administrator"

    def __repr__(self):
        return f'Administrator {self.name}'
