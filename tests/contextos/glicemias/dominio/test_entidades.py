from datetime import datetime
from freezegun import freeze_time

from contextos.glicemias.dominio.entidades.glicemias import (
    Glicemia,
)


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_nova_glicemia():
    glicemia_esperada = Glicemia(
        valor=120,
        jejum=True,
        data=datetime.now(),
        observacoes="primeira glicemia do dia",
    )

    glicemia_criada = Glicemia.criar_nova(
        valor=120,
        jejum=True,
        data=datetime.now(),
        observacoes="primeira glicemia do dia",
    )

    assert glicemia_criada == glicemia_esperada
