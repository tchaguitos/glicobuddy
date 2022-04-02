from uuid import UUID
from typing import Iterator

from libs.repositorio import SqlAlchemyRepository

from contextos.usuarios.dominio.agregados import (
    Email,
    Usuario,
)


class RepoAbstratoUsuarios(SqlAlchemyRepository):
    def adicionar(self, usuario: Usuario):
        raise NotImplementedError

    def remover(self, usuario: Usuario):
        raise NotImplementedError

    def consultar_todos(self):
        raise NotImplementedError

    def consultar_por_id(self, id: UUID) -> Usuario:
        raise NotImplementedError

    def consultar_por_email(self, email: Email) -> Usuario:
        raise NotImplementedError


class RepoDominioUsuarios(RepoAbstratoUsuarios):
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
