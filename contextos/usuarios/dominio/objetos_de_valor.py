from datetime import date
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate

from libs.tipos_basicos.texto import Nome


@dataclass_validate
@dataclass(frozen=True)
class ValoresParaEdicaoDeUsuario:
    nome_completo: Nome
    data_de_nascimento: date
