from libs.dominio import Dominio
from libs.unidade_de_trabalho import AbstractUnitOfWork

from libs.tipos_basicos.texto import Email
from libs.tipos_basicos.identificadores_db import IdUsuario

from contextos.usuarios.dominio.entidades import Usuario


def consultar_usuario_por_id(
    uow: AbstractUnitOfWork,
    usuario_id: IdUsuario,
) -> Usuario:
    """"""

    with uow(Dominio.usuarios):
        usuario = uow.repo_consulta.consultar_por_id(id_usuario=usuario_id)

    return usuario


def consultar_usuario_por_email(
    uow: AbstractUnitOfWork,
    usuario_email: Email,
) -> Usuario:
    """"""

    with uow(Dominio.usuarios):
        usuario = uow.repo_consulta.consultar_por_email(email=Email(usuario_email))

    return usuario
