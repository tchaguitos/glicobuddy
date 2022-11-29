from abc import ABC, abstractmethod
from passlib.context import CryptContext


class Encriptador(ABC):
    """
    Interface utilizada para adaptadores com a função de tratar
    as senhas dos usuários do sistema
    """

    @abstractmethod
    def _encriptar(self, texto: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _verificar(
        self,
        texto_para_verificar: str,
        texto_encriptado: str,
    ) -> bool:
        raise NotImplementedError()


class EncriptadorDeSenha(Encriptador):
    """
    Classe responsável por encriptar senhas
    """

    # TODO: criar abstracao para ser possivel alterar o contexto ao iniciar a classe
    contexto: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encriptar_senha(self, senha: str) -> str:
        senha_encriptada = self._encriptar(texto=senha)
        return senha_encriptada

    def verificar_senha(self, senha_para_verificar: str, senha_do_usuario: str) -> bool:
        senha_valida = self._verificar(
            texto_para_verificar=senha_para_verificar,
            texto_encriptado=senha_do_usuario,
        )
        return senha_valida

    def _encriptar(self, texto: str) -> str:
        return self.contexto.hash(texto)

    def _verificar(
        self,
        texto_para_verificar: str,
        texto_encriptado: str,
    ) -> bool:
        return self.contexto.verify(
            texto_para_verificar,
            texto_encriptado,
        )
