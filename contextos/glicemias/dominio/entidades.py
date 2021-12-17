from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from dataclasses import dataclass, asdict, replace
from dataclass_type_validator import dataclass_validate

from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia


@dataclass_validate
@dataclass
class Auditoria:
    criado_por: UUID  # TODO: criar classe para usuario
    data_criacao: datetime
    ultima_vez_editado_por: Optional[UUID]
    data_ultima_edicao: Optional[datetime]
    ativo: bool = True
    deletado: bool = False

    def __composite_values__(self):
        return (
            self.criado_por,
            self.data_criacao,
            self.ultima_vez_editado_por,
            self.data_ultima_edicao,
            self.ativo,
            self.deletado,
        )


@dataclass_validate
@dataclass
class Glicemia:
    valor: int
    observacoes: str
    primeira_do_dia: bool
    horario_dosagem: datetime
    auditoria: Auditoria
    id: Optional[UUID] = None  # TODO: melhorar modelagem

    class ValorDeGlicemiaInvalido(Exception):
        pass

    def __post_init__(self):
        if not self.valor > 20:
            raise Glicemia.ValorDeGlicemiaInvalido(
                "O valor da glicemia deve ser superior a 20mg/dl"
            )

    @classmethod
    def criar(
        cls,
        valor: int,
        horario_dosagem: datetime,
        observacoes: str,
        primeira_do_dia: bool,
        criado_por: UUID,
    ):
        """"""
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

    def __atualizar_valores_auditoria(self, editado_por: UUID):
        novos_valores_auditoria = {
            "data_ultima_edicao": datetime.now(),
            "ultima_vez_editado_por": editado_por,
        }

        auditoria = replace(self.auditoria, **novos_valores_auditoria)

        self.auditoria = auditoria

    def __atualizar_valores(
        self,
        editado_por: UUID,
        novos_valores: ValoresParaEdicaoDeGlicemia,
    ):
        """"""
        novos_valores_glicemia = asdict(novos_valores)

        self = replace(self, **novos_valores_glicemia)

        self.__atualizar_valores_auditoria(editado_por=editado_por)

        return self
