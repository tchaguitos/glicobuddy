from uuid import UUID
from uuid import uuid4
from datetime import datetime
from typing import Set, Optional
from freezegun import freeze_time

from contextos.glicemias.dominio.entidades import Glicemia

from contextos.glicemias.dominio.entidades import Auditoria, Glicemia
from contextos.glicemias.dominio.comandos import (
    CriarGlicemia,
    EditarGlicemia,
    RemoverGlicemia,
)
from contextos.glicemias.servicos.executores import (
    criar_glicemia,
    editar_glicemia,
    remover_glicemia,
)
from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia

from contextos.glicemias.repositorio.repo_dominio import AbstractRepository
from contextos.glicemias.servicos.unidade_de_trabalho import AbstractUnitOfWork


class FakeRepo(AbstractRepository):
    __glicemias: Set[Glicemia] = set()

    def __init__(self, glicemias: Optional[Set[Glicemia]] = None):
        if not glicemias:
            glicemias = set()

        self.__glicemias = glicemias

    def adicionar(self, glicemia: Glicemia):
        self.__glicemias.add(glicemia)

    def atualizar(self, glicemia: Glicemia):
        return glicemia

    def remover(self, glicemia: Glicemia):
        self.__glicemias.remove(glicemia)

    def consultar_todos(self):
        yield from self.__glicemias

    def consultar_por_id(self, id: UUID):
        return next(glicemia for glicemia in self.__glicemias if glicemia.id == id)


class FakeUOW(AbstractUnitOfWork):
    def __init__(self):
        self.repo = FakeRepo(set())
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_glicemia():
    uow = FakeUOW()

    id_usuario = uuid4()
    horario_dosagem = datetime(2021, 8, 27, 10, 15)

    registros_no_banco = list(uow.repo.consultar_todos())

    assert len(registros_no_banco) == 0

    glicemia_criada = criar_glicemia(
        comando=CriarGlicemia(
            valor=98,
            horario_dosagem=horario_dosagem,
            observacoes="glicose em jejum",
            primeira_do_dia=True,
            criado_por=id_usuario,
        ),
        uow=uow,
    )

    assert uow.committed is True

    registros_no_banco = list(uow.repo.consultar_todos())

    assert len(registros_no_banco) == 1
    assert registros_no_banco[0] == glicemia_criada

    glicemia_esperada = Glicemia(
        valor=98,
        primeira_do_dia=True,
        horario_dosagem=horario_dosagem,
        observacoes="glicose em jejum",
        auditoria=Auditoria(
            criado_por=id_usuario,
            data_criacao=datetime(2021, 8, 27, 16, 20),
            ultima_vez_editado_por=None,
            data_ultima_edicao=None,
            ativo=True,
            deletado=False,
        ),
    )

    assert glicemia_criada.id
    assert glicemia_criada.valor == 98
    assert glicemia_criada.primeira_do_dia is True
    assert glicemia_criada.horario_dosagem == horario_dosagem
    assert glicemia_criada.observacoes == "glicose em jejum"
    assert glicemia_criada.auditoria.criado_por == id_usuario
    assert glicemia_criada.auditoria.data_criacao == datetime.now()


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_editar_glicemia():
    uow = FakeUOW()

    id_usuario = uuid4()

    horario_dosagem = datetime(2021, 8, 27, 10, 15)
    horario_edicao = datetime(2021, 8, 27, 16, 21)

    glicemia_criada = criar_glicemia(
        comando=CriarGlicemia(
            valor=105,
            horario_dosagem=horario_dosagem,
            observacoes="glicose em jejum",
            primeira_do_dia=True,
            criado_por=id_usuario,
        ),
        uow=uow,
    )

    assert uow.committed is True

    with freeze_time(horario_edicao):
        glicemia_editada = editar_glicemia(
            comando=EditarGlicemia(
                glicemia_id=glicemia_criada.id,
                novos_valores=ValoresParaEdicaoDeGlicemia(
                    valor=98,
                    primeira_do_dia=True,
                    horario_dosagem=horario_dosagem,
                    observacoes="teste mano afff",
                ),
                editado_por=id_usuario,
            ),
            uow=uow,
        )

    glicemia_esperada_apos_edicao = Glicemia(
        id=glicemia_criada.id,
        valor=98,
        primeira_do_dia=True,
        horario_dosagem=horario_dosagem,
        observacoes="teste mano afff",
        auditoria=Auditoria(
            criado_por=id_usuario,
            data_criacao=datetime(2021, 8, 27, 16, 20),
            ultima_vez_editado_por=id_usuario,
            data_ultima_edicao=horario_edicao,
            ativo=True,
            deletado=False,
        ),
    )

    assert glicemia_editada == glicemia_esperada_apos_edicao


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_remover_glicemia():
    uow = FakeUOW()

    registros_no_banco = list(uow.repo.consultar_todos())

    assert len(registros_no_banco) == 0

    glicemia_criada = criar_glicemia(
        comando=CriarGlicemia(
            valor=98,
            horario_dosagem=datetime(2021, 8, 27, 10, 15),
            observacoes="glicose em jejum",
            primeira_do_dia=False,
            criado_por=uuid4(),
        ),
        uow=uow,
    )

    assert uow.committed is True

    registros_no_banco = list(uow.repo.consultar_todos())

    assert len(registros_no_banco) == 1
    assert registros_no_banco[0] == glicemia_criada

    id_glicemia_removida = remover_glicemia(
        comando=RemoverGlicemia(glicemia_id=glicemia_criada.id),
        uow=uow,
    )

    assert id_glicemia_removida == glicemia_criada.id

    registros_no_banco = list(uow.repo.consultar_todos())

    assert len(registros_no_banco) == 0
