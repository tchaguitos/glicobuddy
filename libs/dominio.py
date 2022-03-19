from enum import Enum

from contextos.glicemias.repositorio.repo_dominio import RepoDominioGlicemias
from contextos.usuarios.repositorio.repo_dominio import RepoDominioUsuarios


class Dominio(Enum):
    glicemias = (RepoDominioGlicemias, None)
    usuarios = (RepoDominioUsuarios, None)
