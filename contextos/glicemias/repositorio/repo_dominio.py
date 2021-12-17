import abc
from uuid import UUID
from contextos.glicemias.dominio.entidades import Glicemia


class AbstractRepository(abc.ABC):
    @abc.abstractclassmethod
    def adicionar(self, glicemia: Glicemia):
        raise NotImplementedError

    @abc.abstractmethod
    def remover(self, glicemia: Glicemia):
        raise NotImplementedError

    @abc.abstractmethod
    def consultar_todos(self):
        raise NotImplementedError

    @abc.abstractmethod
    def consultar_por_id(self, id: UUID) -> Glicemia:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def adicionar(self, glicemia: Glicemia):
        self.session.add(glicemia)

    def remover(self, glicemia: Glicemia):
        self.session.delete(glicemia)

    def consultar_todos(self):
        return self.session.query(Glicemia).all()

    def consultar_por_id(self, id: UUID):
        return self.session.query(Glicemia).filter_by(id=id).one()
