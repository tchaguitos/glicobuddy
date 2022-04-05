from uuid import uuid4
from datetime import datetime
from freezegun import freeze_time

from contextos.glicemias.dominio.entidades import Glicemia

from contextos.glicemias.repositorio.repo_dominio import RepoDominioGlicemias


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_adicionar_glicemia(session):
    # TODO: criar forma melhor de limpar o db para os testes
    session.execute("DELETE FROM glicemia")

    repo = RepoDominioGlicemias(session)

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

    repo = RepoDominioGlicemias(session)

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
