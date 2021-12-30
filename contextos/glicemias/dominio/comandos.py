from uuid import UUID
from datetime import datetime
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate

from contextos.glicemias.dominio.entidades import Glicemia
from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia


@dataclass_validate
@dataclass(frozen=True)
class CriarGlicemia:
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime
    criado_por: UUID


@dataclass_validate
@dataclass(frozen=True)
class EditarGlicemia:
    glicemia_id: UUID
    novos_valores: ValoresParaEdicaoDeGlicemia
    editado_por: UUID


@dataclass_validate
@dataclass(frozen=True)
class RemoverGlicemia:
    glicemia_id: UUID
