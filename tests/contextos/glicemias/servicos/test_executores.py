from uuid import UUID
from uuid import uuid4
from datetime import datetime
from typing import Set, Optional
from freezegun import freeze_time

from libs.unidade_de_trabalho import UnidadeDeTrabalhoAbstrata
from libs.repositorio import RepositorioDominio, RepositorioConsulta
from libs.tipos_basicos.identificadores_db import IdUsuario, IdGlicemia

from contextos.glicemias.dominio.entidades import Glicemia

from contextos.glicemias.dominio.entidades import Glicemia
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


class FakeRepo(RepositorioDominio, RepositorioConsulta):
    __glicemias: Set[Glicemia]

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

    def consultar_por_id(self, id: IdGlicemia):
        return next(glicemia for glicemia in self.__glicemias if glicemia.id == id)


class FakeUOW(UnidadeDeTrabalhoAbstrata):
    def __init__(self):
        repo = FakeRepo(set())

        self.repo_dominio = repo
        self.repo_consulta = repo

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

    registros_no_banco = list(uow.repo_consulta.consultar_todos())

    assert len(registros_no_banco) == 0

    glicemia_criada = criar_glicemia(
        comando=CriarGlicemia(
            valor=98,
            horario_dosagem=horario_dosagem,
            observacoes="glicose em jejum",
            primeira_do_dia=True,
            criado_por=IdUsuario(id_usuario),
        ),
        uow=uow,
    )

    assert uow.committed is True

    registros_no_banco = list(uow.repo_consulta.consultar_todos())

    assert len(registros_no_banco) == 1
    assert registros_no_banco[0] == glicemia_criada

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
            criado_por=IdUsuario(id_usuario),
        ),
        uow=uow,
    )

    assert uow.committed is True

    registros_no_banco = list(uow.repo_consulta.consultar_todos())

    assert len(registros_no_banco) == 1

    assert glicemia_criada.valor == 105
    assert glicemia_criada.observacoes == "glicose em jejum"

    assert glicemia_criada.auditoria.ultima_vez_editado_por is None
    assert glicemia_criada.auditoria.data_ultima_edicao is None

    with freeze_time(horario_edicao):
        glicemia_editada = editar_glicemia(
            comando=EditarGlicemia(
                glicemia_id=IdGlicemia(glicemia_criada.id),
                novos_valores=ValoresParaEdicaoDeGlicemia(
                    valor=98,
                    primeira_do_dia=True,
                    horario_dosagem=horario_dosagem,
                    observacoes="teste mano afff",
                ),
                editado_por=IdUsuario(id_usuario),
            ),
            uow=uow,
        )

    assert glicemia_editada.valor == 98
    assert glicemia_editada.observacoes == "teste mano afff"

    assert glicemia_editada.auditoria.ultima_vez_editado_por == id_usuario
    assert glicemia_editada.auditoria.data_ultima_edicao == horario_edicao

    registros_no_banco = list(uow.repo_consulta.consultar_todos())

    assert len(registros_no_banco) == 1


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_remover_glicemia():
    uow = FakeUOW()

    registros_no_banco = list(uow.repo_consulta.consultar_todos())

    assert len(registros_no_banco) == 0

    glicemia_criada = criar_glicemia(
        comando=CriarGlicemia(
            valor=98,
            horario_dosagem=datetime(2021, 8, 27, 10, 15),
            observacoes="glicose em jejum",
            primeira_do_dia=False,
            criado_por=IdUsuario(uuid4()),
        ),
        uow=uow,
    )

    assert uow.committed is True

    registros_no_banco = list(uow.repo_consulta.consultar_todos())

    assert len(registros_no_banco) == 1
    assert registros_no_banco[0] == glicemia_criada

    id_glicemia_removida = remover_glicemia(
        comando=RemoverGlicemia(
            glicemia_id=IdGlicemia(glicemia_criada.id),
        ),
        uow=uow,
    )

    assert id_glicemia_removida == glicemia_criada.id

    registros_no_banco = list(uow.repo_consulta.consultar_todos())

    assert len(registros_no_banco) == 0
