import abc

from uuid import UUID


class AbstractRepository(abc.ABC):
    @abc.abstractclassmethod
    def adicionar(self):
        raise NotImplementedError

    @abc.abstractmethod
    def remover(self):
        raise NotImplementedError

    @abc.abstractmethod
    def consultar_todos(self):
        raise NotImplementedError

    @abc.abstractmethod
    def consultar_por_id(self, id: UUID):
        raise NotImplementedError


class SqlAlchemyRepository(abc.ABC):
    def __init__(self, session):
        self.session = session

    @abc.abstractmethod
    def __exit__(self):
        raise NotImplementedError
