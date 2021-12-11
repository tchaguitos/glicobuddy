from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from dataclasses import dataclass, asdict, replace
from dataclass_type_validator import dataclass_validate

from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia


class ValorDeGlicemiaInvalido(Exception):
    pass


@dataclass_validate
@dataclass
class Auditoria:
    criado_por: UUID  # TODO: criar classe para usuario
    data_criacao: datetime
    ultima_vez_editado_por: Optional[UUID]
    data_ultima_edicao: Optional[datetime]
    ativo: bool = True
    deletado: bool = False


@dataclass_validate
@dataclass
class Glicemia:
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime
    auditoria: Auditoria
    id: Optional[UUID] = None  # TODO: melhorar modelagem

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
        self,
        editado_por: UUID,
        novos_valores: ValoresParaEdicaoDeGlicemia,
    ):
        """"""
        objeto_editado = self.__atualizar_valores(
            novos_valores=novos_valores, editado_por=editado_por
        )

        return objeto_editado

    def __atualizar_valores(
        self,
        editado_por: UUID,
        novos_valores: ValoresParaEdicaoDeGlicemia,
    ):
        """"""
        novos_valores_glicemia = asdict(novos_valores)

        self = replace(self, **novos_valores_glicemia)

        novos_valores_auditoria = {
            "data_ultima_edicao": datetime.now(),
            "ultima_vez_editado_por": editado_por,
        }

        auditoria = replace(self.auditoria, **novos_valores_auditoria)

        self.auditoria = auditoria

        return self
