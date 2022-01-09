from uuid import uuid4
from datetime import datetime
from freezegun import freeze_time

from contextos.glicemias.dominio.entidades import Glicemia

from contextos.glicemias.repositorio import repo_dominio


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_adicionar_glicemia(session):
    # TODO: criar forma melhor de limpar o db para os testes
    session.execute("DELETE FROM glicemia")

    repo = repo_dominio.SqlAlchemyRepository(session)

    glicemia = Glicemia.criar(
        valor=120,
        primeira_do_dia=True,
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="primeira glicemia do dia",
        criado_por=uuid4(),
    )

    repo.adicionar(glicemia)
    session.commit()

    rows = session.execute("SELECT * FROM glicemia")

    registros = list(rows)

    assert len(registros) == 1
    assert registros[0].id == glicemia.id


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_remover_glicemia(session):
    session.execute("DELETE FROM glicemia")

    repo = repo_dominio.SqlAlchemyRepository(session)

    glicemia = Glicemia.criar(
        valor=120,
        primeira_do_dia=True,
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="primeira glicemia do dia",
        criado_por=uuid4(),
    )

    repo.adicionar(glicemia)
    session.commit()

    rows = session.execute("SELECT * FROM glicemia")

    assert len(list(rows)) == 1

    repo.remover(glicemia)
    session.commit()

    rows = session.execute("SELECT * FROM glicemia")

    assert len(list(rows)) == 0


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_consultar_glicemias(session):
    session.execute("DELETE FROM glicemia")

    repo = repo_dominio.SqlAlchemyRepository(session)

    glicemia_1 = Glicemia.criar(
        valor=120,
        primeira_do_dia=True,
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="primeira glicemia do dia",
        criado_por=uuid4(),
    )

    repo.adicionar(glicemia_1)
    session.commit()

    registros_no_banco = repo.consultar_todos()

    assert len(registros_no_banco) == 1

    glicemia_2 = Glicemia.criar(
        valor=87,
        primeira_do_dia=True,
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="teste bro",
        criado_por=uuid4(),
    )

    glicemia_3 = Glicemia.criar(
        valor=95,
        primeira_do_dia=True,
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="somos apenas objetos efêmeros que morrem depois que o teste acaba",
        criado_por=uuid4(),
    )

    repo.adicionar(glicemia_2)
    repo.adicionar(glicemia_3)
    session.commit()

    registros_no_banco = repo.consultar_todos()

    assert len(registros_no_banco) == 3


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_consultar_glicemia_por_id(session):
    session.execute("DELETE FROM glicemia")

    repo = repo_dominio.SqlAlchemyRepository(session)

    glicemia_criada = Glicemia.criar(
        valor=120,
        primeira_do_dia=True,
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="primeira glicemia do dia",
        criado_por=uuid4(),
    )

    repo.adicionar(glicemia_criada)
    session.commit()

    glicemia_salva_no_banco = repo.consultar_por_id(id=glicemia_criada.id)

    assert glicemia_criada == glicemia_salva_no_banco
