from src.database import engine, SessionLocal
from src.models.base import Base
from src.models.role import Role


def init_db():
    Base.metadata.create_all(bind=engine)

    roles = ["ADMINISTRATOR", "COMMERCIAL", "TECHNICIAN"]

    session = SessionLocal()
    for role in roles:
        if not session.query(Role).filter_by(name=role).first():
            session.add(Role(name=role))
    session.commit()
    session.close()


def main():
    init_db()


if __name__ == '__main__':
    main()
