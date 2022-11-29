from typing import Optional


class ExceptionBase(Exception):
    titulo: str
    descricao: Optional[str]

    def __init__(self, titulo: str, descricao: Optional[str] = None):
        self.titulo = titulo
        self.descricao = descricao

    def __str__(self):
        return self.titulo


class UsuarioNaoEncontrado(ExceptionBase):
    pass


class ErroNaAutenticacao(ExceptionBase):
    pass
