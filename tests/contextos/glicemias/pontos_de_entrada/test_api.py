from datetime import datetime
from freezegun import freeze_time
from fastapi.testclient import TestClient

from contextos.glicemias.pontos_de_entrada.api import app

from contextos.glicemias.dominio.entidades import Glicemia

client = TestClient(app)


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_glicemia(session):
    horario_dosagem = datetime.now()

    glicemia_a_ser_criada = {
        "valor": 108,
        "observacoes": "poxa ein teste de integracao nao",
        "primeira_do_dia": True,
        "horario_dosagem": str(horario_dosagem),
    }
    
    response = client.post(
        "/v1/glicemias",
        json=glicemia_a_ser_criada,
    )

    assert "id" in response.json()
    assert response.status_code == 201
