import abc

from config import get_session_factory
from sqlalchemy.orm.session import Session

from libs.dominio import Dominio
from libs.repositorio import AbstractRepository, SqlAlchemyRepository


class AbstractUnitOfWork(abc.ABC):
    committed: bool
    repo_dominio: AbstractRepository
    classe_repo_dominio: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __call__(self, dominio):
        assert dominio, "o dominio deve ser passado para utilizar a unidade de trabalho"

        self.classe_repo_dominio = dominio.value[0]

        return self

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=get_session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.repo_dominio = self.classe_repo_dominio(self.session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()
        self.committed = True

    def rollback(self):
        self.session.rollback()
