import pytest

from uuid import uuid4
from fastapi.testclient import TestClient

from freezegun import freeze_time
from datetime import datetime, date

from contextos.glicemias.dominio.entidades import Glicemia

from main import app

client = TestClient(app)


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_usuario(session):
    data_de_nascimento = date(1995, 8, 27)

    usuario_a_ser_criado = {
        "email": "nome.completo@teste.com",
        "senha": "senha123",
        "nome_completo": "Nome completo",
        "data_de_nascimento": str(data_de_nascimento),
    }

    response = client.post(
        "/v1/usuarios",
        json=usuario_a_ser_criado,
    )

    assert "id" in response.json()
    assert response.status_code == 201
