import pytest

from typing import Type

from libs.dominio import Dominio
from libs.repositorio import RepositorioDominio, RepositorioConsulta

from libs.unidade_de_trabalho import AbstractUnitOfWork, SqlAlchemyUnitOfWork

from contextos.usuarios.repositorio.repo_dominio import RepoDominioUsuarios
from contextos.usuarios.repositorio.repo_consulta import RepoConsultaUsuarios

from contextos.glicemias.repositorio.repo_dominio import RepoDominioGlicemias
from contextos.glicemias.repositorio.repo_consulta import RepoConsultaGlicemias


class FakeUOW(AbstractUnitOfWork):
    committed: bool = False
    repo_dominio: RepositorioDominio = None
    classe_repo_dominio: Type[RepositorioDominio] = None
    repo_consulta: RepositorioConsulta = None
    classe_repo_consulta: Type[RepositorioConsulta] = None

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakeSQLUOW(SqlAlchemyUnitOfWork):
    committed: bool = False
    repo_dominio: RepositorioDominio = None
    classe_repo_dominio: Type[RepositorioDominio] = None
    repo_consulta: RepositorioConsulta = None
    classe_repo_consulta: Type[RepositorioConsulta] = None

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_unidade_de_trabalho_abstrata():
    uow = FakeUOW()

    assert uow.committed is False
    assert uow.classe_repo_dominio is None

    with uow(Dominio.glicemias):
        assert uow.classe_repo_dominio

    with uow(Dominio.usuarios):
        uow.commit()
        assert uow.committed

    with pytest.raises(Exception) as e:
        with uow:
            assert (
                str(e.value)
                == "o dominio deve ser passado para utilizar a unidade de trabalho"
            )

    with pytest.raises(Exception) as e:
        with uow():
            assert (
                str(e.value)
                == "o dominio deve ser passado para utilizar a unidade de trabalho"
            )


def test_unidade_de_trabalho_abstrata_sql():
    uow = FakeSQLUOW()

    assert uow.committed is False

    assert uow.classe_repo_dominio is None
    assert uow.repo_dominio is None
    assert uow.repo_consulta is None

    with uow(Dominio.glicemias):
        assert uow.classe_repo_dominio
        assert isinstance(uow.repo_dominio, RepoDominioGlicemias)
        assert isinstance(uow.repo_consulta, RepoConsultaGlicemias)

    with uow(Dominio.usuarios):
        assert uow.classe_repo_dominio
        assert isinstance(uow.repo_dominio, RepoDominioUsuarios)
        assert isinstance(uow.repo_consulta, RepoConsultaUsuarios)

        uow.commit()

        assert uow.committed

    with pytest.raises(Exception) as e:
        with uow:
            assert (
                str(e.value)
                == "o dominio deve ser passado para utilizar a unidade de trabalho"
            )

    with pytest.raises(Exception) as e:
        with uow():
            assert (
                str(e.value)
                == "o dominio deve ser passado para utilizar a unidade de trabalho"
            )
