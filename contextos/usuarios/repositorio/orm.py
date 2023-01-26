from datetime import datetime
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Table,
    Column,
    String,
    DateTime,
    UniqueConstraint,
)

from libs.orm import mapper, metadata

from contextos.usuarios.dominio.agregados import Usuario


usuario = Table(
    "usuario",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True),
    Column("email", String(155), unique=True),
    Column("senha", String(255), nullable=False),
    Column("nome_completo", String(255), nullable=False),
    Column("data_de_nascimento", Date, nullable=False),
    Column(
        "data_criacao_utc",
        DateTime,
        default=datetime.utcnow(),
        nullable=False,
    ),
    UniqueConstraint("email", name="constraint_usuario_email"),
)

mapper_usuario = mapper.map_imperatively(
    Usuario,
    usuario,
)
