from typing import Optional
from datetime import datetime

from dataclass_type_validator import dataclass_validate
from dataclasses import dataclass, asdict, replace, field

from libs.tipos_basicos.identificadores_db import IdUsuario, IdGlicemia

from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia


@dataclass_validate
@dataclass
class Auditoria:
    criado_por: IdUsuario
    data_criacao: datetime
    ultima_vez_editado_por: Optional[IdUsuario]
    data_ultima_edicao: Optional[datetime]
    ativo: bool = True
    deletado: bool = False

    def __post_init__(self):
        self.criado_por = IdUsuario(self.criado_por)

        if self.ultima_vez_editado_por:
            self.ultima_vez_editado_por = IdUsuario(self.ultima_vez_editado_por)

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
    id: IdGlicemia = field(init=False, default_factory=IdGlicemia)

    class ValorDeGlicemiaInvalido(Exception):
        pass

    def __hash__(self):
        return hash(self.id)

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
        criado_por: IdUsuario,
    ):
        """"""
        return cls(
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
        editado_por: IdUsuario,
        novos_valores: ValoresParaEdicaoDeGlicemia,
    ):
        """"""
        objeto_editado = self.__atualizar_valores(
            novos_valores=novos_valores, editado_por=editado_por
        )

        return objeto_editado

    def __atualizar_valores_auditoria(self, editado_por: IdUsuario):
        self.auditoria.data_ultima_edicao = datetime.now()
        self.auditoria.ultima_vez_editado_por = editado_por

        return self.auditoria

    def __atualizar_valores(
        self,
        editado_por: IdUsuario,
        novos_valores: ValoresParaEdicaoDeGlicemia,
    ):
        """"""

        glicemia_atualizada = replace(self, **asdict(novos_valores))

        self.valor = glicemia_atualizada.valor
        self.observacoes = glicemia_atualizada.observacoes
        self.primeira_do_dia = glicemia_atualizada.primeira_do_dia
        self.horario_dosagem = glicemia_atualizada.horario_dosagem

        self.__atualizar_valores_auditoria(editado_por=editado_por)

        return self
