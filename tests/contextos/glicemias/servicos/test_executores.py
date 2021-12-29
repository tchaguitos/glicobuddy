from uuid import UUID
from uuid import uuid4
from datetime import datetime
from typing import Set, Optional
from freezegun import freeze_time

from contextos.glicemias.dominio.entidades import Glicemia

from contextos.glicemias.dominio.entidades import Auditoria, Glicemia
from contextos.glicemias.dominio.comandos import CriarGlicemia, EditarGlicemia
from contextos.glicemias.servicos.executores import criar_glicemia, editar_glicemia
from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia

from contextos.glicemias.repositorio.repo_dominio import AbstractRepository


# TODO: transformar em fixture ou algo do tipo
class FakeSession:
    commited = False

    def commit(self):
        self.commited = True

class FakeRepo(AbstractRepository):
    __glicemias: Set[Glicemia] = set()

    def __init__(self, glicemias: Optional[Set[Glicemia]] = None):
        if not glicemias:
            glicemias = set()

        self.__glicemias = glicemias

    def adicionar(self, glicemia: Glicemia):
        self.__glicemias.add(glicemia)

    def remover(self, glicemia: Glicemia):
        self.__glicemias.remove(glicemia)

    def consultar_todos(self):
        yield from self.__glicemias

    def consultar_por_id(self, glicemia_id: UUID):
        yield from next(
            glicemia for glicemia in self.__glicemias if glicemia.id == glicemia_id
        )


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_glicemia():
    repo = FakeRepo()
    id_usuario = uuid4()

    horario_dosagem = datetime(2021, 8, 27, 10, 15)

    comando = CriarGlicemia(
        valor=98,
        horario_dosagem=horario_dosagem,
        observacoes="glicose em jejum",
        primeira_do_dia=True,
        criado_por=id_usuario,
    )

    registros_no_banco = list(repo.consultar_todos())
    assert len(registros_no_banco) == 0

    glicemia_criada = criar_glicemia(
        comando=comando,
        repo=repo,
        session=FakeSession(),
    )

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
    assert glicemia_criada.valor == glicemia_esperada.valor
    assert glicemia_criada.primeira_do_dia == glicemia_esperada.primeira_do_dia
    assert glicemia_criada.horario_dosagem == glicemia_esperada.horario_dosagem
    assert glicemia_criada.observacoes == glicemia_esperada.observacoes
    assert (
        glicemia_criada.auditoria.criado_por == glicemia_esperada.auditoria.criado_por
    )
    assert (
        glicemia_criada.auditoria.data_criacao
        == glicemia_esperada.auditoria.data_criacao
    )

    registros_no_banco = list(repo.consultar_todos())

    assert len(registros_no_banco) == 1
    assert registros_no_banco[0] == glicemia_criada


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_editar_glicemia():
    id_usuario = uuid4()

    horario_dosagem = datetime(2021, 8, 27, 10, 15)
    horario_edicao = datetime(2021, 8, 27, 16, 21)

    comando = CriarGlicemia(
        valor=105,
        horario_dosagem=horario_dosagem,
        observacoes="glicose em jejum",
        primeira_do_dia=True,
        criado_por=id_usuario,
    )

    glicemia_criada = criar_glicemia(
        comando=comando,
        repo=FakeRepo(),
        session=FakeSession(),
    )

    with freeze_time(horario_edicao):
        glicemia_editada = editar_glicemia(
            comando=EditarGlicemia(
                glicemia=glicemia_criada,
                novos_valores=ValoresParaEdicaoDeGlicemia(
                    valor=98,
                    primeira_do_dia=True,
                    horario_dosagem=horario_dosagem,
                    observacoes="teste mano afff",
                ),
                editado_por=id_usuario,
            ),
            repo=FakeRepo(),
            session=FakeSession(),
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
