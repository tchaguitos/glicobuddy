from typing import Callable, Dict, Type, Union, List

from libs.ddd import Comando, Evento

from contextos.barramento.usuarios import (
    COMANDOS_E_EXECUTORES,
    EVENTOS_E_EXECUTORES,
)

Mensagem = Union[Comando, Evento]


# TODO: como coletar todos os handlers de todos os contextos?
class MessageBus:
    eventos_e_executores: Dict[Type[Evento], List[Callable]] = EVENTOS_E_EXECUTORES
    comandos_e_executores: Dict[Type[Comando], List[Callable]] = COMANDOS_E_EXECUTORES

    mensagens_e_executores: Dict[Type[Mensagem], List[Callable]]

    def __init__(self):
        self.mensagens_e_executores = (
            self.eventos_e_executores + self.comandos_e_executores
        )

    def executar_mensagem(self, mensagem: Mensagem):
        tipo_da_mensagem = type[mensagem]

        for executor in self.mensagens_e_executores[tipo_da_mensagem]:
            executor(mensagem)
