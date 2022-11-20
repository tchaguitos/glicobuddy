from uuid import uuid4
from datetime import datetime
from freezegun import freeze_time

from libs.tipos_basicos.identificadores_db import IdUsuario

from contextos.glicemias.dominio.entidades import Glicemia

from contextos.glicemias.repositorio.repo_dominio import RepoDominioGlicemias
from contextos.glicemias.repositorio.repo_consulta import RepoConsultaGlicemias


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_consultar_glicemias(session):
    session.execute("DELETE FROM glicemia")

    repo_dominio = RepoDominioGlicemias(session)
    repo_consulta = RepoConsultaGlicemias(session)

    glicemia_1 = Glicemia.criar(
        valor=120,
        primeira_do_dia=True,
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="primeira glicemia do dia",
        criado_por=IdUsuario(uuid4()),
    )

    repo_dominio.adicionar(glicemia_1)
    session.commit()

    registros_no_banco = repo_consulta.consultar_todos()

    assert len(registros_no_banco) == 1

    glicemia_2 = Glicemia.criar(
        valor=87,
        primeira_do_dia=True,
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="teste bro",
        criado_por=IdUsuario(uuid4()),
    )

    glicemia_3 = Glicemia.criar(
        valor=95,
        primeira_do_dia=True,
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="somos apenas objetos efêmeros que morrem depois que o teste acaba",
        criado_por=IdUsuario(uuid4()),
    )

    repo_dominio.adicionar(glicemia_2)
    repo_dominio.adicionar(glicemia_3)
    session.commit()

    registros_no_banco = repo_consulta.consultar_todos()

    assert len(registros_no_banco) == 3


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_consultar_glicemia_por_id(session):
    session.execute("DELETE FROM glicemia")

    repo_dominio = RepoDominioGlicemias(session)
    repo_consulta = RepoConsultaGlicemias(session)

    glicemia_criada = Glicemia.criar(
        valor=120,
        primeira_do_dia=True,
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="primeira glicemia do dia",
        criado_por=IdUsuario(uuid4()),
    )

    repo_dominio.adicionar(glicemia_criada)
    session.commit()

    glicemia_salva_no_banco = repo_consulta.consultar_por_id(id=glicemia_criada.id)

    assert glicemia_criada == glicemia_salva_no_banco
