import abc

from typing import Type, List, Optional

from config import get_session_factory
from sqlalchemy.orm.session import Session

from libs.dominio import Dominio
from libs.repositorio import RepositorioDominio, RepositorioConsulta

from libs.tipos_basicos.identificadores_db import IdUsuario


class UnidadeDeTrabalhoUtilizadaSemDominio(Exception):
    pass


class UnidadeDeTrabalhoAbstrata(abc.ABC):
    committed: bool
    repo_dominio: RepositorioDominio
    repo_consulta: RepositorioConsulta
    classe_repo_dominio: Type[RepositorioDominio]
    classe_repo_consulta: Type[RepositorioConsulta]
    usuario: Optional[IdUsuario]

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

    def coletar_novos_eventos(self):
        repositorios: List[RepositorioDominio] = []

        if hasattr(self, "repo_dominio") and self.repo_dominio:
            repositorios.extend([self.repo_dominio])

        for repositorio in repositorios:
            for agregado in repositorio.objetos_modificados:
                while getattr(agregado, "eventos", []):
                    yield agregado.eventos.pop(0)

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class UnidadeDeTrabalho(UnidadeDeTrabalhoAbstrata):
    repo_dominio: RepositorioDominio
    repo_consulta: RepositorioConsulta

    def __init__(
        self,
        session_factory=get_session_factory,
        usuario: Optional[IdUsuario] = None,
    ):
        self.session_factory = session_factory
        self.usuario = usuario

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
