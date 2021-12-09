from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, MetaData, Column, Boolean, String, Integer, DateTime, ForeignKey

from contextos.glicemias.dominio.entidades import Auditoria, Glicemia

metadata = MetaData()

tabela_auditoria = Table(
    "auditoria",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("criado_por", String(94)),
    Column("data_criacao", DateTime, default=datetime.now()),
    Column("ultima_vez_editado_por", DateTime, nullable=True),
    Column("data_ultima_edicao", DateTime, nullable=True),
    Column("ativo", Boolean, default=True),
    Column("deletado", Boolean, default=False),
)

tabela_glicemias = Table(
    "glicemia",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("valor", Integer)
    Column("jejum", Boolean, default=False),
    Column("data")
    Column("observacoes")
    # auditoria: Auditoria
)