from uuid import UUID

from libs.dominio import Dominio
from libs.unidade_de_trabalho import AbstractUnitOfWork

from contextos.usuarios.dominio.agregados import Email, Usuario


def consultar_usuario_por_id(
    uow: AbstractUnitOfWork,
    usuario_id: UUID,
) -> Usuario:

    # TODO: criar repo de visualizacao
    with uow(Dominio.usuarios):
        usuario = uow.repo_dominio.consultar_por_id(id=usuario_id)

    return usuario


def consultar_usuario_por_email(
    uow: AbstractUnitOfWork,
    usuario_email: Email,
) -> Usuario:
    # TODO: criar repo de visualizacao
    with uow(Dominio.usuarios):
        usuario = uow.repo_dominio.consultar_por_email(email=Email(usuario_email))

    return usuario
