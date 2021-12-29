import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DEFAULT_SESSION_FACTORY

from contextos.glicemias.repositorio import orm


@pytest.fixture(scope="session")
def session():
    orm.start_mappers()

    session = DEFAULT_SESSION_FACTORY()
    session.execute("DELETE FROM glicemia")

    yield session
