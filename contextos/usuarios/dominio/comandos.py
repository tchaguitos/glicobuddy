from uuid import UUID
from datetime import date
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate

from contextos.usuarios.dominio.agregados import Email
from contextos.usuarios.dominio.objetos_de_valor import ValoresParaEdicaoDeUsuario


@dataclass_validate
@dataclass(frozen=True)
class CriarUsuario:
    email: Email
    senha: str
    nome_completo: str
    data_de_nascimento: date


@dataclass_validate
@dataclass(frozen=True)
class EditarUsuario:
    usuario_id: UUID
    novos_valores: ValoresParaEdicaoDeUsuario
    editado_por: UUID


@dataclass_validate
@dataclass(frozen=True)
class AlterarEmailDoUsuario:
    usuario_id: UUID
    novo_email: Email
