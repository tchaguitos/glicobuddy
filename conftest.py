import pytest

from config import get_session

from contextos.glicemias.repositorio.orm import start_mappers


@pytest.fixture(scope="session")
def session():
    start_mappers()

    session = get_session()

    yield session
