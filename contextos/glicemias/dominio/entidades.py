from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from dataclasses import dataclass, asdict
from dataclass_type_validator import dataclass_validate


class ValorDeGlicemiaInvalido(Exception):
    pass


@dataclass_validate
@dataclass(frozen=True)
class Auditoria:
    criado_por: UUID  # TODO: criar classe para usuario
    data_criacao: datetime
    ultima_vez_editado_por: Optional[UUID]
    data_ultima_edicao: Optional[datetime]
    ativo: bool = True
    deletado: bool = False


@dataclass_validate
@dataclass(frozen=True)
class Glicemia:
    id: UUID
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime
    auditoria: Auditoria

    @classmethod
    def criar(
        cls,
        valor: int,
        horario_dosagem: datetime,
        observacoes: str,
        primeira_do_dia: bool,
        criado_por: UUID,
    ):

        if not valor > 20:
            raise ValorDeGlicemiaInvalido(
                "O valor da glicemia deve ser superior a 20mg/dl"
            )

        return cls(
            id=uuid4(),
            valor=valor,
            horario_dosagem=horario_dosagem,
            observacoes=observacoes,
            primeira_do_dia=primeira_do_dia,
            auditoria=Auditoria(
                criado_por=criado_por,
                data_criacao=datetime.now(),
                ultima_vez_editado_por=None,
                data_ultima_edicao=None,
                ativo=True,
                deletado=False,
            ),
        )

    def editar(
        id: UUID,
        valor: int,
        horario_dosagem: datetime,
        observacoes: str,
        primeira_do_dia: bool,
        editado_por: UUID,
    ):
        asdict

    def __atualizar_valor_se_necessario(self):
        return
