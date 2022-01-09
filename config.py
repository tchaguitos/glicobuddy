import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contextos.glicemias.repositorio.orm import metadata, start_mappers


def get_session_factory(engine=None, is_test: bool = False):
    if not engine:
        engine = create_engine(get_postgres_uri())

    if is_test is True:
        metadata.drop_all(engine)
        metadata.create_all(engine)

    start_mappers()

    return sessionmaker(bind=engine, expire_on_commit=False)()


def get_postgres_uri():
    usuario = os.environ.get("DB_USER", "glico")
    senha = os.environ.get("DB_PASSWORD", "test")
    host = os.environ.get("DB_HOST", "localhost")
    db_name = os.environ.get("DB_NAME", "glicotest")
    return f"postgresql+psycopg2://{usuario}:{senha}@{host}/{db_name}"
