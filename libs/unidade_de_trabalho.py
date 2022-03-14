import abc

from config import get_session_factory
from sqlalchemy.orm.session import Session

from contextos.glicemias.repositorio.repo_dominio import (
    AbstractRepository,
    SqlAlchemyRepository,
)


class AbstractUnitOfWork(abc.ABC):
    repo: AbstractRepository
    committed: bool = False

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.rollback()

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
        self.repo: SqlAlchemyRepository = SqlAlchemyRepository(self.session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()
        self.committed = True

    def rollback(self):
        self.session.rollback()
