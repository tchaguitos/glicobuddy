from uuid import uuid4
from datetime import datetime
from freezegun import freeze_time

from contextos.glicemias.dominio.entidades import Auditoria, Glicemia
from contextos.glicemias.dominio.comandos import CriarGlicemia, EditarGlicemia
from contextos.glicemias.servicos.executores import criar_glicemia, editar_glicemia
from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_glicemia():
    id_usuario = uuid4()

    horario_dosagem = datetime(2021, 8, 27, 10, 15)

    comando = CriarGlicemia(
        valor=98,
        horario_dosagem=horario_dosagem,
        observacoes="glicose em jejum",
        primeira_do_dia=True,
        criado_por=id_usuario,
    )

    glicemia_criada = criar_glicemia(comando=comando)

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

    glicemia_criada = criar_glicemia(comando=comando)

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
            )
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
