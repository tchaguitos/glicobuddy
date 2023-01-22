from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate

from libs.ddd import Comando
from libs.tipos_basicos.numeros import ValorDeGlicemia
from libs.tipos_basicos.identificadores_db import IdGlicemia

from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia, TipoDeGlicemia


@dataclass_validate
@dataclass(frozen=True)
class CriarGlicemia(Comando):
    tipo: TipoDeGlicemia
    valor: ValorDeGlicemia
    horario_dosagem: datetime
    observacoes: Optional[str] = None


@dataclass_validate
@dataclass(frozen=True)
class EditarGlicemia(Comando):
    glicemia_id: IdGlicemia
    novos_valores: ValoresParaEdicaoDeGlicemia


@dataclass_validate
@dataclass(frozen=True)
class RemoverGlicemia(Comando):
    glicemia_id: IdGlicemia
