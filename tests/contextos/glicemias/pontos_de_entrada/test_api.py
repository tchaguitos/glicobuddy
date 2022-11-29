import pytest
from uuid import uuid4
from fastapi.testclient import TestClient

from freezegun import freeze_time
from datetime import datetime, timedelta

from contextos.glicemias.dominio.entidades import Glicemia

from main import app

client = TestClient(app)


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_consultar_glicemias(session, usuario_autenticado):
    horario_dosagem = datetime.now()

    glicemia_a_criar = [
        {
            "valor": 108,
            "observacoes": "poxa ein teste de integracao nao",
            "primeira_do_dia": True,
            "horario_dosagem": str(horario_dosagem + timedelta(hours=2)),
        },
        {
            "valor": 98,
            "observacoes": "",
            "primeira_do_dia": False,
            "horario_dosagem": str(horario_dosagem + timedelta(hours=2)),
        },
    ]

    headers = {"Authorization": f"Bearer {usuario_autenticado}"}

    for glicemia in glicemia_a_criar:
        response = client.post(
            "/v1/glicemias",
            json=glicemia,
            headers=headers,
        )

    response = client.get(
        "/v1/glicemias",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json().get("glicemias")) == 2

    client.post(
        "/v1/glicemias",
        json={
            "valor": 129,
            "observacoes": "",
            "primeira_do_dia": False,
            "horario_dosagem": str(horario_dosagem + timedelta(hours=4)),
        },
        headers=headers,
    )

    response = client.get(
        "/v1/glicemias",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json().get("glicemias")) == 3


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_consultar_glicemias_por_id(session, usuario_autenticado):
    horario_dosagem = datetime.now()

    headers = {"Authorization": f"Bearer {usuario_autenticado}"}

    response = client.post(
        "/v1/glicemias",
        json={
            "valor": 129,
            "observacoes": "pós prandial",
            "primeira_do_dia": False,
            "horario_dosagem": str(horario_dosagem + timedelta(hours=4)),
        },
        headers=headers,
    )

    glicemia_id = response.json().get("id")

    response = client.get(
        f"/v1/glicemias/{glicemia_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json().get("glicemias")) == 1

    glicemia = response.json().get("glicemias")[0]

    assert glicemia.get("id") == glicemia_id
    assert glicemia.get("valor") == 129
    assert glicemia.get("observacoes") == "pós prandial"
    assert glicemia.get("primeira_do_dia") == False
    assert (
        glicemia.get("horario_dosagem")
        == (horario_dosagem + timedelta(hours=4)).isoformat()
    )

    response = client.get(
        f"/v1/glicemias/{uuid4()}",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json().get("detail") == "Não existe glicemia com o ID informado"


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_glicemia(session, usuario_autenticado):
    horario_dosagem = datetime.now()

    glicemia_a_ser_criada = {
        "valor": 108,
        "observacoes": "poxa ein teste de integracao nao",
        "primeira_do_dia": True,
        "horario_dosagem": str(horario_dosagem),
    }

    headers = {"Authorization": f"Bearer {usuario_autenticado}"}

    response = client.post(
        "/v1/glicemias",
        json=glicemia_a_ser_criada,
        headers=headers,
    )

    assert "id" in response.json()
    assert response.status_code == 201


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_editar_glicemia(session, usuario_autenticado):
    horario_dosagem = datetime.now()

    glicemia_a_ser_criada = {
        "valor": 108,
        "observacoes": "poxa ein teste de integracao nao",
        "primeira_do_dia": True,
        "horario_dosagem": str(horario_dosagem),
    }

    headers = {"Authorization": f"Bearer {usuario_autenticado}"}

    response = client.post(
        "/v1/glicemias",
        json=glicemia_a_ser_criada,
        headers=headers,
    )

    assert "id" in response.json()
    assert response.status_code == 201

    valores_para_edicao_de_glicemia = {
        "valor": 95,
        "observacoes": "errei mano",
        "primeira_do_dia": False,
        "horario_dosagem": str(horario_dosagem),
    }

    glicemia_id = response.json().get("id")
    response = client.patch(
        f"/v1/glicemias/{glicemia_id}",
        json=valores_para_edicao_de_glicemia,
        headers=headers,
    )

    assert "id" in response.json()
    assert response.status_code == 200

    valores_para_edicao_de_glicemia = {
        "valor": 13,
        "observacoes": "nao vai dar certo",
        "primeira_do_dia": False,
        "horario_dosagem": str(horario_dosagem),
    }

    response = client.patch(
        f"/v1/glicemias/{glicemia_id}",
        json=valores_para_edicao_de_glicemia,
        headers=headers,
    )

    assert (
        response.json().get("detail")
        == "O valor da glicemia deve ser superior a 20mg/dl"
    )


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_remover_glicemia(session, usuario_autenticado):
    horario_dosagem = datetime.now()

    glicemia_a_ser_criada = {
        "valor": 108,
        "observacoes": "poxa ein teste de integracao nao",
        "primeira_do_dia": True,
        "horario_dosagem": str(horario_dosagem),
    }

    headers = {"Authorization": f"Bearer {usuario_autenticado}"}

    response = client.post(
        "/v1/glicemias",
        json=glicemia_a_ser_criada,
        headers=headers,
    )

    assert "id" in response.json()
    assert response.status_code == 201

    glicemia_id = response.json().get("id")
    response = client.delete(
        f"/v1/glicemias/{glicemia_id}",
        headers=headers,
    )

    assert "id" in response.json()
    assert response.status_code == 200
