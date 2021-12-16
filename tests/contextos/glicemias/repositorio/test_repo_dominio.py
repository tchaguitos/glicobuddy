import pytest

from uuid import uuid4
from datetime import datetime
from freezegun import freeze_time

from contextos.glicemias.dominio.entidades import Glicemia
from contextos.glicemias.repositorio import repo_dominio


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_salvar_glicemia(session):
    id_usuario = uuid4()

    hora_glicemia = datetime(2021, 8, 27, 8, 15)

    glicemia = Glicemia.criar(
        valor=120,
        primeira_do_dia=True,
        horario_dosagem=hora_glicemia,
        observacoes="primeira glicemia do dia",
        criado_por=id_usuario,
    )

    repo = repo_dominio.SqlAlchemyRepository(session)

    repo.add(glicemia)
    session.commit()

    rows = session.execute(
        "SELECT * FROM glicemia"
    )

    assert len(list(rows)) == 1
