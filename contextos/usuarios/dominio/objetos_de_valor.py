from datetime import date
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate


@dataclass_validate
@dataclass(frozen=True)
class ValoresParaEdicaoDeUsuario:
    nome_completo: str
    data_de_nascimento: date
