from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate

from libs.ddd import Evento
from libs.tipos_basicos.texto import Email
from libs.tipos_basicos.identificadores_db import IdUsuario


@dataclass_validate
@dataclass
class UsuarioCriado(Evento):
    usuario_id: IdUsuario


@dataclass_validate
@dataclass
class EmailAlterado(Evento):
    usuario_id: IdUsuario
    novo_email: Email
