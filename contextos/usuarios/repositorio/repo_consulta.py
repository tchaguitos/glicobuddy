from uuid import UUID
from typing import Iterator

from libs.repositorio import RepositorioConsulta

from contextos.usuarios.dominio.agregados import Email, Usuario


class RepoConsultaUsuarios(RepositorioConsulta):
    def consultar_todos(self) -> Iterator[Usuario]:
        return self.session.query(Usuario).all()

    def consultar_por_id(self, id: UUID) -> Usuario:
        return self.session.query(Usuario).filter_by(id=id).first()

    def consultar_por_email(self, email: Email) -> Usuario:
        return self.session.query(Usuario).filter_by(email=email).first()
