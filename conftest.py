import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from contextos.glicemias.repositorio.orm import metadata, start_mappers


@pytest.fixture(scope="session")
def conexao_db():
    engine = create_engine("postgresql+psycopg2://glico:test@localhost/glicotest")
    metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session")
def session(conexao_db):
    start_mappers()
    yield sessionmaker(bind=conexao_db)()
    clear_mappers()
