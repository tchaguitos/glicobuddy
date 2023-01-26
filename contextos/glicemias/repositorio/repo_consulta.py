from typing import List

from libs.repositorio import RepositorioConsulta
from libs.tipos_basicos.identificadores_db import IdUsuario, IdGlicemia

from contextos.glicemias.dominio.entidades import Glicemia


class RepoConsultaGlicemias(RepositorioConsulta):
    def consultar_todos(self) -> List[Glicemia]:
        return self.session.query(Glicemia).all()

    def consultar_por_id(self, id: IdGlicemia) -> Glicemia:
        return self.session.query(Glicemia).filter_by(id=id).first()

    def consultar_por_usuario(self, id_usuario: IdUsuario) -> List[Glicemia]:
        return (
            self.session.query(Glicemia).filter(Glicemia.criado_por == id_usuario).all()
        )
