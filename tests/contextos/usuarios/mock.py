import pytest

from datetime import date

from config import get_session_factory

from libs.tipos_basicos.texto import Email, Senha, Nome

from contextos.usuarios.dominio.agregados import Usuario
from contextos.usuarios.adaptadores.jwt import GeradorDeToken, Token
from contextos.usuarios.adaptadores.encriptador import EncriptadorDeSenha
from contextos.usuarios.repositorio.repo_dominio import RepoDominioUsuarios


@pytest.fixture
def usuario_salvo():
    session = get_session_factory()
    repo = RepoDominioUsuarios(session)

    senha = EncriptadorDeSenha().encriptar_senha(senha="senha123")
    usuario = Usuario.criar(
        email=Email("mock.usuario@teste.com"),
        senha=Senha(senha.decode()),
        nome_completo=Nome("Mock de usuario"),
        data_de_nascimento=date(1995, 8, 26),
    )

    repo.adicionar(usuario)
    session.commit()

    return usuario


@pytest.fixture
def usuario_autenticado(usuario_salvo) -> Token:
    usuario = usuario_salvo
    token = GeradorDeToken.gerar_token(usuario=usuario)

    return token
