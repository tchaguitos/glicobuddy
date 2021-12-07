from typing import Optional
from uuid import UUID, uuid4
from datetime import date, datetime
from dataclasses import dataclass


@dataclass
class Auditoria:
    criado_por: UUID  # TODO: criar classe para usuario
    data_criacao: datetime
    ultima_vez_editado_por: Optional[UUID]
    data_ultima_edicao: Optional[datetime]
    ativo: bool = True
    deletado: bool = False


@dataclass
class Glicemia:
    valor: int
    jejum: bool
    data: datetime
    observacoes: str
    auditoria: Auditoria

    @classmethod
    def criar_nova(
        cls,
        valor: int,
        jejum: bool,
        data: datetime,
        observacoes: str,
        criado_por: UUID,
    ):
        return cls(
            valor=valor,
            jejum=jejum,
            data=data,
            observacoes=observacoes,
            auditoria=Auditoria(
                criado_por=criado_por,
                data_criacao=datetime.now(),
                ultima_vez_editado_por=None,
                data_ultima_edicao=None,
                ativo=True,
                deletado=False,
            ),
        )
