from sqlalchemy import create_engine, orm
from sqlalchemy.ext import declarative
from urllib.parse import quote
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{quote(settings.database_password)}' \
                          f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
