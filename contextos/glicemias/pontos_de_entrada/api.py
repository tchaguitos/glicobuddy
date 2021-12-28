from uuid import UUID, uuid4

from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel, Extra

from contextos.glicemias.dominio.entidades import Glicemia

from contextos.glicemias.dominio.comandos import CriarGlicemia
from contextos.glicemias.servicos.executores import criar_glicemia


app = FastAPI()


class ValoresParaCriacaoDeGlicemia(BaseModel):
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime

    class Config:
        extra = Extra.forbid


class RetornoDeCriacaoDeGlicemia(BaseModel):
    id: UUID


@app.post("/v1/glicemias", response_model=RetornoDeCriacaoDeGlicemia, status_code=201)
def cadastrar_glicemia(nova_glicemia: ValoresParaCriacaoDeGlicemia) -> UUID:
    usuario_id = uuid4()

    glicemia_criada = criar_glicemia(
        comando=CriarGlicemia(
            valor=nova_glicemia.valor,
            observacoes=nova_glicemia.observacoes,
            primeira_do_dia=nova_glicemia.primeira_do_dia,
            horario_dosagem=nova_glicemia.horario_dosagem,
            criado_por=usuario_id,
        ),
    )

    return RetornoDeCriacaoDeGlicemia(id=glicemia_criada.id)
