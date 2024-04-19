import pytest
from tests.fake_db import Base, get_db
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    echo=False,  # todo
)
FakeSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = FakeSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture()
def fake_db():
    for db in override_get_db():
        yield db


@pytest.fixture()
def fake_engine():
    return engine


@pytest.fixture()
def fake_client():
    return client


@pytest.fixture(autouse=True)
def tables(fake_engine):
    Base.metadata.create_all(fake_engine)
    yield
    Base.metadata.drop_all(fake_engine)
