from datetime import datetime
from sqlalchemy.orm import composite
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Table,
    Column,
    Boolean,
    String,
    Integer,
    DateTime,
)

from libs.orm import mapper, metadata

from contextos.glicemias.dominio.entidades import Auditoria, Glicemia


glicemia = Table(
    "glicemia",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True),
    Column("valor", Integer),
    Column("observacoes", String(255)),
    Column("primeira_do_dia", Boolean, default=False),
    Column("horario_dosagem", DateTime),
    Column("criado_por", UUID(as_uuid=True)),  # p abaixo colunas de auditoria
    Column("data_criacao", DateTime, default=datetime.now()),
    Column("ultima_vez_editado_por", UUID(as_uuid=True), nullable=True),
    Column("data_ultima_edicao", DateTime, nullable=True),
    Column("ativo", Boolean, default=True),
    Column("deletado", Boolean, default=False),
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
            glicemia.c.ativo,
            glicemia.c.deletado,
        )
    },
)
