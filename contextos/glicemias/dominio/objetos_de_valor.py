from datetime import datetime
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate


@dataclass_validate
@dataclass(frozen=True)
class ValoresParaEdicaoDeGlicemia:
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime
