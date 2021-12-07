from datetime import datetime
from dataclasses import dataclass


@dataclass
class Glicemia:
    valor: int
    jejum: bool
    data: datetime
    observacoes: str

    @classmethod
    def criar_nova(
        cls,
        valor: int,
        jejum: bool,
        data: datetime,
        observacoes: str,
    ):
        return cls(
            valor=valor,
            jejum=jejum,
            data=data,
            observacoes=observacoes,
        )
