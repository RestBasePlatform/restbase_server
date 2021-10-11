import os
import shutil
import sys

import pytest
from httpx import AsyncClient


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../source/"))
)
os.environ["DB_URL"] = "sqlite:///./tests/database.db"
os.environ["TEST"] = "True"

from main import app  # noqa: E402


def pytest_sessionstart():
    os.system("alembic downgrade base")
    os.system("alembic upgrade head")


@pytest.fixture(scope="function")
async def test_client():
    if not os.path.exists("./modules"):
        shutil.copytree("./source/modules", "./modules")
    if not os.path.exists("./templates"):
        shutil.copytree("./source/templates", "./templates")
    shutil.copy("./source/database.db", "./tests/database.db")
    client = AsyncClient(app=app, base_url="http://test/")
    try:
        yield client
    except Exception as e:
        print(e)
    finally:
        await client.aclose()


@pytest.fixture(scope="function")
def db_test_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("sqlite:///./tests/database.db")
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return Session()


@pytest.fixture()
def latest_test_module_config() -> dict:
    return {"name": "TestModule", "version": "0.4"}


def pytest_sessionfinish(session, exitstatus):
    shutil.rmtree("./source/modules")
    shutil.copytree("./modules", "./source/modules")
    shutil.rmtree("./modules")
    shutil.rmtree("./templates")
