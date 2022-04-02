from uuid import UUID, uuid4
from datetime import date, datetime

from libs.ddd import Agregado

from dataclasses import dataclass, field
from dataclass_type_validator import dataclass_validate

from contextos.usuarios.dominio.eventos import EmailAlterado
from contextos.usuarios.dominio.objetos_de_valor import ValoresParaEdicaoDeUsuario


class Email(str):
    class EmailInvalido(Exception):
        pass

    def __init__(self, email):
        self.__verificar_se_email_eh_valido(email=email)

    def __verificar_se_email_eh_valido(self, email: str):
        # TODO: criar "validacao real"
        if "@" not in email:
            raise self.EmailInvalido("Você deve fornecer um e-mail válido")

        if len(email) <= 8:
            raise self.EmailInvalido(
                "O e-mail fornecido não possui caracteres suficientes"
            )

        return None


@dataclass_validate
@dataclass
class Usuario(Agregado):
    email: Email
    senha: str
    nome_completo: str
    data_de_nascimento: date
    id: UUID = field(init=False, default_factory=uuid4)
    data_criacao_utc: datetime

    eventos = []

    class UsuarioInvalido(Exception):
        pass

    @classmethod
    def criar(
        cls,
        email: str,
        senha: str,
        nome_completo: str,
        data_de_nascimento: date,
    ) -> "Usuario":
        return cls(
            email=email,
            senha=senha,
            nome_completo=nome_completo,
            data_de_nascimento=data_de_nascimento,
            data_criacao_utc=datetime.utcnow(),
        )

    def editar(
        self,
        valores_para_edicao: ValoresParaEdicaoDeUsuario,
    ) -> "Usuario":
        self.nome_completo = valores_para_edicao.nome_completo
        self.data_de_nascimento = valores_para_edicao.data_de_nascimento

        return self

    def alterar_email(self, email: Email) -> "Usuario":
        self.email = email
        self.adicionar_evento(evento=EmailAlterado(usuario_id=self.id))

        return self

    def __hash__(self):
        return hash(self.id)
