import pytest

from uuid import UUID
from typing import Set, Optional
from freezegun import freeze_time
from datetime import datetime, date

from libs.unidade_de_trabalho import AbstractUnitOfWork
from contextos.usuarios.repositorio.repo_dominio import RepoAbstratoUsuarios

from contextos.usuarios.dominio.agregados import Usuario, Email
from contextos.usuarios.dominio.comandos import (
    CriarUsuario,
    EditarUsuario,
    AlterarEmailDoUsuario,
)
from contextos.usuarios.servicos.executores import (
    criar_usuario,
    editar_usuario,
    alterar_email_do_usuario,
)
from contextos.usuarios.dominio.objetos_de_valor import ValoresParaEdicaoDeUsuario


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


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_editar_usuario():
    uow = FakeUOW()

    usuario_criado = criar_usuario(
        comando=CriarUsuario(
            email=Email("tchaguitos@gmail.com"),
            senha="abc123",
            nome_completo="Thiago Brasil",
            data_de_nascimento=date(1995, 8, 27),
        ),
        uow=uow,
    )

    usuario = uow.repo_dominio.consultar_por_id(id=usuario_criado.id)

    assert usuario.id == usuario_criado.id
    assert usuario.nome_completo == "Thiago Brasil"
    assert usuario.data_de_nascimento == date(1995, 8, 27)

    usuario_editado = editar_usuario(
        comando=EditarUsuario(
            usuario_id=usuario_criado.id,
            novos_valores=ValoresParaEdicaoDeUsuario(
                nome_completo="Bill Cypher", data_de_nascimento=date(1985, 9, 15)
            ),
            editado_por=usuario_criado.id,
        ),
        uow=uow,
    )

    assert usuario_editado.id == usuario_criado.id
    assert usuario_editado.nome_completo == "Bill Cypher"
    assert usuario_editado.data_de_nascimento == date(1985, 9, 15)


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_alterar_email_de_usuario():
    uow = FakeUOW()

    usuario_1 = criar_usuario(
        comando=CriarUsuario(
            email=Email("usuario.1@teste.com"),
            senha="abc123",
            nome_completo="Usuario 1",
            data_de_nascimento=date(1995, 8, 27),
        ),
        uow=uow,
    )

    usuario_2 = criar_usuario(
        comando=CriarUsuario(
            email=Email("usuario.2@teste.com"),
            senha="abc123",
            nome_completo="Usuario 2",
            data_de_nascimento=date(1990, 8, 27),
        ),
        uow=uow,
    )

    assert usuario_1.email == Email("usuario.1@teste.com")

    usuario_com_email_alterado = alterar_email_do_usuario(
        comando=AlterarEmailDoUsuario(
            usuario_id=usuario_1.id,
            novo_email=Email("tchaguitos@gmail.com"),
        ),
        uow=uow,
    )

    assert usuario_1.id == usuario_com_email_alterado.id
    assert usuario_com_email_alterado.email == Email("tchaguitos@gmail.com")

    with pytest.raises(Usuario.UsuarioInvalido) as e:
        usuario_com_email_alterado = alterar_email_do_usuario(
            comando=AlterarEmailDoUsuario(
                usuario_id=usuario_2.id,
                novo_email=Email("tchaguitos@gmail.com"),
            ),
            uow=uow,
        )

        assert str(e.value) == "Não é possível criar um novo usuário com este e-mail."
