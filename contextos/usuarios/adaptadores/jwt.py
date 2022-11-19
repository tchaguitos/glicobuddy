import jwt

from typing import Dict, Any

from contextos.usuarios.dominio.entidades import Usuario

ALGORITMO = "HS256"
MINUTOS_ATE_EXPIRAR = 24 * 60
# TODO: configurar variaveis de ambiente
# TODO: ajustar expiracao de tokens
SEGREDO = "73f8a6d421cffdd587c4c8489124760b4ff6b23bf45017d1de417db63533439b"


class Token(str):
    def __new__(cls, token: str):
        return super().__new__(cls, token)


class GeradorDeToken:
    """"""

    @classmethod
    def gerar_token(self, usuario: Usuario) -> Token:
        dados_do_usuario = {
            "id": str(usuario.id),
            "email": usuario.email,
            "nome_completo": usuario.nome_completo,
            "data_de_nascimento": usuario.data_de_nascimento.strftime("%d/%m/%Y"),
        }

        return Token(jwt.encode(dados_do_usuario, SEGREDO, algorithm=ALGORITMO))

    @classmethod
    def verificar_token(self, token: Token) -> Dict[str, Any]:
        return jwt.decode(token, SEGREDO, algorithms=[ALGORITMO])
