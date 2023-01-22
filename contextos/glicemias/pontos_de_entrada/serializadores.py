from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Extra
from contextos.glicemias.dominio.objetos_de_valor import TipoDeGlicemia

from libs.tipos_basicos.numeros import ValorDeGlicemia
from libs.tipos_basicos.identificadores_db import IdGlicemia


class SerializadorParaCriacaoDeGlicemia(BaseModel):
    tipo: TipoDeGlicemia
    valor: ValorDeGlicemia
    horario_dosagem: datetime
    observacoes: Optional[str] = None

    class Config:
        extra = Extra.forbid


class SerializadorParaEdicaoDeGlicemia(BaseModel):
    tipo: TipoDeGlicemia
    valor: ValorDeGlicemia
    horario_dosagem: datetime
    observacoes: Optional[str] = None

    class Config:
        extra = Extra.forbid


class RetornoDaAPIDeGlicemias(BaseModel):
    id: IdGlicemia


class SerializadorDeGlicemia(BaseModel):
    id: IdGlicemia
    observacoes: str
    tipo: TipoDeGlicemia
    valor: ValorDeGlicemia
    horario_dosagem: datetime


class RetornoDeConsultaDeGlicemias(BaseModel):
    glicemias: List[SerializadorDeGlicemia]
