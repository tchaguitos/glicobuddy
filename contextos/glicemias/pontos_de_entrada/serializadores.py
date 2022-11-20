from typing import List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Extra

from libs.tipos_basicos.identificadores_db import IdGlicemia


class SerializadorParaCriacaoDeGlicemia(BaseModel):
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime

    class Config:
        extra = Extra.forbid


class SerializadorParaEdicaoDeGlicemia(BaseModel):
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime

    class Config:
        extra = Extra.forbid


class RetornoDaAPIDeGlicemias(BaseModel):
    id: IdGlicemia


class SerializadorDeGlicemia(BaseModel):
    id: IdGlicemia
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime


class RetornoDeConsultaDeGlicemias(BaseModel):
    glicemias: List[SerializadorDeGlicemia]
