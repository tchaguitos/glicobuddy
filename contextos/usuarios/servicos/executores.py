from typing import Optional

from libs.dominio import Dominio
from libs.tipos_basicos.texto import Email, Senha
from libs.unidade_de_trabalho import AbstractUnitOfWork

from contextos.usuarios.exceptions import UsuarioNaoEncontrado

from contextos.usuarios.dominio.entidades import Usuario
from contextos.usuarios.dominio.comandos import (
    CriarUsuario,
    EditarUsuario,
    AutenticarUsuario,
    AlterarEmailDoUsuario,
)
from contextos.usuarios.adaptadores.encriptador import EncriptadorDeSenha


def criar_usuario(
    comando: CriarUsuario,
    uow: AbstractUnitOfWork,
    encriptador: Optional[EncriptadorDeSenha] = None,
) -> Usuario:
    with uow(Dominio.usuarios):
        ja_existe_usuario_com_o_email = uow.repo_consulta.consultar_por_email(
            email=Email(comando.email)
        )

        if ja_existe_usuario_com_o_email:
            raise Usuario.UsuarioInvalido(
                "Não é possível criar um novo usuário com este e-mail."
            )

        senha = comando.senha

        if encriptador:
            senha = encriptador.encriptar_senha(senha=comando.senha)
            senha = Senha(senha.decode())

        novo_usuario = Usuario.criar(
            email=Email(comando.email),
            senha=senha,
            nome_completo=comando.nome_completo,
            data_de_nascimento=comando.data_de_nascimento,
        )

        uow.repo_dominio.adicionar(novo_usuario)
        uow.commit()

    return novo_usuario


def editar_usuario(comando: EditarUsuario, uow: AbstractUnitOfWork) -> Usuario:
    with uow(Dominio.usuarios):
        usuario: Usuario = uow.repo_consulta.consultar_por_id(
            id_usuario=comando.usuario_id
        )

        usuario_editado = usuario.editar(valores_para_edicao=comando.novos_valores)

        uow.repo_dominio.atualizar(usuario_editado)
        uow.commit()

    return usuario_editado


def autenticar_usuario(comando: AutenticarUsuario, uow: AbstractUnitOfWork) -> Usuario:
    with uow(Dominio.usuarios):
        usuario: Usuario = uow.repo_consulta.consultar_por_email(email=comando.email)

        if not usuario:
            raise UsuarioNaoEncontrado("Usuário não encontrado")

        encriptador = EncriptadorDeSenha()

        senha_eh_valida = encriptador.verificar_senha(
            senha_para_verificar=comando.senha,
            senha_do_usuario=usuario.senha,
        )

        # TODO: gerar e retornar o token jwt?

        return senha_eh_valida


def alterar_email_do_usuario(
    comando: AlterarEmailDoUsuario, uow: AbstractUnitOfWork
) -> Usuario:
    with uow(Dominio.usuarios):
        usuario = uow.repo_consulta.consultar_por_email(email=Email(comando.novo_email))

        # email ja utilizado por usuario com id diferente
        if usuario and usuario.id != comando.usuario_id:
            raise Usuario.UsuarioInvalido(
                "Não é possível criar um novo usuário com este e-mail."
            )

        if not usuario:
            usuario = uow.repo_consulta.consultar_por_id(id_usuario=comando.usuario_id)

        usuario_alterado = usuario.alterar_email(email=Email(comando.novo_email))

        uow.repo_dominio.atualizar(usuario_alterado)
        uow.commit()

    return usuario_alterado
