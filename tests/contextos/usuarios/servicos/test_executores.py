import pytest

from uuid import UUID
from uuid import uuid4
from typing import Set, Optional
from freezegun import freeze_time
from datetime import datetime, date

from libs.unidade_de_trabalho import AbstractUnitOfWork
from contextos.usuarios.repositorio.repo_dominio import RepoAbstratoUsuarios

from contextos.usuarios.dominio.comandos import CriarUsuario
from contextos.usuarios.dominio.entidades import Usuario, Email
from contextos.usuarios.servicos.executores import criar_usuario


class FakeRepo(RepoAbstratoUsuarios):
    __usuarios: Set[Usuario]

    def __init__(self, usuarios: Optional[Set[Usuario]] = None):
        if not usuarios:
            usuarios = set()

        self.__usuarios = usuarios

    def adicionar(self, usuario: Usuario):
        self.__usuarios.add(usuario)

    def atualizar(self, usuario: Usuario):
        return usuario

    def remover(self, usuario: Usuario):
        self.__usuarios.remove(usuario)

    def consultar_todos(self):
        yield from self.__usuarios

    def consultar_por_id(self, id: UUID):
        return next(usuario for usuario in self.__usuarios if usuario.id == id)

    def consultar_por_email(self, email: str):
        return next(
            (usuario for usuario in self.__usuarios if usuario.email == email), None
        )


class FakeUOW(AbstractUnitOfWork):
    def __init__(self):
        self.repo_dominio = FakeRepo(set())
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_usuario():
    uow = FakeUOW()

    registros_no_banco = list(uow.repo_dominio.consultar_todos())

    assert len(registros_no_banco) == 0

    usuario_criado = criar_usuario(
        comando=CriarUsuario(
            email=Email("tchaguitos@gmail.com"),
            senha="abc123",
            nome_completo="Thiago Brasil",
            data_de_nascimento=date(1995, 8, 27),
        ),
        uow=uow,
    )

    assert uow.committed is True

    registros_no_banco = list(uow.repo_dominio.consultar_todos())

    assert len(registros_no_banco) == 1
    assert registros_no_banco[0] == usuario_criado

    assert usuario_criado.id


def test_criar_usuario_com_email_ja_existente():
    uow = FakeUOW()

    criar_usuario(
        comando=CriarUsuario(
            email=Email("tchaguitos@gmail.com"),
            senha="abc123",
            nome_completo="Thiago Brasil",
            data_de_nascimento=date(1995, 8, 27),
        ),
        uow=uow,
    )

    with pytest.raises(Usuario.UsuarioInvalido) as e:
        criar_usuario(
            comando=CriarUsuario(
                email=Email("tchaguitos@gmail.com"),
                senha="abc123",
                nome_completo="Thiago Brasil",
                data_de_nascimento=date(1995, 8, 27),
            ),
            uow=uow,
        )

        assert str(e.value) == "Não é possível criar um novo usuário com este e-mail."
