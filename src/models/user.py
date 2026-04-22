from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class Collaborator(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(100), nullable=False)


class Technician(Collaborator):
    __tablename__ = "technician"
    __table_args__ = {'sqlite_autoincrement': True}

    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    role = relationship("Role")

    def __repr__(self):
        return f'Technician {self.name}'


class Commercial(Collaborator):
    __tablename__ = "commercial"
    __table_args__ = {'sqlite_autoincrement': True}

    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    role = relationship("Role")

    def __repr__(self):
        return f'Commercial {self.name}'


class Manager(Collaborator):
    __tablename__ = "manager"
    __table_args__ = {'sqlite_autoincrement': True}

    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    role = relationship("Role")

    def __repr__(self):
        return f'Manager {self.name}'
