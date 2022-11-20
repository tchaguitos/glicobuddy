from libs.barramento import MessageBus
from libs.unidade_de_trabalho import AbstractUnitOfWork, SqlAlchemyUnitOfWork

from contextos.barramento import usuarios


CONTEXTOS = [usuarios]


def coletar_executores_em_todos_os_contextos():
    """"""

    eventos_e_executores = {}
    comandos_e_executores = {}

    for contexto in CONTEXTOS:
        # coletar comandos
        for classe, executores in getattr(contexto, "COMANDOS_E_EXECUTORES").items():
            if classe in comandos_e_executores:
                raise ValueError(
                    "Deve existir apenas um comando na lista de comandos e executores"
                )

            comandos_e_executores[classe] = executores

        # coletar eventos
        for classe, executores in getattr(contexto, "EVENTOS_E_EXECUTORES").items():
            eventos_e_executores[classe] = eventos_e_executores.get(classe, [])
            eventos_e_executores[classe] += executores

    return comandos_e_executores, eventos_e_executores


(
    COMANDOS_E_EXECUTORES,
    EVENTOS_E_EXECUTORES,
) = coletar_executores_em_todos_os_contextos()


def bootstrap(
    uow: AbstractUnitOfWork,
) -> MessageBus:
    """"""

    if uow is None:
        uow = SqlAlchemyUnitOfWork()

    comandos_e_executores = COMANDOS_E_EXECUTORES
    eventos_e_executores = EVENTOS_E_EXECUTORES

    return MessageBus(
        unidade_de_trabalho=uow,
        eventos_e_executores=eventos_e_executores,
        comandos_e_executores=comandos_e_executores,
    )
