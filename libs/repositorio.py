import abc
from uuid import UUID
from typing import Set

from libs.ddd import Agregado


class RepositorioDominio(abc.ABC):
    objetos_modificados: Set[Agregado]

    def __init__(self, session):
        self.session = session

    @abc.abstractclassmethod
    def adicionar(self):
        raise NotImplementedError

    @abc.abstractmethod
    def remover(self):
        raise NotImplementedError


class RepositorioConsulta(abc.ABC):
    def __init__(self, session):
        self.session = session

    @abc.abstractmethod
    def consultar_todos(self):
        raise NotImplementedError

    @abc.abstractmethod
    def consultar_por_id(self, id: UUID):
        raise NotImplementedError
