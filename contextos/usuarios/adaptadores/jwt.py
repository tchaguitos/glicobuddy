import os

from typing import Dict, Any
from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError

from contextos.usuarios.dominio.agregados import Usuario

ALGORITMO = "HS256"
MINUTOS_ATE_EXPIRAR = 24 * 60
SEGREDO = os.environ.get("SEGREDO")


class Token(str):
    def __new__(cls, token: str):
        return super().__new__(cls, token)


class TokenExpirado(Exception):
    pass


class GeradorDeToken:
    """"""

    @classmethod
    def gerar_token(cls, usuario: Usuario) -> Token:
        data_de_expiracao = datetime.utcnow() + timedelta(minutes=MINUTOS_ATE_EXPIRAR)

        dados_do_usuario = {
            "id": str(usuario.id),
            "email": usuario.email,
            "nome_completo": usuario.nome_completo,
            "data_de_nascimento": usuario.data_de_nascimento.strftime("%d/%m/%Y"),
            "exp": data_de_expiracao,
        }

        return Token(jwt.encode(dados_do_usuario, SEGREDO, algorithm=ALGORITMO))

    @classmethod
    def verificar_token(cls, token: Token) -> Dict[str, Any]:
        try:
            return jwt.decode(token, SEGREDO, algorithms=[ALGORITMO])

        except ExpiredSignatureError:
            raise TokenExpirado("O token utilizado expirou. Faça login novamente")
