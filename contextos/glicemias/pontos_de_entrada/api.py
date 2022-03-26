from typing import List
from uuid import UUID, uuid4
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel, Extra
from fastapi import APIRouter, HTTPException

from libs.unidade_de_trabalho import SqlAlchemyUnitOfWork

from contextos.glicemias.dominio.comandos import (
    CriarGlicemia,
    EditarGlicemia,
    RemoverGlicemia,
)
from contextos.glicemias.servicos.executores import (
    criar_glicemia,
    editar_glicemia,
    remover_glicemia,
)
from contextos.glicemias.servicos.visualizadores import (
    consultar_glicemias,
    consultar_glicemia_por_id,
)
from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia

router = APIRouter(
    tags=["glicemias"],
    responses={404: {"description": "Not found"}},
)


class ValoresParaCriacaoDeGlicemiaAPI(BaseModel):
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime

    class Config:
        extra = Extra.forbid


class ValoresParaEdicaoDeGlicemiaAPI(BaseModel):
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime

    class Config:
        extra = Extra.forbid


class RetornoDeGlicemiasAPI(BaseModel):
    id: UUID


class GlicemiaAPI(BaseModel):
    id: UUID
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime


class RetornoDeConsultaGlicemiasAPI(BaseModel):
    glicemias: List[GlicemiaAPI]


@router.get(
    "/v1/glicemias",
    status_code=200,
    response_model=RetornoDeConsultaGlicemiasAPI,
)
def listar_glicemias():
    usuario_id = uuid4()

    uow = SqlAlchemyUnitOfWork()

    glicemias = consultar_glicemias(
        usuario_id=usuario_id,
        uow=uow,
    )

    return RetornoDeConsultaGlicemiasAPI(
        glicemias=[
            GlicemiaAPI(
                id=glicemia.id,
                valor=glicemia.valor,
                observacoes=glicemia.observacoes,
                primeira_do_dia=glicemia.primeira_do_dia,
                horario_dosagem=glicemia.horario_dosagem,
            )
            for glicemia in glicemias
        ]
    )


@router.get(
    "/v1/glicemias/{glicemia_id}",
    status_code=200,
    response_model=RetornoDeConsultaGlicemiasAPI,
)
def consultar_glicemias_por_id(glicemia_id: UUID):
    usuario_id = uuid4()

    uow = SqlAlchemyUnitOfWork()

    glicemia = consultar_glicemia_por_id(
        glicemia_id=glicemia_id,
        usuario_id=usuario_id,
        uow=uow,
    )

    if not glicemia:
        raise HTTPException(
            status_code=404, detail="Não existe glicemia com o ID informado"
        )

    return RetornoDeConsultaGlicemiasAPI(
        glicemias=[
            GlicemiaAPI(
                id=glicemia.id,
                valor=glicemia.valor,
                observacoes=glicemia.observacoes,
                primeira_do_dia=glicemia.primeira_do_dia,
                horario_dosagem=glicemia.horario_dosagem,
            )
        ]
    )


@router.post(
    "/v1/glicemias",
    status_code=201,
    response_model=RetornoDeGlicemiasAPI,
)
def cadastrar_glicemia(
    nova_glicemia: ValoresParaCriacaoDeGlicemiaAPI,
):
    # TODO: receber o usuário por meio da requisicao
    usuario_id = uuid4()

    uow = SqlAlchemyUnitOfWork()

    glicemia_criada = criar_glicemia(
        comando=CriarGlicemia(
            valor=nova_glicemia.valor,
            observacoes=nova_glicemia.observacoes,
            primeira_do_dia=nova_glicemia.primeira_do_dia,
            horario_dosagem=nova_glicemia.horario_dosagem,
            criado_por=usuario_id,
        ),
        uow=uow,
    )

    return RetornoDeGlicemiasAPI(id=glicemia_criada.id)


@router.patch(
    "/v1/glicemias/{glicemia_id}",
    status_code=200,
    response_model=RetornoDeGlicemiasAPI,
)
def atualizar_glicemia(
    glicemia_id: UUID, novos_valores: ValoresParaEdicaoDeGlicemiaAPI
):
    # TODO: receber o usuário por meio da requisicao
    usuario_id = uuid4()

    uow = SqlAlchemyUnitOfWork()

    glicemia_editada = editar_glicemia(
        comando=EditarGlicemia(
            glicemia_id=glicemia_id,
            novos_valores=ValoresParaEdicaoDeGlicemia(
                valor=novos_valores.valor,
                observacoes=novos_valores.observacoes,
                primeira_do_dia=novos_valores.primeira_do_dia,
                horario_dosagem=novos_valores.horario_dosagem,
            ),
            editado_por=usuario_id,
        ),
        uow=uow,
    )

    return RetornoDeGlicemiasAPI(id=glicemia_editada.id)


@router.delete(
    "/v1/glicemias/{glicemia_id}",
    status_code=200,
    response_model=RetornoDeGlicemiasAPI,
)
def deletar_glicemia(glicemia_id: UUID):
    uow = SqlAlchemyUnitOfWork()

    id_glicemia_removida = remover_glicemia(
        comando=RemoverGlicemia(
            glicemia_id=glicemia_id,
        ),
        uow=uow,
    )

    return RetornoDeGlicemiasAPI(id=id_glicemia_removida)
