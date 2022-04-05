from uuid import UUID
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate

from libs.ddd import Evento


@dataclass_validate
@dataclass
class UsuarioCriado(Evento):
    usuario_id: UUID


@dataclass_validate
@dataclass
class EmailAlterado(Evento):
    usuario_id: UUID
