from uuid import UUID
from datetime import datetime
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate

from libs.ddd import Comando
from libs.tipos_basicos.identificadores_db import IdUsuario, IdGlicemia

from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia


@dataclass_validate
@dataclass(frozen=True)
class CriarGlicemia(Comando):
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime
    criado_por: IdUsuario


@dataclass_validate
@dataclass(frozen=True)
class EditarGlicemia(Comando):
    glicemia_id: IdGlicemia
    novos_valores: ValoresParaEdicaoDeGlicemia
    editado_por: IdUsuario


@dataclass_validate
@dataclass(frozen=True)
class RemoverGlicemia(Comando):
    glicemia_id: IdGlicemia
