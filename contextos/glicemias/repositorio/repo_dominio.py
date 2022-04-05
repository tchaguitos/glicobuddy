from libs.repositorio import RepositorioDominio

from contextos.glicemias.dominio.entidades import Glicemia


class RepoDominioGlicemias(RepositorioDominio):
    def adicionar(self, glicemia: Glicemia):
        self.session.add(glicemia)

    def atualizar(self, glicemia: Glicemia):
        self.session.merge(glicemia)

    def remover(self, glicemia: Glicemia):
        self.session.delete(glicemia)
