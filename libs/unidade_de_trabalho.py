import abc

from typing import Type

from config import get_session_factory
from sqlalchemy.orm.session import Session

from libs.dominio import Dominio
from libs.repositorio import AbstractRepository, SqlAlchemyRepository


class UnidadeDeTrabalhoUtilizadaSemDominio(Exception):
    pass


class AbstractUnitOfWork(abc.ABC):
    committed: bool
    repo_dominio: SqlAlchemyRepository
    classe_repo_dominio: Type[SqlAlchemyRepository]

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.rollback()

    def __call__(self, dominio: Dominio):
        assert dominio, "o dominio deve ser passado para utilizar a unidade de trabalho"

        self.classe_repo_dominio = dominio.value[0]

        return self

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


# TODO: mudar apenas para `unidade de trabalho`
class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    repo_dominio: AbstractRepository

    def __init__(self, session_factory=get_session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        if not hasattr(self, "classe_repo_dominio"):
            raise UnidadeDeTrabalhoUtilizadaSemDominio(
                "o dominio deve ser passado para utilizar a unidade de trabalho"
            )

        self.commited = False

        self.session: Session = self.session_factory()
        self.repo_dominio: SqlAlchemyRepository = self.classe_repo_dominio(self.session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()
        self.committed = True

    def rollback(self):
        self.session.rollback()
