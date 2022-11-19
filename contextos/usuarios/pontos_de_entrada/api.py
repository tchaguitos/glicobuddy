from fastapi import APIRouter, HTTPException

from libs.unidade_de_trabalho import SqlAlchemyUnitOfWork

from libs.tipos_basicos.texto import Nome, Email, Senha
from libs.tipos_basicos.identificadores_db import IdUsuario

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

from contextos.usuarios.servicos.visualizadores import consultar_usuario_por_id

from contextos.usuarios.adaptadores.encriptador import EncriptadorDeSenha
from contextos.usuarios.dominio.objetos_de_valor import ValoresParaEdicaoDeUsuario

from contextos.usuarios.pontos_de_entrada.serializadores import (
    SerializadorDeUsuario,
    RetornoDaAutenticacao,
    RetornoDaAPIDeUsuarios,
    SerializadorParaEdicaoDeUsuario,
    SerializadorParaAlteracaoDeEmail,
    SerializadorParaCriacaoDeUsuario,
    SerializadorParaAutenticarUsuario,
)

router = APIRouter(
    tags=["usuários"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/v1/usuarios/login",
    status_code=200,
    response_model=RetornoDaAutenticacao,
)
def login(
    dados_para_login: SerializadorParaAutenticarUsuario,
):

    uow = SqlAlchemyUnitOfWork()

    try:
        token_gerado = autenticar_usuario(
            comando=AutenticarUsuario(
                email=Email(dados_para_login.email),
                senha=Senha(dados_para_login.senha),
            ),
            uow=uow,
        )

        return RetornoDaAutenticacao(
            access_token=token_gerado,
            token_type="jwt",
        )

    except Exception:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")


@router.post(
    "/v1/usuarios",
    status_code=201,
    response_model=RetornoDaAPIDeUsuarios,
)
def cadastrar_usuario(
    novo_usuario: SerializadorParaCriacaoDeUsuario,
):

    uow = SqlAlchemyUnitOfWork()

    usuario_criado = criar_usuario(
        comando=CriarUsuario(
            email=Email(novo_usuario.email),
            senha=Senha(novo_usuario.senha),
            nome_completo=Nome(novo_usuario.nome_completo),
            data_de_nascimento=novo_usuario.data_de_nascimento,
        ),
        uow=uow,
        encriptador=EncriptadorDeSenha(),
    )

    return RetornoDaAPIDeUsuarios(id=usuario_criado.id)


@router.patch(
    "/v1/usuarios/{usuario_id}",
    status_code=200,
    response_model=RetornoDaAPIDeUsuarios,
)
def atualizar_usuario(
    usuario_id: IdUsuario, novos_valores: SerializadorParaEdicaoDeUsuario
):
    uow = SqlAlchemyUnitOfWork()

    usuario_editado = editar_usuario(
        comando=EditarUsuario(
            usuario_id=IdUsuario(usuario_id),
            novos_valores=ValoresParaEdicaoDeUsuario(
                nome_completo=Nome(novos_valores.nome_completo),
                data_de_nascimento=novos_valores.data_de_nascimento,
            ),
            editado_por=IdUsuario(usuario_id),
        ),
        uow=uow,
    )

    return RetornoDaAPIDeUsuarios(id=usuario_editado.id)


@router.patch(
    "/v1/usuarios/{usuario_id}/alterar-email",
    status_code=200,
    response_model=RetornoDaAPIDeUsuarios,
)
def atualizar_email_do_usuario(
    usuario_id: IdUsuario, novos_valores: SerializadorParaAlteracaoDeEmail
):
    uow = SqlAlchemyUnitOfWork()

    usuario_com_email_alterado = alterar_email_do_usuario(
        comando=AlterarEmailDoUsuario(
            usuario_id=IdUsuario(usuario_id),
            novo_email=Email(novos_valores.novo_email),
        ),
        uow=uow,
    )

    return RetornoDaAPIDeUsuarios(id=usuario_com_email_alterado.id)


@router.get(
    "/v1/usuarios/{usuario_id}",
    status_code=200,
    response_model=SerializadorDeUsuario,
)
def consultar_usuarios_por_id(usuario_id: IdUsuario):
    uow = SqlAlchemyUnitOfWork()

    usuario = consultar_usuario_por_id(
        uow=uow,
        usuario_id=usuario_id,
    )

    if not usuario:
        raise HTTPException(
            status_code=404, detail="Não existe usuario com o ID informado"
        )

    return SerializadorDeUsuario(
        id=usuario.id,
        email=usuario.email,
        nome_completo=usuario.nome_completo,
        data_de_nascimento=usuario.data_de_nascimento,
    )
