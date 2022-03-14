from datetime import date
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate

from contextos.usuarios.dominio.entidades import Email


@dataclass_validate
@dataclass(frozen=True)
class CriarUsuario:
    email: Email
    senha: str
    nome_completo: str
    data_de_nascimento: date
