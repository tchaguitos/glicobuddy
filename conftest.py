import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_session

from contextos.glicemias.repositorio.orm import metadata, start_mappers


@pytest.fixture(scope="session")
def session():
    start_mappers()

    session = get_session()

    session.execute("DELETE FROM glicemia")

    yield session
