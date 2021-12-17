import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contextos.glicemias.repositorio.orm import metadata, start_mappers


@pytest.fixture
def conexao_db():
    engine = create_engine("postgresql+psycopg2://glico:test@localhost/glicotest")

    metadata.drop_all(engine)
    metadata.create_all(engine)

    return engine


@pytest.fixture
def session(conexao_db):
    start_mappers()
    yield sessionmaker(bind=conexao_db)()
