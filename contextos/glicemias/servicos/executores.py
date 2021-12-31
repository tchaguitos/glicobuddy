from uuid import UUID
from contextos.glicemias.dominio.entidades import Glicemia
from contextos.glicemias.dominio.comandos import (
    CriarGlicemia,
    EditarGlicemia,
    RemoverGlicemia,
)

from contextos.glicemias.servicos.unidade_de_trabalho import AbstractUnitOfWork


def criar_glicemia(comando: CriarGlicemia, uow: AbstractUnitOfWork):
    with uow:
        nova_glicemia = Glicemia.criar(
            valor=comando.valor,
            horario_dosagem=comando.horario_dosagem,
            observacoes=comando.observacoes,
            primeira_do_dia=comando.primeira_do_dia,
            criado_por=comando.criado_por,
        )

        uow.repo.adicionar(nova_glicemia)
        uow.commit()

        return nova_glicemia


def editar_glicemia(comando: EditarGlicemia, uow: AbstractUnitOfWork):

    with uow:
        glicemia = uow.repo.consultar_por_id(id=comando.glicemia_id)

        glicemia_editada = glicemia.editar(
            editado_por=comando.editado_por,
            novos_valores=comando.novos_valores,
        )

        uow.repo.atualizar(glicemia_editada)
        uow.commit()

        return glicemia_editada


def remover_glicemia(comando: RemoverGlicemia, uow: AbstractUnitOfWork) -> UUID:
    with uow:
        glicemia = uow.repo.consultar_por_id(id=comando.glicemia_id)

        uow.repo.remover(glicemia)
        uow.commit()

        return glicemia.id
