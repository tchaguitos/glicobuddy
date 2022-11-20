from uuid import UUID
from typing import Iterator

from libs.dominio import Dominio
from libs.unidade_de_trabalho import AbstractUnitOfWork
from libs.tipos_basicos.identificadores_db import IdUsuario, IdGlicemia

from contextos.glicemias.dominio.entidades import Glicemia


def consultar_glicemias(
    uow: AbstractUnitOfWork,
    usuario_id: IdUsuario,
) -> Iterator[Glicemia]:

    with uow(Dominio.glicemias):
        print(usuario_id)  # TODO: vincular glicemias a usuarios ou outra entidade
        glicemias = uow.repo_consulta.consultar_todos()

    return glicemias


def consultar_glicemia_por_id(
    uow: AbstractUnitOfWork,
    usuario_id: IdUsuario,
    glicemia_id: IdGlicemia,
) -> Glicemia:

    with uow(Dominio.glicemias):
        print(usuario_id)  # TODO: vincular glicemias a usuarios ou outra entidade
        glicemia = uow.repo_consulta.consultar_por_id(id=glicemia_id)

    return glicemia
