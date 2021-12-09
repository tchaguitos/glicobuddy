import pytest

from uuid import uuid4
from datetime import datetime
from freezegun import freeze_time

from contextos.glicemias.dominio.entidades import (
    Glicemia,
    Auditoria,
    ValorDeGlicemiaInvalido,
)


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

    assert glicemia_criada == glicemia_esperada


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_glicemia_com_valores_invalidos():
    id_usuario = uuid4()

    with pytest.raises(ValorDeGlicemiaInvalido) as e:
        Glicemia.criar(
            valor=10,
            primeira_do_dia=True,
            horario_dosagem=datetime.now(),
            observacoes="primeira glicemia do dia",
            criado_por=id_usuario,
        )

        assert str(e.value) == "O valor da glicemia deve ser superior a 20mg/dl"
