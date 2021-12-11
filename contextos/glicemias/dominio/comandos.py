from uuid import UUID
from datetime import datetime
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate


@dataclass_validate
@dataclass(frozen=True)
class CriarGlicemia:
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime
    criado_por: UUID
