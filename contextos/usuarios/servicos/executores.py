from libs.unidade_de_trabalho import AbstractUnitOfWork
from contextos.usuarios.dominio.comandos import CriarUsuario
from contextos.usuarios.dominio.entidades import Usuario, Email

from libs.dominio import Dominio


def criar_usuario(comando: CriarUsuario, uow: AbstractUnitOfWork) -> Usuario:
    with uow(Dominio.usuarios):
        ja_existe_usuario_com_o_email = uow.repo_dominio.consultar_por_email(
            email=Email(comando.email)
        )

        if ja_existe_usuario_com_o_email:
            raise Usuario.UsuarioInvalido(
                "Não é possível criar um novo usuário com este e-mail."
            )

        novo_usuario = Usuario.criar(
            email=Email(comando.email),
            senha=comando.senha,
            nome_completo=comando.nome_completo,
            data_de_nascimento=comando.data_de_nascimento,
        )

        uow.repo_dominio.adicionar(novo_usuario)
        uow.commit()

    return novo_usuario
