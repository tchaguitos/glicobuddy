from freezegun import freeze_time
from datetime import datetime, date

from libs.tipos_basicos.texto import Email, Senha, Nome

from contextos.usuarios.dominio.entidades import Usuario
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

    assert payload == {
        "id": str(usuario.id),
        "email": usuario.email,
        "nome_completo": usuario.nome_completo,
        "data_de_nascimento": usuario.data_de_nascimento.strftime("%d/%m/%Y"),
    }
