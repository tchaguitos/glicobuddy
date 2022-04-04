from libs.repositorio import RepositorioDominio

from contextos.usuarios.dominio.entidades import Usuario


class RepoDominioUsuarios(RepositorioDominio):
    def adicionar(self, usuario: Usuario):
        self.session.add(usuario)

    def atualizar(self, usuario: Usuario):
        self.session.merge(usuario)

    def remover(self, usuario: Usuario):
        self.session.delete(usuario)
