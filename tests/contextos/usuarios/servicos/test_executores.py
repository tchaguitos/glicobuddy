import pytest

from typing import Set, Optional
from freezegun import freeze_time
from datetime import datetime, date

from libs.unidade_de_trabalho import AbstractUnitOfWork
from libs.repositorio import RepositorioDominio, RepositorioConsulta

from libs.tipos_basicos.texto import Email, Senha, Nome
from libs.tipos_basicos.identificadores_db import IdUsuario

from contextos.usuarios.dominio.entidades import Usuario
from contextos.usuarios.dominio.comandos import (
    CriarUsuario,
    EditarUsuario,
    AutenticarUsuario,
    AlterarEmailDoUsuario,
)
from contextos.usuarios.servicos.executores import (
    criar_usuario,
    editar_usuario,
    autenticar_usuario,
    alterar_email_do_usuario,
)
from contextos.usuarios.dominio.objetos_de_valor import ValoresParaEdicaoDeUsuario

from contextos.usuarios.adaptadores.encriptador import EncriptadorDeSenha


class FakeRepo(RepositorioDominio, RepositorioConsulta):
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

    def consultar_por_id(self, id_usuario: IdUsuario):
        return next(usuario for usuario in self.__usuarios if usuario.id == id_usuario)

    def consultar_por_email(self, email: str):
        return next(
            (usuario for usuario in self.__usuarios if usuario.email == email), None
        )


class FakeUOW(AbstractUnitOfWork):
    def __init__(self):
        repo = FakeRepo(set())

        self.repo_dominio = repo
        self.repo_consulta = repo

        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_usuario():
    uow = FakeUOW()

    registros_no_banco = list(uow.repo_consulta.consultar_todos())

    assert len(registros_no_banco) == 0

    usuario_criado = criar_usuario(
        comando=CriarUsuario(
            email=Email("tchaguitos@gmail.com"),
            senha=Senha("abc123"),
            nome_completo=Nome("Thiago Brasil"),
            data_de_nascimento=date(1995, 8, 27),
        ),
        uow=uow,
    )

    assert uow.committed is True

    registros_no_banco = list(uow.repo_consulta.consultar_todos())

    assert len(registros_no_banco) == 1
    assert registros_no_banco[0] == usuario_criado

    assert usuario_criado.id
    assert usuario_criado.senha == Senha("abc123")


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_usuario_com_senha_encriptada():
    uow = FakeUOW()

    registros_no_banco = list(uow.repo_consulta.consultar_todos())

    assert len(registros_no_banco) == 0

    encriptador = EncriptadorDeSenha()

    usuario_criado = criar_usuario(
        comando=CriarUsuario(
            email=Email("tchaguitos@gmail.com"),
            senha=Senha("abc123"),
            nome_completo=Nome("Thiago Brasil"),
            data_de_nascimento=date(1995, 8, 27),
        ),
        uow=uow,
        encriptador=encriptador,
    )

    assert uow.committed is True

    registros_no_banco = list(uow.repo_consulta.consultar_todos())

    assert len(registros_no_banco) == 1
    assert registros_no_banco[0] == usuario_criado

    assert usuario_criado.id

    senha_eh_valida = encriptador.verificar_senha(
        senha_para_verificar=Senha("abc123"),
        senha_do_usuario=usuario_criado.senha,
    )

    assert senha_eh_valida is True


def test_criar_usuario_com_email_ja_existente():
    uow = FakeUOW()

    criar_usuario(
        comando=CriarUsuario(
            email=Email("tchaguitos@gmail.com"),
            senha=Senha("abc123"),
            nome_completo=Nome("Thiago Brasil"),
            data_de_nascimento=date(1995, 8, 27),
        ),
        uow=uow,
    )

    with pytest.raises(Usuario.UsuarioInvalido) as e:
        criar_usuario(
            comando=CriarUsuario(
                email=Email("tchaguitos@gmail.com"),
                senha=Senha("abc123"),
                nome_completo=Nome("Thiago Brasil"),
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
            senha=Senha("abc123"),
            nome_completo=Nome("Thiago Brasil"),
            data_de_nascimento=date(1995, 8, 27),
        ),
        uow=uow,
    )

    usuario = uow.repo_consulta.consultar_por_id(id_usuario=usuario_criado.id)

    assert usuario.id == usuario_criado.id
    assert usuario.nome_completo == "Thiago Brasil"
    assert usuario.data_de_nascimento == date(1995, 8, 27)

    usuario_editado = editar_usuario(
        comando=EditarUsuario(
            usuario_id=IdUsuario(usuario_criado.id),
            novos_valores=ValoresParaEdicaoDeUsuario(
                nome_completo=Nome("Bill Cypher"),
                data_de_nascimento=date(1985, 9, 15),
            ),
            editado_por=IdUsuario(usuario_criado.id),
        ),
        uow=uow,
    )

    assert usuario_editado.id == usuario_criado.id
    assert usuario_editado.nome_completo == "Bill Cypher"
    assert usuario_editado.data_de_nascimento == date(1985, 9, 15)


@freeze_time(datetime(2037, 8, 26, 4, 20))
def test_autenticar_usuario():
    uow = FakeUOW()

    email = Email("usuario.1@teste.com")
    senha = Senha("abc123")

    criar_usuario(
        comando=CriarUsuario(
            email=email,
            senha=senha,
            nome_completo=Nome("Usuario 1"),
            data_de_nascimento=date(1995, 8, 27),
        ),
        uow=uow,
        encriptador=EncriptadorDeSenha(),
    )

    usuario_autenticado = autenticar_usuario(
        comando=AutenticarUsuario(
            email=email,
            senha=senha,
        ),
        uow=uow,
    )

    assert usuario_autenticado is True

    usuario_autenticado = autenticar_usuario(
        comando=AutenticarUsuario(
            email=email,
            senha=Senha("123abcd"),
        ),
        uow=uow,
    )

    assert usuario_autenticado is False

    usuario_autenticado = autenticar_usuario(
        comando=AutenticarUsuario(
            email=email,
            senha=Senha("senhaaaAaaAa"),
        ),
        uow=uow,
    )

    assert usuario_autenticado is False

    usuario_autenticado = autenticar_usuario(
        comando=AutenticarUsuario(
            email=email,
            senha=Senha("abc123"),
        ),
        uow=uow,
    )

    assert usuario_autenticado is True


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_alterar_email_de_usuario():
    uow = FakeUOW()

    usuario_1 = criar_usuario(
        comando=CriarUsuario(
            email=Email("usuario.1@teste.com"),
            senha=Senha("abc123"),
            nome_completo=Nome("Usuario 1"),
            data_de_nascimento=date(1995, 8, 27),
        ),
        uow=uow,
    )

    usuario_2 = criar_usuario(
        comando=CriarUsuario(
            email=Email("usuario.2@teste.com"),
            senha=Senha("abc123"),
            nome_completo=Nome("Usuario 2"),
            data_de_nascimento=date(1990, 8, 27),
        ),
        uow=uow,
    )

    assert usuario_1.email == Email("usuario.1@teste.com")

    usuario_com_email_alterado = alterar_email_do_usuario(
        comando=AlterarEmailDoUsuario(
            usuario_id=IdUsuario(usuario_1.id),
            novo_email=Email("tchaguitos@gmail.com"),
        ),
        uow=uow,
    )

    assert usuario_1.id == usuario_com_email_alterado.id
    assert usuario_com_email_alterado.email == Email("tchaguitos@gmail.com")

    with pytest.raises(Usuario.UsuarioInvalido) as e:
        usuario_com_email_alterado = alterar_email_do_usuario(
            comando=AlterarEmailDoUsuario(
                usuario_id=IdUsuario(usuario_2.id),
                novo_email=Email("tchaguitos@gmail.com"),
            ),
            uow=uow,
        )

        assert str(e.value) == "Não é possível criar um novo usuário com este e-mail."
