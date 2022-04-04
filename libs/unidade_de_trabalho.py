import abc

from typing import Type

from config import get_session_factory
from sqlalchemy.orm.session import Session

from libs.dominio import Dominio

from libs.repositorio import RepositorioDominio, RepositorioConsulta


class UnidadeDeTrabalhoUtilizadaSemDominio(Exception):
    pass


class AbstractUnitOfWork(abc.ABC):
    committed: bool
    repo_dominio: RepositorioDominio
    repo_consulta: RepositorioConsulta
    classe_repo_dominio: Type[RepositorioDominio]
    classe_repo_consulta: Type[RepositorioConsulta]

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        # TODO: ajustar exception ao buscar registros pela api
        # self.rollback()
        pass

    def __call__(self, dominio: Dominio):
        assert dominio, "o dominio deve ser passado para utilizar a unidade de trabalho"

        # TODO: validar se existem os dois repos antes de setar?
        self.classe_repo_dominio = dominio.value[0]
        self.classe_repo_consulta = dominio.value[1]

        return self

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


# TODO: mudar apenas para `unidade de trabalho`
class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    repo_dominio: RepositorioDominio
    repo_consulta: RepositorioConsulta

    def __init__(self, session_factory=get_session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        if not hasattr(self, "classe_repo_dominio"):
            raise UnidadeDeTrabalhoUtilizadaSemDominio(
                "o dominio deve ser passado para utilizar a unidade de trabalho"
            )

        self.commited = False

        self.session: Session = self.session_factory()

        self.repo_dominio: RepositorioDominio = self.classe_repo_dominio(self.session)
        self.repo_consulta: RepositorioConsulta = self.classe_repo_consulta(
            self.session
        )

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()
        self.committed = True

    def rollback(self):
        self.session.rollback()
