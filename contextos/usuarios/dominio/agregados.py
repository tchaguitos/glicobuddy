from datetime import date, datetime

from libs.ddd import Agregado

from dataclasses import dataclass, field
from dataclass_type_validator import dataclass_validate

from libs.tipos_basicos.texto import Nome, Email, Senha
from libs.tipos_basicos.identificadores_db import IdUsuario

from contextos.usuarios.dominio.eventos import EmailAlterado
from contextos.usuarios.dominio.objetos_de_valor import ValoresParaEdicaoDeUsuario


@dataclass_validate
@dataclass
class Usuario(Agregado):
    email: Email
    senha: Senha
    nome_completo: Nome
    data_de_nascimento: date
    id: IdUsuario = field(init=False, default_factory=IdUsuario)
    data_criacao_utc: datetime  # TODO: criar contexto de auditoria?

    eventos = []

    class UsuarioInvalido(Exception):
        pass

    @classmethod
    def criar(
        cls,
        email: Email,
        senha: Senha,
        nome_completo: Nome,
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

        self.adicionar_evento(
            evento=EmailAlterado(
                usuario_id=self.id,
                novo_email=email,
            ),
        )

        return self

    def __hash__(self):
        return hash(self.id)
