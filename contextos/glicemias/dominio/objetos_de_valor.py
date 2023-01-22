from enum import Enum
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate

from libs.tipos_basicos.numeros import ValorDeGlicemia

class TipoDeGlicemia(str, Enum):
    jejum = "jejum"
    casual = "casual"
    pre_prandial = "pre_prandial"
    pos_prandial = "pos_prandial"

@dataclass_validate
@dataclass(frozen=True)
class ValoresParaEdicaoDeGlicemia:
    tipo: TipoDeGlicemia
    valor: ValorDeGlicemia
    horario_dosagem: datetime
    observacoes: Optional[str] = None
