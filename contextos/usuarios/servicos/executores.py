from libs.unidade_de_trabalho import AbstractUnitOfWork
from contextos.usuarios.dominio.comandos import CriarUsuario
from contextos.usuarios.dominio.entidades import Usuario, Email


def criar_usuario(comando: CriarUsuario, uow: AbstractUnitOfWork) -> Usuario:
    with uow:
        novo_usuario = Usuario.criar(
            email=Email(comando.email),
            senha=comando.senha,
            nome_completo=comando.nome_completo,
            data_de_nascimento=comando.data_de_nascimento,
        )

        uow.repo.adicionar(novo_usuario)
        uow.commit()

    return novo_usuario
