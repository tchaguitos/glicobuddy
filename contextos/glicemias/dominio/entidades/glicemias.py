from datetime import datetime
from dataclasses import dataclass


@dataclass
class Glicemia:
    valor: int
    jejum: bool
    data: datetime
    observacoes: str
