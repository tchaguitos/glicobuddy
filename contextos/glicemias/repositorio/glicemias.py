import abc

from contextos.glicemias.dominio.entidades import Glicemia


class AbstractRepository(abc.ABC):
    @abc.abstractclassmethod
    def add(self, glicemia: Glicemia):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> Glicemia:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, id):
        return self.session.query(Glicemia).filter_by(id=id).one()

    def list(self):
        return self.session.query(Glicemia).all()
