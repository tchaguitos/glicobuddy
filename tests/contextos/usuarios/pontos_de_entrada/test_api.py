import pytest

from uuid import uuid4
from fastapi.testclient import TestClient

from freezegun import freeze_time
from datetime import datetime, date

from contextos.usuarios.dominio.entidades import Email, Usuario

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


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_editar_usuario(session):
    data_de_nascimento = date(1995, 8, 27)

    usuario_a_ser_criado = {
        "email": "nome.completo@teste.com.br",
        "senha": "senha123",
        "nome_completo": "Nome completo",
        "data_de_nascimento": str(data_de_nascimento),
    }

    response = client.post(
        "/v1/usuarios",
        json=usuario_a_ser_criado,
    )

    usuario_id = response.json().get("id")

    response = client.patch(
        f"/v1/usuarios/{usuario_id}",
        json={
            "nome_completo": "Nome do meio completo",
            "data_de_nascimento": str(date(1960, 8, 27)),
        },
    )

    assert "id" in response.json()
    assert response.status_code == 200


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_consultar_usuarios_por_id(session):
    data_de_nascimento = date(1995, 8, 27)

    response = client.post(
        "/v1/usuarios",
        json={
            "email": "thiago.brasil@teste.com",
            "senha": "senha123",
            "nome_completo": "Thiago Brasil",
            "data_de_nascimento": str(data_de_nascimento),
        },
    )

    usuario_id = response.json().get("id")

    response = client.get(f"/v1/usuarios/{usuario_id}")

    assert response.json() == {
        "id": str(usuario_id),
        "nome_completo": "Thiago Brasil",
        "email": "thiago.brasil@teste.com",
        "data_de_nascimento": str(data_de_nascimento),
    }

    response = client.get(f"/v1/usuarios/{uuid4()}")

    assert response.status_code == 404
    assert response.json().get("detail") == "Não existe usuario com o ID informado"
