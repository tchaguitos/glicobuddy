import pytest

from libs.dominio import Dominio

from libs.repositorio import AbstractRepository

from libs.unidade_de_trabalho import AbstractUnitOfWork, SqlAlchemyUnitOfWork

from contextos.glicemias.repositorio.repo_dominio import RepoDominioGlicemias


class FakeUOW(AbstractUnitOfWork):
    committed: bool = False
    classe_repo_dominio: AbstractRepository = None
    repo_dominio: AbstractRepository = None

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakeSQLUOW(SqlAlchemyUnitOfWork):
    committed: bool = False
    classe_repo_dominio: AbstractRepository = None
    repo_dominio: AbstractRepository = None

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

    with uow(Dominio.glicemias):
        assert uow.classe_repo_dominio
        assert isinstance(uow.repo_dominio, RepoDominioGlicemias)

    with uow(Dominio.usuarios):
        uow.commit()
        assert uow.committed

    with pytest.raises(Exception) as e:
        with uow():
            assert (
                str(e.value)
                == "o dominio deve ser passado para utilizar a unidade de trabalho"
            )
