from datetime import datetime
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Table,
    Column,
    String,
    DateTime,
)

from libs.orm import mapper, metadata

from contextos.usuarios.dominio.agregados import Usuario


usuario = Table(
    "usuario",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True),
    Column("email", String(155)),
    Column("senha", String(75)),
    Column("nome_completo", String(255)),
    Column("data_de_nascimento", Date),
    Column("data_criacao_utc", DateTime, default=datetime.utcnow()),
)

mapper_usuario = mapper.map_imperatively(
    Usuario,
    usuario,
)
