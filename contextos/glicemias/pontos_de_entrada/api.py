from fastapi import APIRouter, HTTPException, Depends

from libs.unidade_de_trabalho import UnidadeDeTrabalho
from libs.tipos_basicos.identificadores_db import IdUsuario, IdGlicemia
from libs.pontos_de_entrada import retornar_usuario_logado

from contextos.glicemias.dominio.comandos import (
    CriarGlicemia,
    EditarGlicemia,
    RemoverGlicemia,
)

from contextos.glicemias.servicos.visualizadores import (
    consultar_glicemias,
    consultar_glicemia_por_id,
)
from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia

from contextos.glicemias.pontos_de_entrada.serializadores import (
    SerializadorDeGlicemia,
    RetornoDaAPIDeGlicemias,
    RetornoDeConsultaDeGlicemias,
    SerializadorParaEdicaoDeGlicemia,
    SerializadorParaCriacaoDeGlicemia,
)

from contextos import barramento

from contextos.usuarios.pontos_de_entrada.serializadores import SerializadorDeUsuario

router = APIRouter(
    tags=["glicemias"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/v1/glicemias",
    status_code=200,
    response_model=RetornoDeConsultaDeGlicemias,
)
def listar_glicemias(
    usuario_logado: SerializadorDeUsuario = Depends(retornar_usuario_logado),
):

    uow = UnidadeDeTrabalho(usuario=usuario_logado.id)

    glicemias = consultar_glicemias(
        uow=uow,
    )

    return RetornoDeConsultaDeGlicemias(
        glicemias=[
            SerializadorDeGlicemia(
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
    response_model=RetornoDeConsultaDeGlicemias,
)
def consultar_glicemias_por_id(
    glicemia_id: IdGlicemia,
    usuario_logado: SerializadorDeUsuario = Depends(retornar_usuario_logado),
):
    uow = UnidadeDeTrabalho(usuario=usuario_logado.id)

    glicemia = consultar_glicemia_por_id(
        glicemia_id=glicemia_id,
        uow=uow,
    )

    if not glicemia:
        raise HTTPException(
            status_code=404, detail="Não existe glicemia com o ID informado"
        )

    return RetornoDeConsultaDeGlicemias(
        glicemias=[
            SerializadorDeGlicemia(
                id=IdGlicemia(glicemia.id),
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
    response_model=RetornoDaAPIDeGlicemias,
)
def cadastrar_glicemia(
    nova_glicemia: SerializadorParaCriacaoDeGlicemia,
    usuario_logado: SerializadorDeUsuario = Depends(retornar_usuario_logado),
):
    usuario_id = usuario_logado.id

    uow = UnidadeDeTrabalho(usuario=usuario_id)
    bus = barramento.bootstrap(uow=uow)

    try:
        glicemia_criada = bus.tratar_mensagem(
            mensagem=CriarGlicemia(
                valor=nova_glicemia.valor,
                observacoes=nova_glicemia.observacoes,
                primeira_do_dia=nova_glicemia.primeira_do_dia,
                horario_dosagem=nova_glicemia.horario_dosagem,
            ),
        )

        return RetornoDaAPIDeGlicemias(id=glicemia_criada.id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/v1/glicemias/{glicemia_id}",
    status_code=200,
    response_model=RetornoDaAPIDeGlicemias,
)
def atualizar_glicemia(
    glicemia_id: IdGlicemia,
    novos_valores: SerializadorParaEdicaoDeGlicemia,
    usuario_logado: SerializadorDeUsuario = Depends(retornar_usuario_logado),
):
    usuario_id = usuario_logado.id

    uow = UnidadeDeTrabalho(usuario=usuario_id)
    bus = barramento.bootstrap(uow=uow)

    try:
        glicemia_editada = bus.tratar_mensagem(
            mensagem=EditarGlicemia(
                glicemia_id=IdGlicemia(glicemia_id),
                novos_valores=ValoresParaEdicaoDeGlicemia(
                    valor=novos_valores.valor,
                    observacoes=novos_valores.observacoes,
                    primeira_do_dia=novos_valores.primeira_do_dia,
                    horario_dosagem=novos_valores.horario_dosagem,
                ),
            ),
        )

        return RetornoDaAPIDeGlicemias(id=glicemia_editada.id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/v1/glicemias/{glicemia_id}",
    status_code=200,
    response_model=RetornoDaAPIDeGlicemias,
)
def deletar_glicemia(
    glicemia_id: IdGlicemia,
    usuario_logado: SerializadorDeUsuario = Depends(retornar_usuario_logado),
):
    uow = UnidadeDeTrabalho(usuario=usuario_logado.id)
    bus = barramento.bootstrap(uow=uow)

    id_glicemia_removida = bus.tratar_mensagem(
        mensagem=RemoverGlicemia(
            glicemia_id=IdGlicemia(glicemia_id),
        ),
    )

    return RetornoDaAPIDeGlicemias(id=id_glicemia_removida)
