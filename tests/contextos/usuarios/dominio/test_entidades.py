import pytest

from uuid import uuid4
from freezegun import freeze_time
from datetime import datetime, date

from contextos.usuarios.dominio.entidades import (
    Email,
    Usuario,
)


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_tipo_email():
    with pytest.raises(Email.EmailInvalido) as e:
        Email("test")
        assert str(e.value) == "O e-mail fornecido não possui caracteres suficientes"

    with pytest.raises(Email.EmailInvalido) as e:
        Email("tchaguitosgmail.com.br")
        assert str(e.value) == "Você deve fornecer um e-mail válido"


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_usuario():
    horario_atual_utc = datetime.utcnow()

    usuario_esperado = Usuario(
        email=Email("tchaguitos@gmail.com"),
        senha="abc123",
        nome_completo="Thiago Brasil",
        data_de_nascimento=date(1995, 8, 27),
        data_criacao_utc=horario_atual_utc,
    )

    usuario_criado = Usuario.criar(
        email=Email("tchaguitos@gmail.com"),
        senha="abc123",
        nome_completo="Thiago Brasil",
        data_de_nascimento=date(1995, 8, 27),
    )

    assert usuario_criado.id
    assert usuario_criado.email == usuario_esperado.email
    assert usuario_criado.senha == usuario_esperado.senha
    assert usuario_criado.nome_completo == usuario_esperado.nome_completo
    assert usuario_criado.data_de_nascimento == usuario_esperado.data_de_nascimento

    assert usuario_criado.data_criacao_utc == horario_atual_utc
