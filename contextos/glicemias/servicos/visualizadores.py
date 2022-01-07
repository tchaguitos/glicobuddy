from typing import List

from contextos.glicemias.dominio.entidades import Glicemia
from contextos.glicemias.repositorio.repo_dominio import AbstractRepository


def consultar_glicemias(repo: AbstractRepository, sessao) -> List[Glicemia]:
    glicemias = repo.consultar_todos()
    yield from glicemias
