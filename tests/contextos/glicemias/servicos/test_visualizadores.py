from uuid import UUID
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Set, Optional
from freezegun import freeze_time

from libs.tipos_basicos.numeros import ValorDeGlicemia
from libs.unidade_de_trabalho import UnidadeDeTrabalhoAbstrata
from libs.repositorio import RepositorioDominio, RepositorioConsulta
from libs.tipos_basicos.identificadores_db import IdUsuario

from contextos.glicemias.dominio.entidades import Glicemia, Auditoria
from contextos.glicemias.dominio.objetos_de_valor import TipoDeGlicemia
from contextos.glicemias.servicos.visualizadores import (
    consultar_glicemias,
    consultar_glicemia_por_id,
)


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

    def consultar_por_usuario(self, id_usuario: IdUsuario):
        return [
            glicemia
            for glicemia in self.__glicemias
            if glicemia.auditoria.criado_por == id_usuario
        ]

    def consultar_por_id(self, id: UUID):
        return next(
            (glicemia for glicemia in self.__glicemias if glicemia.id == id), None
        )


class FakeUOW(UnidadeDeTrabalhoAbstrata):
    usuario: Optional[IdUsuario] = None

    def __init__(self, usuario: Optional[IdUsuario] = None):
        repo = FakeRepo(set())

        self.repo_dominio = repo
        self.repo_consulta = repo

        self.committed = False
        self.usuario = usuario

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_consultar_glicemias():
    usuario_id = IdUsuario(uuid4())
    uow = FakeUOW(usuario=usuario_id)

    horario_dosagem_1 = datetime(2021, 8, 27, 10, 15)
    horario_dosagem_2 = horario_dosagem_1 + timedelta(hours=2)
    horario_dosagem_3 = horario_dosagem_2 + timedelta(hours=4)

    glicemias_esperadas = [
        Glicemia(
            valor=ValorDeGlicemia(103),
            tipo=TipoDeGlicemia.pre_prandial,
            horario_dosagem=horario_dosagem_1,
            observacoes="glicose em jejum",
            auditoria=Auditoria(
                criado_por=usuario_id,
                data_criacao=datetime.now(),
                ultima_vez_editado_por=None,
                data_ultima_edicao=None,
            ),
        ),
        Glicemia(
            valor=ValorDeGlicemia(98),
            tipo=TipoDeGlicemia.pre_prandial,
            horario_dosagem=horario_dosagem_2,
            observacoes="depois do café da manhã",
            auditoria=Auditoria(
                criado_por=usuario_id,
                data_criacao=datetime.now() + timedelta(hours=2),
                ultima_vez_editado_por=None,
                data_ultima_edicao=None,
            ),
        ),
    ]

    for glicemia in glicemias_esperadas:
        uow.repo_dominio.adicionar(glicemia)

    glicemias = list(consultar_glicemias(uow=uow))

    assert len(glicemias) == 2

    assert glicemias_esperadas[0] in glicemias
    assert glicemias_esperadas[1] in glicemias

    nova_glicemia = Glicemia(
        valor=ValorDeGlicemia(115),
        tipo=TipoDeGlicemia.pre_prandial,
        horario_dosagem=horario_dosagem_3,
        observacoes="pré almoço",
        auditoria=Auditoria(
            criado_por=usuario_id,
            data_criacao=datetime.now() + timedelta(hours=4),
            ultima_vez_editado_por=None,
            data_ultima_edicao=None,
        ),
    )
    uow.repo_dominio.adicionar(nova_glicemia)

    glicemias = list(consultar_glicemias(uow=uow))

    assert len(glicemias) == 3
    assert nova_glicemia in glicemias

    glicemia_de_outro_usuario = Glicemia(
        valor=ValorDeGlicemia(119),
        tipo=TipoDeGlicemia.pre_prandial,
        horario_dosagem=horario_dosagem_3,
        observacoes="pré almoço",
        auditoria=Auditoria(
            criado_por=IdUsuario(uuid4()),  # outro usuario. nao deve ser retornada
            data_criacao=datetime.now() + timedelta(hours=4),
            ultima_vez_editado_por=None,
            data_ultima_edicao=None,
        ),
    )
    uow.repo_dominio.adicionar(glicemia_de_outro_usuario)

    assert len(glicemias) == 3
    assert glicemia_de_outro_usuario not in glicemias


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_consultar_glicemia_por_id():
    uow = FakeUOW()
    usuario_id = uuid4()

    horario_dosagem_1 = datetime(2021, 8, 27, 10, 15)
    horario_dosagem_2 = horario_dosagem_1 + timedelta(hours=2)
    horario_dosagem_3 = horario_dosagem_2 + timedelta(hours=4)

    glicemias_esperadas = [
        Glicemia(
            valor=ValorDeGlicemia(103),
            tipo=TipoDeGlicemia.pre_prandial,
            horario_dosagem=horario_dosagem_1,
            observacoes="glicose em jejum",
            auditoria=Auditoria(
                criado_por=IdUsuario(usuario_id),
                data_criacao=datetime.now(),
                ultima_vez_editado_por=None,
                data_ultima_edicao=None,
            ),
        ),
        Glicemia(
            valor=ValorDeGlicemia(98),
            tipo=TipoDeGlicemia.pre_prandial,
            horario_dosagem=horario_dosagem_2,
            observacoes="depois do café da manhã",
            auditoria=Auditoria(
                criado_por=IdUsuario(usuario_id),
                data_criacao=datetime.now() + timedelta(hours=2),
                ultima_vez_editado_por=None,
                data_ultima_edicao=None,
            ),
        ),
        Glicemia(
            valor=ValorDeGlicemia(115),
            tipo=TipoDeGlicemia.pos_prandial,
            horario_dosagem=horario_dosagem_3,
            observacoes="pré almoço",
            auditoria=Auditoria(
                criado_por=IdUsuario(usuario_id),
                data_criacao=datetime.now() + timedelta(hours=4),
                ultima_vez_editado_por=None,
                data_ultima_edicao=None,
            ),
        ),
    ]

    for glicemia in glicemias_esperadas:
        uow.repo_dominio.adicionar(glicemia)

    glicemia_esperada = glicemias_esperadas[0]

    glicemia = consultar_glicemia_por_id(
        glicemia_id=glicemia_esperada.id,
        uow=uow,
    )

    assert glicemia == glicemia_esperada

    glicemia_esperada = glicemias_esperadas[1]

    glicemia = consultar_glicemia_por_id(
        glicemia_id=glicemia_esperada.id,
        uow=uow,
    )

    assert glicemia == glicemia_esperada
