from uuid import UUID
from typing import Iterator

from libs.dominio import Dominio
from libs.unidade_de_trabalho import UnidadeDeTrabalhoAbstrata
from libs.tipos_basicos.identificadores_db import IdGlicemia

from contextos.glicemias.dominio.entidades import Glicemia
from contextos.glicemias.repositorio.repo_consulta import RepoConsultaGlicemias


def consultar_glicemias(
    uow: UnidadeDeTrabalhoAbstrata,
) -> Iterator[Glicemia]:

    with uow(Dominio.glicemias):
        repo_consulta: RepoConsultaGlicemias = uow.repo_consulta
        glicemias_do_usuario = repo_consulta.consultar_por_usuario(
            id_usuario=uow.usuario
        )

    return glicemias_do_usuario


def consultar_glicemia_por_id(
    uow: UnidadeDeTrabalhoAbstrata,
    glicemia_id: IdGlicemia,
) -> Glicemia:

    with uow(Dominio.glicemias):
        glicemia = uow.repo_consulta.consultar_por_id(id=glicemia_id)

    return glicemia
