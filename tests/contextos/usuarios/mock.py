import pytest
from datetime import date
from typing import Optional
from sqlalchemy.orm import close_all_sessions

from config import get_session_factory

from libs.tipos_basicos.texto import Email, Senha, Nome

from contextos.usuarios.dominio.agregados import Usuario
from contextos.usuarios.adaptadores.jwt import GeradorDeToken, Token
from contextos.usuarios.adaptadores.encriptador import EncriptadorDeSenha
from contextos.usuarios.repositorio.repo_dominio import RepoDominioUsuarios
from contextos.usuarios.repositorio.repo_consulta import RepoConsultaUsuarios


def mock_criar_usuario(
    session,
    email: Optional[Email],
    salvar_no_db: Optional[bool] = False,
) -> Usuario:
    """"""

    repo_consulta = RepoConsultaUsuarios(session)

    if not email:
        email = Email("mock.usuario@teste.com")

    usuario = repo_consulta.consultar_por_email(email=email)

    if usuario:
        return usuario

    senha = EncriptadorDeSenha().encriptar_senha(senha="senha123")
    usuario = Usuario.criar(
        email=email,
        senha=Senha(senha),
        nome_completo=Nome("Mock de usuario"),
        data_de_nascimento=date(1995, 8, 26),
    )

    if salvar_no_db:
        repo_dominio = RepoDominioUsuarios(session)
        repo_dominio.adicionar(usuario)
        session.commit()
        return repo_consulta.consultar_por_email(email=email)

    return usuario


@pytest.fixture(scope="session")
def usuario_salvo():
    session = get_session_factory()

    repo_dominio = RepoDominioUsuarios(session)
    repo_consulta = RepoConsultaUsuarios(session)

    email_de_teste = Email("mock.usuario@teste.com")

    usuario = repo_consulta.consultar_por_email(email=email_de_teste)

    if usuario:
        yield usuario

    senha = EncriptadorDeSenha().encriptar_senha(senha="senha123")
    usuario = Usuario.criar(
        email=email_de_teste,
        senha=Senha(senha),
        nome_completo=Nome("Mock de usuario"),
        data_de_nascimento=date(1995, 8, 26),
    )

    repo_dominio.adicionar(usuario)
    session.commit()

    yield usuario

    close_all_sessions()


@pytest.fixture
def usuario_autenticado(usuario_salvo) -> Token:
    usuario = usuario_salvo
    token = GeradorDeToken.gerar_token(usuario=usuario)

    return token
