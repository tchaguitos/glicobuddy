import pytest

from uuid import uuid4
from datetime import datetime
from freezegun import freeze_time

from libs.tipos_basicos.identificadores_db import IdUsuario, IdGlicemia
from libs.tipos_basicos.numeros import ValorDeGlicemia, ValorDeGlicemiaInvalido

from contextos.glicemias.dominio.entidades import (
    Glicemia,
    Auditoria,
)
from contextos.glicemias.dominio.objetos_de_valor import (
    TipoDeGlicemia,
    ValoresParaEdicaoDeGlicemia,
)


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_glicemia():
    id_usuario = uuid4()

    hora_atual = datetime.now()
    hora_glicemia = datetime(2021, 8, 27, 8, 15)

    glicemia_esperada = Glicemia(
        valor=ValorDeGlicemia(120),
        tipo=TipoDeGlicemia("jejum"),
        horario_dosagem=hora_glicemia,
        observacoes="primeira glicemia do dia",
        auditoria=Auditoria(
            criado_por=IdUsuario(id_usuario),
            data_criacao=hora_atual,
            ultima_vez_editado_por=None,
            data_ultima_edicao=None,
        ),
    )

    glicemia_criada = Glicemia.criar(
        valor=ValorDeGlicemia(120),
        tipo=TipoDeGlicemia("jejum"),
        horario_dosagem=hora_glicemia,
        observacoes="primeira glicemia do dia",
        criado_por=IdUsuario(id_usuario),
    )

    assert glicemia_criada.id
    assert glicemia_criada.valor == glicemia_esperada.valor
    assert glicemia_criada.tipo == glicemia_esperada.tipo
    assert glicemia_criada.horario_dosagem == glicemia_esperada.horario_dosagem
    assert glicemia_criada.observacoes == glicemia_esperada.observacoes
    assert (
        glicemia_criada.auditoria.criado_por == glicemia_esperada.auditoria.criado_por
    )
    assert (
        glicemia_criada.auditoria.data_criacao
        == glicemia_esperada.auditoria.data_criacao
    )


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_glicemia_com_valores_invalidos():
    id_usuario = uuid4()

    with pytest.raises(ValorDeGlicemiaInvalido) as e:
        Glicemia.criar(
            valor=ValorDeGlicemia(10),
            tipo=TipoDeGlicemia.jejum,
            horario_dosagem=datetime.now(),
            observacoes="primeira glicemia do dia",
            criado_por=IdUsuario(id_usuario),
        )

        assert str(e.value) == "O valor da glicemia deve ser superior a 20mg/dl"


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_editar_glicemia():
    id_usuario = uuid4()

    horario_edicao = datetime(2021, 8, 27, 16, 21)

    horario_dosagem = datetime(2021, 8, 27, 8, 15)

    glicemia_criada = Glicemia.criar(
        valor=ValorDeGlicemia(120),
        tipo=TipoDeGlicemia.jejum,
        horario_dosagem=horario_dosagem,
        observacoes="primeira glicemia do dia",
        criado_por=IdUsuario(id_usuario),
    )

    assert glicemia_criada.id
    assert glicemia_criada.valor == 120
    assert glicemia_criada.observacoes == "primeira glicemia do dia"

    assert glicemia_criada.auditoria.ultima_vez_editado_por is None
    assert glicemia_criada.auditoria.data_ultima_edicao is None

    with freeze_time(horario_edicao):
        glicemia_editada = glicemia_criada.editar(
            novos_valores=ValoresParaEdicaoDeGlicemia(
                valor=ValorDeGlicemia(88),
                tipo=TipoDeGlicemia.jejum,
                horario_dosagem=horario_dosagem,
                observacoes="glicose em jejum",
            ),
            editado_por=IdUsuario(id_usuario),
        )

    assert glicemia_editada.valor == 88
    assert glicemia_editada.id == glicemia_criada.id
    assert glicemia_editada.observacoes == "glicose em jejum"

    assert glicemia_editada.auditoria.ultima_vez_editado_por == id_usuario
    assert glicemia_editada.auditoria.data_ultima_edicao == horario_edicao

    # TODO: add mais casos


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_editar_glicemia_com_valores_invalidos():
    id_usuario = uuid4()

    horario_dosagem = datetime(2021, 8, 27, 8, 15)

    glicemia_criada = Glicemia.criar(
        valor=ValorDeGlicemia(120),
        tipo=TipoDeGlicemia.pos_prandial,
        horario_dosagem=horario_dosagem,
        observacoes="primeira glicemia do dia",
        criado_por=IdUsuario(id_usuario),
    )

    with pytest.raises(ValorDeGlicemiaInvalido) as e:
        glicemia_criada.editar(
            novos_valores=ValoresParaEdicaoDeGlicemia(
                valor=ValorDeGlicemia(13),
                tipo=TipoDeGlicemia.pos_prandial,
                horario_dosagem=horario_dosagem,
                observacoes="glicose em jejum",
            ),
            editado_por=IdUsuario(id_usuario),
        )

        assert str(e.value) == "O valor da glicemia deve ser superior a 20mg/dl"
