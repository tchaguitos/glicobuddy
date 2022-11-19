import bcrypt

from abc import ABC, abstractmethod

SEGREDO = bcrypt.gensalt()


class Encriptador(ABC):
    """
    Interface utilizada para adaptadores com a função de tratar
    as senhas dos usuários do sistema
    """

    segredo: bytes = SEGREDO

    @abstractmethod
    def _encriptar(self, texto: str) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def _verificar(self, texto_para_verificar: str, texto_original: bytes) -> bool:
        raise NotImplementedError()


class EncriptadorDeSenha(Encriptador):
    """"""

    def encriptar_senha(self, senha: str) -> bytes:
        senha_encriptada = self._encriptar(texto=senha)
        return senha_encriptada

    def verificar_senha(self, senha_para_verificar: str, senha_do_usuario: str) -> bool:
        senha_valida = self._verificar(
            texto_para_verificar=senha_para_verificar,
            texto_original=senha_do_usuario,
        )
        return senha_valida

    def _encriptar(self, texto: str) -> bytes:
        texto = str.encode(texto)
        return bcrypt.hashpw(texto, self.segredo)

    def _verificar(self, texto_para_verificar: str, texto_original: bytes):
        texto_para_verificar = str.encode(texto_para_verificar)

        if not isinstance(texto_original, bytes):
            texto_original = str.encode(texto_original)

        return bcrypt.checkpw(
            password=texto_para_verificar,
            hashed_password=texto_original,
        )
