import pytest

from uuid import uuid4
from datetime import datetime
from freezegun import freeze_time

from contextos.glicemias.dominio.entidades import (
    Glicemia,
    Auditoria,
)
from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_glicemia():
    id_usuario = uuid4()

    hora_atual = datetime.now()
    hora_glicemia = datetime(2021, 8, 27, 8, 15)

    glicemia_esperada = Glicemia(
        valor=120,
        primeira_do_dia=True,
        horario_dosagem=hora_glicemia,
        observacoes="primeira glicemia do dia",
        auditoria=Auditoria(
            criado_por=id_usuario,
            data_criacao=hora_atual,
            ultima_vez_editado_por=None,
            data_ultima_edicao=None,
            ativo=True,
            deletado=False,
        ),
    )

    glicemia_criada = Glicemia.criar(
        valor=120,
        primeira_do_dia=True,
        horario_dosagem=hora_glicemia,
        observacoes="primeira glicemia do dia",
        criado_por=id_usuario,
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


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_glicemia_com_valores_invalidos():
    id_usuario = uuid4()

    with pytest.raises(Glicemia.ValorDeGlicemiaInvalido) as e:
        Glicemia.criar(
            valor=10,
            primeira_do_dia=True,
            horario_dosagem=datetime.now(),
            observacoes="primeira glicemia do dia",
            criado_por=id_usuario,
        )

        assert str(e.value) == "O valor da glicemia deve ser superior a 20mg/dl"


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_editar_glicemia():
    id_usuario = uuid4()

    horario_criacao = datetime(2021, 8, 27, 16, 20)
    horario_edicao = datetime(2021, 8, 27, 16, 21)

    horario_dosagem = datetime(2021, 8, 27, 8, 15)

    glicemia_criada = Glicemia.criar(
        valor=120,
        primeira_do_dia=True,
        horario_dosagem=horario_dosagem,
        observacoes="primeira glicemia do dia",
        criado_por=id_usuario,
    )

    glicemia_esperada_apos_edicao = Glicemia(
        id=glicemia_criada.id,
        valor=88,
        primeira_do_dia=True,
        horario_dosagem=horario_dosagem,
        observacoes="glicose em jejum",
        auditoria=Auditoria(
            criado_por=id_usuario,
            data_criacao=horario_criacao,
            ultima_vez_editado_por=id_usuario,
            data_ultima_edicao=horario_edicao,
            ativo=True,
            deletado=False,
        ),
    )

    with freeze_time(horario_edicao):
        # mudou o valor e a descricao
        glicemia_apos_edicao = glicemia_criada.editar(
            novos_valores=ValoresParaEdicaoDeGlicemia(
                valor=88,
                primeira_do_dia=True,
                horario_dosagem=horario_dosagem,
                observacoes="glicose em jejum",
            ),
            editado_por=id_usuario,
        )

    assert glicemia_apos_edicao == glicemia_esperada_apos_edicao


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_editar_glicemia_com_valores_invalidos():
    id_usuario = uuid4()

    horario_dosagem = datetime(2021, 8, 27, 8, 15)

    glicemia_criada = Glicemia.criar(
        valor=120,
        primeira_do_dia=True,
        horario_dosagem=horario_dosagem,
        observacoes="primeira glicemia do dia",
        criado_por=id_usuario,
    )

    with pytest.raises(Glicemia.ValorDeGlicemiaInvalido) as e:
        glicemia_criada.editar(
            novos_valores=ValoresParaEdicaoDeGlicemia(
                valor=13,
                primeira_do_dia=True,
                horario_dosagem=horario_dosagem,
                observacoes="glicose em jejum",
            ),
            editado_por=id_usuario,
        )

        assert str(e.value) == "O valor da glicemia deve ser superior a 20mg/dl"
