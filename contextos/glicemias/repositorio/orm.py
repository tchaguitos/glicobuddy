from datetime import datetime
from sqlalchemy.orm import composite
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
)

from libs.orm import mapper, metadata

from contextos.usuarios.repositorio.orm import usuario
from contextos.glicemias.dominio.entidades import Auditoria, Glicemia
from contextos.glicemias.dominio.objetos_de_valor import TipoDeGlicemia


glicemia = Table(
    "glicemia",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True),
    Column("valor", Integer),
    Column("observacoes", String(255)),
    Column("tipo", ENUM(TipoDeGlicemia, schema="public")),
    Column("horario_dosagem", DateTime),
    Column("criado_por", ForeignKey(usuario.c.id, ondelete="CASCADE")),
    Column("data_criacao", DateTime, default=datetime.utcnow()),
    Column(
        "ultima_vez_editado_por",
        ForeignKey(usuario.c.id, ondelete="CASCADE"),
        nullable=True,
    ),
    Column("data_ultima_edicao", DateTime, nullable=True),
)

mapper_glicemia = mapper.map_imperatively(
    Glicemia,
    glicemia,
    properties={
        "auditoria": composite(
            Auditoria,
            glicemia.c.criado_por,
            glicemia.c.data_criacao,
            glicemia.c.ultima_vez_editado_por,
            glicemia.c.data_ultima_edicao,
        )
    },
)
