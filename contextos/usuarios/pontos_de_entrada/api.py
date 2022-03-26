from uuid import UUID
from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel, Extra

from libs.unidade_de_trabalho import SqlAlchemyUnitOfWork

from contextos.usuarios.dominio.entidades import Email
from contextos.usuarios.dominio.comandos import CriarUsuario
from contextos.usuarios.servicos.executores import criar_usuario

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


class RetornoDeUsuariosAPI(BaseModel):
    id: UUID


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
