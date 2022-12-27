from uuid import UUID
from typing import Iterator

from libs.repositorio import RepositorioConsulta
from libs.tipos_basicos.identificadores_db import IdUsuario

from contextos.glicemias.dominio.entidades import Glicemia


class RepoConsultaGlicemias(RepositorioConsulta):
    def consultar_todos(self) -> Iterator[Glicemia]:
        return self.session.query(Glicemia).all()

    def consultar_por_id(self, id: UUID) -> Glicemia:
        return self.session.query(Glicemia).filter_by(id=id).first()

    def consultar_por_usuario(self, id_usuario: IdUsuario) -> Iterator[Glicemia]:
        return (
            self.session.query(Glicemia).filter(Glicemia.criado_por == id_usuario).all()
        )
