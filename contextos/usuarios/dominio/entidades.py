from datetime import date, datetime
from uuid import UUID, uuid4
from typing import Optional

from dataclasses import dataclass, field
from dataclass_type_validator import dataclass_validate


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
class Usuario:
    email: Email
    senha: str
    nome_completo: str
    data_de_nascimento: date
    id: UUID = field(init=False, default_factory=uuid4)
    data_criacao_utc: datetime  # TODO: criar contexto de auditoria?

    @classmethod
    def criar(
        cls,
        email: str,
        senha: str,
        nome_completo: str,
        data_de_nascimento: date,
    ):
        return cls(
            email=email,
            senha=senha,
            nome_completo=nome_completo,
            data_de_nascimento=data_de_nascimento,
            data_criacao_utc=datetime.utcnow(),
        )
