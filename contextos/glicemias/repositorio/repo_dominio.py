from uuid import UUID
from typing import Iterator

from libs.repositorio import SqlAlchemyRepository

from contextos.glicemias.dominio.entidades import Glicemia


class RepoAbstratoGlicemias(SqlAlchemyRepository):
    def adicionar(self, glicemia: Glicemia):
        raise NotImplementedError

    def remover(self, glicemia: Glicemia):
        raise NotImplementedError

    def consultar_todos(self):
        raise NotImplementedError

    def consultar_por_id(self, id: UUID) -> Glicemia:
        raise NotImplementedError


class RepoDominioGlicemias(RepoAbstratoGlicemias):
    def __init__(self, session):
        self.session = session

    def adicionar(self, glicemia: Glicemia):
        self.session.add(glicemia)

    def atualizar(self, glicemia: Glicemia):
        self.session.merge(glicemia)

    def remover(self, glicemia: Glicemia):
        self.session.delete(glicemia)

    def consultar_todos(self) -> Iterator[Glicemia]:
        return self.session.query(Glicemia).all()

    def consultar_por_id(self, id: UUID) -> Glicemia:
        return self.session.query(Glicemia).filter_by(id=id).first()
