import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contextos.glicemias.repositorio.orm import metadata


def get_session(engine=None, is_test: bool = False):
    """"""
    if not engine:
        engine = create_engine("postgresql+psycopg2://glico:test@localhost/glicotest")

    if is_test is True:
        metadata.create_all(engine)

    return sessionmaker(bind=engine)()


def get_postgres_uri():
    usuario = os.environ.get("DB_USER", "glico")
    senha = os.environ.get("DB_PASSWORD", "test")
    host = os.environ.get("DB_HOST", "localhost")
    db_name = os.environ.get("DB_NAME", "glicotest")
    return f"postgresql+psycopg2:://{usuario}:{senha}@{host}/{db_name}"
