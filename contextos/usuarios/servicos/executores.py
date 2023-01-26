from typing import Optional

from libs.dominio import Dominio
from libs.tipos_basicos.texto import Email, Senha
from libs.unidade_de_trabalho import UnidadeDeTrabalhoAbstrata

from contextos.usuarios.dominio.agregados import Usuario
from contextos.usuarios.dominio.comandos import (
    CriarUsuario,
    EditarUsuario,
    AutenticarUsuario,
    AlterarEmailDoUsuario,
)
from contextos.usuarios.repositorio.repo_consulta import RepoConsultaUsuarios

from contextos.usuarios.dominio.eventos import EmailAlterado
from contextos.usuarios.adaptadores.jwt import GeradorDeToken, Token
from contextos.usuarios.adaptadores.encriptador import EncriptadorDeSenha
from contextos.usuarios.exceptions import UsuarioNaoEncontrado, ErroNaAutenticacao


def criar_usuario(
    comando: CriarUsuario,
    uow: UnidadeDeTrabalhoAbstrata,
    encriptar_senha: Optional[bool] = True,
) -> Usuario:
    """"""

    uow = uow(Dominio.usuarios)

    with uow:
        repo_consulta: RepoConsultaUsuarios = uow.repo_consulta

        ja_existe_usuario_com_o_email = repo_consulta.consultar_por_email(
            email=Email(comando.email)
        )

        if ja_existe_usuario_com_o_email:
            raise Usuario.UsuarioInvalido(
                "Não é possível criar um novo usuário com este e-mail."
            )

        senha = comando.senha

        if encriptar_senha:
            senha = EncriptadorDeSenha().encriptar_senha(senha=comando.senha)

        novo_usuario = Usuario.criar(
            email=Email(comando.email),
            senha=Senha(senha),
            nome_completo=comando.nome_completo,
            data_de_nascimento=comando.data_de_nascimento,
        )

        uow.repo_dominio.adicionar(novo_usuario)
        uow.commit()

    return novo_usuario


def editar_usuario(comando: EditarUsuario, uow: UnidadeDeTrabalhoAbstrata) -> Usuario:
    """"""

    uow = uow(Dominio.usuarios)

    with uow:
        repo_consulta: RepoConsultaUsuarios = uow.repo_consulta
        usuario: Usuario = repo_consulta.consultar_por_id(id_usuario=comando.usuario_id)

        usuario_editado = usuario.editar(valores_para_edicao=comando.novos_valores)

        uow.repo_dominio.atualizar(usuario_editado)
        uow.commit()

    return usuario_editado


def autenticar_usuario(
    comando: AutenticarUsuario, uow: UnidadeDeTrabalhoAbstrata
) -> Token:

    uow = uow(Dominio.usuarios)

    with uow:
        repo_consulta: RepoConsultaUsuarios = uow.repo_consulta
        usuario: Usuario = repo_consulta.consultar_por_email(email=comando.email)

        if not usuario:
            raise UsuarioNaoEncontrado("Usuário não encontrado")

        encriptador = EncriptadorDeSenha()
        senha_eh_valida = encriptador.verificar_senha(
            senha_para_verificar=comando.senha,
            senha_do_usuario=usuario.senha,
        )

        if not senha_eh_valida:
            raise ErroNaAutenticacao("Usuário ou senha incorretos")

        return GeradorDeToken.gerar_token(usuario=usuario)


def alterar_email_do_usuario(
    comando: AlterarEmailDoUsuario, uow: UnidadeDeTrabalhoAbstrata
) -> Usuario:
    with uow(Dominio.usuarios):
        usuario: Usuario = uow.repo_consulta.consultar_por_email(
            email=Email(comando.novo_email)
        )

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


def enviar_email_de_confirmacao(evento: EmailAlterado, uow: UnidadeDeTrabalhoAbstrata):
    print(f"==== ENVIOU O E-MAIL PARA {evento.novo_email} ====")
