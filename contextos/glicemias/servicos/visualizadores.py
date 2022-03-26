from uuid import UUID
from typing import Iterator

from libs.dominio import Dominio
from libs.unidade_de_trabalho import AbstractUnitOfWork

from contextos.glicemias.dominio.entidades import Glicemia


def consultar_glicemias(
    uow: AbstractUnitOfWork,
    usuario_id: UUID,
) -> Iterator[Glicemia]:

    with uow(Dominio.glicemias):
        print(usuario_id)  # TODO: vincular glicemias a usuarios ou outra entidade
        # TODO: criar repo de visualizacao
        glicemias = uow.repo_dominio.consultar_todos()

    return glicemias


def consultar_glicemia_por_id(
    uow: AbstractUnitOfWork,
    usuario_id: UUID,
    glicemia_id: UUID,
) -> Glicemia:

    with uow(Dominio.glicemias):
        print(usuario_id)  # TODO: vincular glicemias a usuarios ou outra entidade
        # TODO: criar repo de visualizacao
        glicemia = uow.repo_dominio.consultar_por_id(id=glicemia_id)

    return glicemia
