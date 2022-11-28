import pytest

from freezegun import freeze_time
from datetime import datetime, date, timedelta

from libs.tipos_basicos.texto import Email, Senha, Nome

from contextos.usuarios.dominio.agregados import Usuario
from contextos.usuarios.adaptadores.jwt import GeradorDeToken


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_gerador_de_token():
    usuario = Usuario(
        email=Email("tchaguitos@gmail.com"),
        senha=Senha("abc123"),
        nome_completo=Nome("Thiago Brasil"),
        data_de_nascimento=date(1995, 8, 27),
        data_criacao_utc=datetime.utcnow(),
    )

    token = GeradorDeToken.gerar_token(usuario=usuario)

    assert token

    payload = GeradorDeToken.verificar_token(token=token)

    assert all([valor for valor in payload.values()])


@freeze_time(datetime(2021, 8, 27, 4, 20))
def test_token_expirado():
    usuario = Usuario(
        email=Email("tchaguitos@gmail.com"),
        senha=Senha("abc123"),
        nome_completo=Nome("Thiago Brasil"),
        data_de_nascimento=date(1995, 8, 27),
        data_criacao_utc=datetime.utcnow(),
    )

    # time travel is the concept of movement between certain points in time
    with freeze_time(datetime.now() - timedelta(days=3)):
        token = GeradorDeToken.gerar_token(usuario=usuario)

    with pytest.raises(GeradorDeToken.TokenExpirado) as e:
        GeradorDeToken.verificar_token(token=token)
        assert str(e.value) == "O token utilizado expirou. Faça login novamente"
