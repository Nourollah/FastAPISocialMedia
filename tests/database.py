import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, orm
from alembic import command
from urllib.parse import quote
from app import main, models, database
from app.config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{quote(settings.database_password)}' \
                          f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DatabaseAndClientConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.session_maker()
        self.client_maker()

    def tearDown(self) -> None:
        self.session_closer()

    def session_maker(self) -> None:
        database.Base.metadata.drop_all(bind=engine)
        database.Base.metadata.create_all(bind=engine)
        # command.upgrade(SQLALCHEMY_DATABASE_URL, 'head')
        self.session = TestingSessionLocal()

    def session_closer(self) -> None:
        self.session.close()

    def client_maker(self) -> None:

        main.app.dependency_overrides[database.get_db] = self.get_test_db
        self.client = TestClient(main.app)

    def client_closer(self) -> None:
        del self.client

    def get_test_db(self):
        try:
            yield self.session
        finally:
            self.session.close()
