from datetime import datetime
from freezegun import freeze_time

from libs.tipos_basicos.texto import Email
from libs.tipos_basicos.numeros import ValorDeGlicemia
from libs.tipos_basicos.identificadores_db import IdUsuario

from contextos.glicemias.dominio.entidades import Glicemia

from contextos.glicemias.dominio.objetos_de_valor import TipoDeGlicemia
from contextos.glicemias.repositorio.repo_dominio import RepoDominioGlicemias
from contextos.glicemias.repositorio.repo_consulta import RepoConsultaGlicemias

from tests.contextos.usuarios.mock import mock_criar_usuario


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_consultar_glicemias(session, usuario_salvo):
    session.execute("DELETE FROM glicemia")

    usuario = usuario_salvo

    repo_dominio = RepoDominioGlicemias(session)
    repo_consulta = RepoConsultaGlicemias(session)

    glicemia_1 = Glicemia.criar(
        valor=ValorDeGlicemia(120),
        tipo=TipoDeGlicemia.jejum,
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="primeira glicemia do dia",
        criado_por=IdUsuario(usuario.id),
    )

    repo_dominio.adicionar(glicemia_1)
    session.commit()

    registros_no_banco = repo_consulta.consultar_todos()

    assert len(registros_no_banco) == 1

    glicemia_2 = Glicemia.criar(
        tipo=TipoDeGlicemia.jejum,
        valor=ValorDeGlicemia(87),
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="teste bro",
        criado_por=IdUsuario(usuario.id),
    )

    glicemia_3 = Glicemia.criar(
        tipo=TipoDeGlicemia.jejum,
        valor=ValorDeGlicemia(95),
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="somos apenas objetos efêmeros que morrem depois que o teste acaba",
        criado_por=IdUsuario(usuario.id),
    )

    repo_dominio.adicionar(glicemia_2)
    repo_dominio.adicionar(glicemia_3)
    session.commit()

    registros_no_banco = repo_consulta.consultar_todos()

    assert len(registros_no_banco) == 3

    session.execute("DELETE FROM glicemia")


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_consultar_glicemia_por_id(session, usuario_salvo):
    repo_dominio = RepoDominioGlicemias(session)
    repo_consulta = RepoConsultaGlicemias(session)

    glicemia_criada = Glicemia.criar(
        tipo=TipoDeGlicemia.jejum,
        valor=ValorDeGlicemia(120),
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="primeira glicemia do dia",
        criado_por=IdUsuario(usuario_salvo.id),
    )

    repo_dominio.adicionar(glicemia_criada)
    session.commit()

    glicemia_salva_no_banco = repo_consulta.consultar_por_id(id=glicemia_criada.id)

    assert glicemia_criada == glicemia_salva_no_banco

    session.execute("DELETE FROM glicemia")


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_consultar_glicemia_por_usuario(session, usuario_salvo):
    usuario = usuario_salvo

    repo_dominio = RepoDominioGlicemias(session)
    repo_consulta = RepoConsultaGlicemias(session)

    glicemia_1 = Glicemia.criar(
        tipo=TipoDeGlicemia.jejum,
        valor=ValorDeGlicemia(120),
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="primeira glicemia do dia",
        criado_por=usuario.id,
    )

    glicemia_2 = Glicemia.criar(
        tipo=TipoDeGlicemia.jejum,
        valor=ValorDeGlicemia(98),
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="antes do almoço",
        criado_por=usuario.id,
    )

    outro_usuario = mock_criar_usuario(
        email=Email("outro.usuario@teste.com"),
        session=session,
        salvar_no_db=True,
    )

    glicemia_3 = Glicemia.criar(
        tipo=TipoDeGlicemia.jejum,
        valor=ValorDeGlicemia(120),
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="glicemia",
        criado_por=IdUsuario(outro_usuario.id),
    )

    repo_dominio.adicionar(glicemia_1)
    repo_dominio.adicionar(glicemia_2)
    repo_dominio.adicionar(glicemia_3)

    session.commit()

    glicemias_do_usuario = list(
        repo_consulta.consultar_por_usuario(id_usuario=usuario.id)
    )

    assert glicemias_do_usuario
    assert len(glicemias_do_usuario) == 2
    assert glicemia_3 not in glicemias_do_usuario
