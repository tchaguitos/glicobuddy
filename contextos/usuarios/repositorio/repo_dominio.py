import abc

from uuid import UUID
from typing import Iterator
from contextos.usuarios.dominio.entidades import (
    Email,
    Usuario,
)


class AbstractRepository(abc.ABC):
    @abc.abstractclassmethod
    def adicionar(self, usuario: Usuario):
        raise NotImplementedError

    @abc.abstractmethod
    def remover(self, usuario: Usuario):
        raise NotImplementedError

    @abc.abstractmethod
    def consultar_todos(self):
        raise NotImplementedError

    @abc.abstractmethod
    def consultar_por_id(self, id: UUID) -> Usuario:
        raise NotImplementedError

    @abc.abstractmethod
    def consultar_por_email(self, email: Email) -> Usuario:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def adicionar(self, usuario: Usuario):
        self.session.add(usuario)

    def atualizar(self, usuario: Usuario):
        self.session.merge(usuario)

    def remover(self, usuario: Usuario):
        self.session.delete(usuario)

    def consultar_todos(self) -> Iterator[Usuario]:
        return self.session.query(Usuario).all()

    def consultar_por_id(self, id: UUID) -> Usuario:
        return self.session.query(Usuario).filter_by(id=id).first()

    def consultar_por_email(self, email: Email) -> Usuario:
        return self.session.query(Usuario).filter_by(email=email).first()
