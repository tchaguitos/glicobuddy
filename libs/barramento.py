import logging

from typing import Callable, Dict, Type, Union, List

from libs.ddd import Comando, Evento
from libs.unidade_de_trabalho import AbstractUnitOfWork


logger = logging.getLogger(__name__)

Mensagem = Union[Comando, Evento]

ExecutoresDeEventos = Dict[Type[Evento], List[Callable]]
ExecutoresDeComandos = Dict[Type[Comando], List[Callable]]


class MessageBus:
    """"""

    fila_de_mensagens: List[Mensagem]

    unidade_de_trabalho: AbstractUnitOfWork
    eventos_e_executores: ExecutoresDeEventos
    comandos_e_executores: ExecutoresDeComandos

    def __init__(
        self,
        unidade_de_trabalho: AbstractUnitOfWork,
        eventos_e_executores: ExecutoresDeEventos,
        comandos_e_executores: ExecutoresDeComandos,
    ):
        self.unidade_de_trabalho = unidade_de_trabalho
        self.eventos_e_executores = eventos_e_executores
        self.comandos_e_executores = comandos_e_executores

    def tratar_mensagem(self, mensagem: Mensagem):
        self.fila_de_mensagens = [mensagem]
        self.resultado_do_comando = None

        while self.fila_de_mensagens:
            mensagem = self.fila_de_mensagens.pop(0)

            if isinstance(mensagem, Evento):
                self.executar_evento(mensagem, self.unidade_de_trabalho)

            elif isinstance(mensagem, Comando):
                self.resultado_do_comando = self.executar_comando(
                    mensagem, self.unidade_de_trabalho
                )

            else:
                raise Exception(f"{mensagem} não possui evento ou comando")

        return self.resultado_do_comando

    def executar_comando(
        self,
        comando: Comando,
        uow: AbstractUnitOfWork,
    ):
        """"""

        tipo_do_comando = type(comando)
        executores_do_comando = (
            self.comandos_e_executores.get(tipo_do_comando, None) or []
        )

        for executor in executores_do_comando:
            resultado_do_comando = None

            try:
                logger.debug(
                    "Executando o comando %s utilizando o executor %s",
                    comando.__class__.__name__,
                    executor.__name__,
                )

                resultado_do_comando = executor(comando, uow)
                self.fila_de_mensagens.extend(uow.coletar_novos_eventos())

            except Exception as e:
                logger.exception(
                    "Ocorreu um erro ao executar o comando %s",
                    comando.__class__.__name__,
                )
                logger.exception(e)

            return resultado_do_comando

    def executar_evento(
        self,
        evento: Evento,
        uow: AbstractUnitOfWork,
    ):
        """"""

        tipo_do_evento = type(evento)
        executores_do_evento = self.eventos_e_executores.get(tipo_do_evento, None) or []

        for executor in executores_do_evento:
            try:
                logger.debug(
                    "Executando o evento %s utilizando o executor %s",
                    evento.__class__.__name__,
                    executor.__name__,
                )

                executor(evento, uow)

                self.fila_de_mensagens.extend(uow.coletar_novos_eventos())

            except Exception as e:
                logger.exception(
                    "Ocorreu um erro ao executar o evento %s", evento.__class__.__name__
                )
                logger.exception(e)
