from typing import Set

from libs.ddd import Agregado
from libs.repositorio import RepositorioDominio

from contextos.usuarios.dominio.agregados import Usuario


class RepoDominioUsuarios(RepositorioDominio):
    objetos_modificados: Set[Agregado]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objetos_modificados: Set[Usuario] = set()

    def adicionar(self, usuario: Usuario):
        self.objetos_modificados.add(usuario)
        self.session.add(usuario)

    def atualizar(self, usuario: Usuario):
        self.objetos_modificados.add(usuario)
        self.session.merge(usuario)

    def remover(self, usuario: Usuario):
        self.objetos_modificados.add(usuario)
        self.session.delete(usuario)
