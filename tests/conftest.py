import pytest
from collections import defaultdict
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base


engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    echo=False,  # todo
    poolclass=StaticPool,
)
FakeSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = FakeSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture()
def fake_db():
    for db in override_get_db():
        yield db


@pytest.fixture()
def fake_engine():
    return engine


@pytest.fixture()
def fake_client():
    from db.database import get_db
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True, scope="session")
def patch_config():
    patch("utils.config.load_config", return_value=defaultdict(str))


@pytest.fixture(autouse=True)
def tables(fake_engine):
    Base.metadata.create_all(fake_engine)
    yield
    Base.metadata.drop_all(fake_engine)
