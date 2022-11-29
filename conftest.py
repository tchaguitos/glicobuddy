import pytest

from config import get_session_factory

from tests.contextos.usuarios.mock import *


@pytest.fixture(scope="session")
def session():
    session = get_session_factory(is_test=True)

    yield session
