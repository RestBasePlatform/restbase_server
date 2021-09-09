import os
import shutil
import sys

import pytest
from fastapi.testclient import TestClient


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../source/"))
)

from main import app  # noqa: E402


def pytest_sessionstart():
    os.system("alembic upgrade head")


@pytest.fixture(scope="function")
def test_client():
    if os.path.exists("./modules"):
        shutil.rmtree("./modules")
    shutil.copy("./source/database.db", "./tests/database.db")
    return TestClient(app)


@pytest.fixture(scope="function")
def db_test_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("sqlite:///./tests/database.db")
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return Session()


@pytest.fixture()
def latest_test_module_config() -> dict:
    return {"name": "TestModule", "version": "1.5"}
