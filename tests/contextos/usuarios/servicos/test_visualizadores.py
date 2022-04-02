from uuid import UUID
from typing import Set, Optional
from freezegun import freeze_time
from datetime import date, datetime

from libs.unidade_de_trabalho import AbstractUnitOfWork

from contextos.usuarios.dominio.agregados import Usuario, Email
from contextos.usuarios.repositorio.repo_dominio import RepoAbstratoUsuarios
from contextos.usuarios.servicos.visualizadores import (
    consultar_usuario_por_id,
    consultar_usuario_por_email,
)


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
        return next((usuario for usuario in self.__usuarios if usuario.id == id), None)

    def consultar_por_email(self, email: Email):
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
def test_consultar_usuario_por_id():
    uow = FakeUOW()

    usuario_criado = Usuario.criar(
        email=Email("tchaguitos@gmail.com"),
        senha="abc123",
        nome_completo="Thiago Brasil",
        data_de_nascimento=date(1995, 8, 27),
    )

    assert usuario_criado.id

    uow.repo_dominio.adicionar(usuario_criado)
    uow.commit()

    usuario = consultar_usuario_por_id(
        uow=uow,
        usuario_id=usuario_criado.id,
    )

    assert usuario == usuario_criado


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_consultar_usuario_por_email():
    uow = FakeUOW()

    usuario_criado = Usuario.criar(
        email=Email("tchaguitos@gmail.com"),
        senha="abc123",
        nome_completo="Thiago Brasil",
        data_de_nascimento=date(1995, 8, 27),
    )

    assert usuario_criado.id

    uow.repo_dominio.adicionar(usuario_criado)
    uow.commit()

    usuario = consultar_usuario_por_email(uow=uow, usuario_email=usuario_criado.email)

    assert usuario == usuario_criado
