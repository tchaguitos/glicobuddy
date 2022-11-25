from fastapi import APIRouter, HTTPException, Depends

from libs.unidade_de_trabalho import SqlAlchemyUnitOfWork

from libs.tipos_basicos.texto import Nome, Email, Senha
from libs.tipos_basicos.identificadores_db import IdUsuario

from libs.pontos_de_entrada import retornar_usuario_logado

from contextos.usuarios.dominio.comandos import (
    CriarUsuario,
    EditarUsuario,
    AutenticarUsuario,
    AlterarEmailDoUsuario,
)

from contextos.usuarios.servicos.visualizadores import consultar_usuario_por_id
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

from contextos import barramento

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
    bus = barramento.bootstrap(uow=uow)

    try:
        token_gerado = bus.tratar_mensagem(
            mensagem=AutenticarUsuario(
                email=Email(dados_para_login.email),
                senha=Senha(dados_para_login.senha),
            )
        )

        return RetornoDaAutenticacao(
            access_token=token_gerado,
            token_type="bearer",
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
    bus = barramento.bootstrap(uow=uow)

    try:
        usuario_criado = bus.tratar_mensagem(
            mensagem=CriarUsuario(
                email=Email(novo_usuario.email),
                senha=Senha(novo_usuario.senha),
                nome_completo=Nome(novo_usuario.nome_completo),
                data_de_nascimento=novo_usuario.data_de_nascimento,
            ),
        )

        return RetornoDaAPIDeUsuarios(id=usuario_criado.id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar o usuário",
        )


@router.patch(
    "/v1/usuarios/{usuario_id}",
    status_code=200,
    response_model=RetornoDaAPIDeUsuarios,
)
def atualizar_usuario(
    novos_valores: SerializadorParaEdicaoDeUsuario,
    usuario_logado: SerializadorDeUsuario = Depends(retornar_usuario_logado),
):
    uow = SqlAlchemyUnitOfWork()
    bus = barramento.bootstrap(uow=uow)

    usuario_editado = bus.tratar_mensagem(
        mensagem=EditarUsuario(
            usuario_id=IdUsuario(usuario_logado.id),
            novos_valores=ValoresParaEdicaoDeUsuario(
                nome_completo=Nome(novos_valores.nome_completo),
                data_de_nascimento=novos_valores.data_de_nascimento,
            ),
            editado_por=IdUsuario(usuario_logado.id),
        ),
    )

    return RetornoDaAPIDeUsuarios(id=usuario_editado.id)


@router.patch(
    "/v1/usuarios/{usuario_id}/alterar-email",
    status_code=200,
    response_model=RetornoDaAPIDeUsuarios,
)
def atualizar_email_do_usuario(
    novos_valores: SerializadorParaAlteracaoDeEmail,
    usuario_logado: SerializadorDeUsuario = Depends(retornar_usuario_logado),
):
    uow = SqlAlchemyUnitOfWork()
    bus = barramento.bootstrap(uow=uow)

    try:
        usuario_com_email_alterado = bus.tratar_mensagem(
            mensagem=AlterarEmailDoUsuario(
                usuario_id=IdUsuario(usuario_logado.id),
                novo_email=Email(novos_valores.novo_email),
            ),
        )

        return RetornoDaAPIDeUsuarios(id=usuario_com_email_alterado.id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível alterar o e-mail do usuário",
        )


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


@router.get("/v1/perfil", response_model=SerializadorDeUsuario)
def consultar_usuario_logado(
    usuario_logado: SerializadorDeUsuario = Depends(retornar_usuario_logado),
):
    return usuario_logado
