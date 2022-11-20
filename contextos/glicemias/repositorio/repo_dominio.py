from typing import Set

from libs.ddd import Agregado
from libs.repositorio import RepositorioDominio

from contextos.glicemias.dominio.entidades import Glicemia


class RepoDominioGlicemias(RepositorioDominio):
    objetos_modificados: Set[Agregado]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objetos_modificados: Set[Glicemia] = set()

    def adicionar(self, glicemia: Glicemia):
        self.objetos_modificados.add(glicemia)
        self.session.add(glicemia)

    def atualizar(self, glicemia: Glicemia):
        self.objetos_modificados.add(glicemia)
        self.session.merge(glicemia)

    def remover(self, glicemia: Glicemia):
        self.objetos_modificados.add(glicemia)
        self.session.delete(glicemia)
