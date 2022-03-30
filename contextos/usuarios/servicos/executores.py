from libs.unidade_de_trabalho import AbstractUnitOfWork
from contextos.usuarios.dominio.entidades import Usuario, Email
from contextos.usuarios.dominio.comandos import (
    CriarUsuario,
    EditarUsuario,
    AlterarEmailDoUsuario,
)

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


def editar_usuario(comando: EditarUsuario, uow: AbstractUnitOfWork) -> Usuario:
    with uow(Dominio.usuarios):
        usuario: Usuario = uow.repo_dominio.consultar_por_id(id=comando.usuario_id)

        usuario_editado = usuario.editar(valores_para_edicao=comando.novos_valores)

        uow.repo_dominio.atualizar(usuario_editado)
        uow.commit()

    return usuario_editado


def alterar_email_do_usuario(
    comando: AlterarEmailDoUsuario, uow: AbstractUnitOfWork
) -> Usuario:
    with uow(Dominio.usuarios):
        usuario = uow.repo_dominio.consultar_por_email(email=Email(comando.novo_email))

        # email ja utilizado por usuario com id diferente
        if usuario and usuario.id != comando.usuario_id:
            raise Usuario.UsuarioInvalido(
                "Não é possível criar um novo usuário com este e-mail."
            )

        if not usuario:
            usuario = uow.repo_dominio.consultar_por_id(id=comando.usuario_id)

        usuario_alterado = usuario.alterar_email(email=Email(comando.novo_email))

    return usuario_alterado
