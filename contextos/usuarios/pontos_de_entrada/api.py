from uuid import UUID
from datetime import date
from pydantic import BaseModel, Extra
from fastapi import APIRouter, HTTPException

from libs.unidade_de_trabalho import SqlAlchemyUnitOfWork

from contextos.usuarios.dominio.entidades import Email
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

from contextos.usuarios.servicos.visualizadores import consultar_usuario_por_id

router = APIRouter(
    tags=["usuários"],
    responses={404: {"description": "Not found"}},
)


class ValoresParaCriacaoDeUsuarioAPI(BaseModel):
    email: Email
    senha: str
    nome_completo: str
    data_de_nascimento: date

    class Config:
        extra = Extra.forbid


class ValoresParaEdicaoDeUsuarioAPI(BaseModel):
    nome_completo: str
    data_de_nascimento: date

    class Config:
        extra = Extra.forbid


class ValoresParaAlteracaoDeEmailAPI(BaseModel):
    novo_email: Email

    class Config:
        extra = Extra.forbid


class RetornoDeUsuariosAPI(BaseModel):
    id: UUID


class UsuarioAPI(BaseModel):
    id: UUID
    email: Email
    nome_completo: str
    data_de_nascimento: date


@router.post(
    "/v1/usuarios",
    status_code=201,
    response_model=RetornoDeUsuariosAPI,
)
def cadastrar_usuario(
    novo_usuario: ValoresParaCriacaoDeUsuarioAPI,
):

    uow = SqlAlchemyUnitOfWork()

    usuario_criado = criar_usuario(
        comando=CriarUsuario(
            email=Email(novo_usuario.email),
            senha=novo_usuario.senha,
            nome_completo=novo_usuario.nome_completo,
            data_de_nascimento=novo_usuario.data_de_nascimento,
        ),
        uow=uow,
    )

    return RetornoDeUsuariosAPI(id=usuario_criado.id)


@router.patch(
    "/v1/usuarios/{usuario_id}",
    status_code=200,
    response_model=RetornoDeUsuariosAPI,
)
def atualizar_usuario(usuario_id: UUID, novos_valores: ValoresParaEdicaoDeUsuarioAPI):
    uow = SqlAlchemyUnitOfWork()

    usuario_editado = editar_usuario(
        comando=EditarUsuario(
            usuario_id=usuario_id,
            novos_valores=ValoresParaEdicaoDeUsuario(
                nome_completo=novos_valores.nome_completo,
                data_de_nascimento=novos_valores.data_de_nascimento,
            ),
            editado_por=usuario_id,
        ),
        uow=uow,
    )

    return RetornoDeUsuariosAPI(id=usuario_editado.id)


@router.patch(
    "/v1/usuarios/{usuario_id}/alterar-email",
    status_code=200,
    response_model=RetornoDeUsuariosAPI,
)
def atualizar_email_do_usuario(
    usuario_id: UUID, novos_valores: ValoresParaAlteracaoDeEmailAPI
):
    uow = SqlAlchemyUnitOfWork()

    usuario_com_email_alterado = alterar_email_do_usuario(
        comando=AlterarEmailDoUsuario(
            usuario_id=usuario_id,
            novo_email=Email(novos_valores.novo_email),
        ),
        uow=uow,
    )

    return RetornoDeUsuariosAPI(id=usuario_com_email_alterado.id)


@router.get(
    "/v1/usuarios/{usuario_id}",
    status_code=200,
    response_model=UsuarioAPI,
)
def consultar_usuarios_por_id(usuario_id: UUID):
    uow = SqlAlchemyUnitOfWork()

    usuario = consultar_usuario_por_id(
        uow=uow,
        usuario_id=usuario_id,
    )

    if not usuario:
        raise HTTPException(
            status_code=404, detail="Não existe usuario com o ID informado"
        )

    return UsuarioAPI(
        id=usuario.id,
        email=usuario.email,
        nome_completo=usuario.nome_completo,
        data_de_nascimento=usuario.data_de_nascimento,
    )
