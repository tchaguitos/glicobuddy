import os
import pathlib

from alembic import config, command

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from libs.orm import metadata


def rodar_migrations():
    root_do_projeto = pathlib.Path(__file__).parent.parent.resolve()

    os.chdir(f"{root_do_projeto}/glicobuddy")

    alembic_cfg = config.Config(f"{root_do_projeto}/glicobuddy/alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", get_postgres_uri())

    command.upgrade(alembic_cfg, "head")


def start_mappers():
    from contextos.usuarios.repositorio.orm import mapper_usuario
    from contextos.glicemias.repositorio.orm import mapper_glicemia


def get_session_factory(engine=None, is_test: bool = False):
    """"""
    engine = create_engine(
        get_postgres_uri(),
        isolation_level="REPEATABLE READ",
    )

    start_mappers()

    if is_test is True:
        metadata.drop_all(engine)
        rodar_migrations()

    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )()


def get_postgres_uri():
    usuario = os.environ.get("DB_USER", "glico")
    senha = os.environ.get("DB_PASSWORD", "test")
    host = os.environ.get("DB_HOST", "localhost")
    db_name = os.environ.get("DB_NAME", "glicotest")
    return f"postgresql+psycopg2://{usuario}:{senha}@{host}/{db_name}"
