import abc

from uuid import UUID


class RepositorioDominio(abc.ABC):
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
