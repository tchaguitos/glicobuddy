from enum import Enum

from contextos.usuarios.repositorio.repo_dominio import RepoDominioUsuarios
from contextos.usuarios.repositorio.repo_consulta import RepoConsultaUsuarios

from contextos.glicemias.repositorio.repo_dominio import RepoDominioGlicemias
from contextos.glicemias.repositorio.repo_consulta import RepoConsultaGlicemias


class Dominio(Enum):
    usuarios = (RepoDominioUsuarios, RepoConsultaUsuarios)
    glicemias = (RepoDominioGlicemias, RepoConsultaGlicemias)
