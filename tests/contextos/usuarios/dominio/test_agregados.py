import pytest

from freezegun import freeze_time
from datetime import datetime, date

from libs.tipos_basicos.texto import Email, Senha, Nome, EmailInvalido

from contextos.usuarios.dominio.agregados import Usuario
from contextos.usuarios.dominio.objetos_de_valor import (
    ValoresParaEdicaoDeUsuario,
)
from contextos.usuarios.dominio.eventos import EmailAlterado


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_tipo_email():
    with pytest.raises(EmailInvalido) as e:
        Email("test")
        assert str(e.value) == "O e-mail fornecido não possui caracteres suficientes"

    with pytest.raises(EmailInvalido) as e:
        Email("tchaguitosgmail.com.br")
        assert str(e.value) == "Você deve fornecer um e-mail válido"

    email_como_texto = "tchaguitos@gmail.com"

    email = Email(email_como_texto)
    assert str(email) == email_como_texto


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_usuario():
    horario_atual_utc = datetime.utcnow()

    usuario_esperado = Usuario(
        email=Email("tchaguitos@gmail.com"),
        senha=Senha("abc123"),
        nome_completo=Nome("Thiago Brasil"),
        data_de_nascimento=date(1995, 8, 27),
        data_criacao_utc=horario_atual_utc,
    )

    usuario_criado = Usuario.criar(
        email=Email("tchaguitos@gmail.com"),
        senha=Senha("abc123"),
        nome_completo=Nome("Thiago Brasil"),
        data_de_nascimento=date(1995, 8, 27),
    )

    assert usuario_criado.id
    assert usuario_criado.email == usuario_esperado.email
    assert usuario_criado.senha == usuario_esperado.senha
    assert usuario_criado.nome_completo == usuario_esperado.nome_completo
    assert usuario_criado.data_de_nascimento == usuario_esperado.data_de_nascimento

    assert usuario_criado.data_criacao_utc == horario_atual_utc


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_editar_usuario():
    usuario = Usuario.criar(
        email=Email("tchaguitos@gmail.com"),
        senha=Senha("abc123"),
        nome_completo=Nome("Thiago Brasil"),
        data_de_nascimento=date(1995, 8, 27),
    )

    assert usuario.nome_completo == "Thiago Brasil"
    assert usuario.data_de_nascimento == date(1995, 8, 27)

    usuario_editado = usuario.editar(
        valores_para_edicao=ValoresParaEdicaoDeUsuario(
            nome_completo=Nome("Teste AAAAA"),
            data_de_nascimento=date(1960, 8, 27),
        )
    )

    assert usuario_editado
    assert usuario_editado.nome_completo == "Teste AAAAA"
    assert usuario_editado.data_de_nascimento == date(1960, 8, 27)


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_alterar_email_usuario():
    usuario = Usuario.criar(
        email=Email("tchaguitos@teste.com"),
        senha=Senha("abc123"),
        nome_completo=Nome("Thiago Brasil"),
        data_de_nascimento=date(1995, 8, 27),
    )

    assert usuario.email == Email("tchaguitos@teste.com")

    assert usuario.eventos == []
    assert len(usuario.eventos) == 0

    usuario = usuario.alterar_email(
        email=Email("tchaguitos@gmail.com"),
    )

    assert len(usuario.eventos) == 1
    assert usuario.eventos == [
        EmailAlterado(
            usuario_id=usuario.id,
            novo_email=Email("tchaguitos@gmail.com"),
        )
    ]

    assert usuario.email == Email("tchaguitos@gmail.com")
