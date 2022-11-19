from typing import Iterator

from libs.repositorio import RepositorioConsulta

from libs.tipos_basicos.texto import Email
from libs.tipos_basicos.identificadores_db import IdUsuario

from contextos.usuarios.dominio.entidades import Usuario


class RepoConsultaUsuarios(RepositorioConsulta):
    def consultar_todos(self) -> Iterator[Usuario]:
        return self.session.query(Usuario).all()

    def consultar_por_id(self, id_usuario: IdUsuario) -> Usuario:
        return self.session.query(Usuario).filter_by(id=id_usuario).first()

    def consultar_por_email(self, email: Email) -> Usuario:
        return self.session.query(Usuario).filter_by(email=email).first()
