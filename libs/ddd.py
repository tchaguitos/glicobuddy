from typing import List


class Comando:
    pass


class Evento:
    pass


class Agregado:
    eventos: List[Evento]

    def adicionar_evento(self, evento: Evento):
        self.eventos.append(evento)
