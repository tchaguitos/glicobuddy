from datetime import date
from pydantic import BaseModel, Extra

from libs.tipos_basicos.texto import Nome, Email, Senha
from libs.tipos_basicos.identificadores_db import IdUsuario


class SerializadorParaCriacaoDeUsuario(BaseModel):
    email: Email
    senha: Senha
    nome_completo: Nome
    data_de_nascimento: date

    class Config:
        extra = Extra.forbid


class SerializadorParaEdicaoDeUsuario(BaseModel):
    nome_completo: Nome
    data_de_nascimento: date

    class Config:
        extra = Extra.forbid


class SerializadorParaAutenticarUsuario(BaseModel):
    email: Email
    senha: Senha


class SerializadorParaAlteracaoDeEmail(BaseModel):
    novo_email: Email

    class Config:
        extra = Extra.forbid


class SerializadorDeUsuario(BaseModel):
    id: IdUsuario
    email: Email
    nome_completo: Nome
    data_de_nascimento: date


class RetornoDaAPIDeUsuarios(BaseModel):
    id: IdUsuario


class RetornoDaAutenticacao(BaseModel):
    logado: bool
