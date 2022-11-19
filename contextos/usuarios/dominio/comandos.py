from datetime import date
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate

from libs.tipos_basicos.texto import Nome, Email, Senha
from libs.tipos_basicos.identificadores_db import IdUsuario

from contextos.usuarios.dominio.objetos_de_valor import ValoresParaEdicaoDeUsuario


@dataclass_validate
@dataclass(frozen=True)
class CriarUsuario:
    email: Email
    senha: Senha
    nome_completo: Nome
    data_de_nascimento: date


@dataclass_validate
@dataclass(frozen=True)
class EditarUsuario:
    usuario_id: IdUsuario
    editado_por: IdUsuario
    novos_valores: ValoresParaEdicaoDeUsuario


@dataclass_validate
@dataclass(frozen=True)
class AutenticarUsuario:
    email: Email
    senha: Senha


@dataclass_validate
@dataclass(frozen=True)
class AlterarEmailDoUsuario:
    usuario_id: IdUsuario
    novo_email: Email
