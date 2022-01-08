from uuid import UUID
from typing import Iterator

from contextos.glicemias.dominio.entidades import Glicemia

from contextos.glicemias.servicos.unidade_de_trabalho import AbstractUnitOfWork


def consultar_glicemias(
    uow: AbstractUnitOfWork,
    usuario_id: UUID,
) -> Iterator[Glicemia]:

    with uow:
        print(usuario_id)  # TODO: vincular glicemias a usuarios ou outra entidade
        glicemias = uow.repo.consultar_todos()

    return glicemias


def consultar_glicemia_por_id(
    uow: AbstractUnitOfWork,
    usuario_id: UUID,
    glicemia_id: UUID,
) -> Glicemia:

    with uow:
        print(usuario_id)  # TODO: vincular glicemias a usuarios ou outra entidade
        glicemia = uow.repo.consultar_por_id(id=glicemia_id)

    return glicemia
