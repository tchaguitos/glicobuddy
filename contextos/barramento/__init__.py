from libs.barramento import MessageBus
from libs.unidade_de_trabalho import UnidadeDeTrabalhoAbstrata

from contextos.barramento import usuarios
from contextos.barramento import glicemias

CONTEXTOS = [
    usuarios,
    glicemias,
]


def coletar_executores_em_todos_os_contextos():
    """"""

    eventos_e_executores = {}
    comandos_e_executores = {}

    for contexto in CONTEXTOS:
        # coletar comandos
        for classe, executores in getattr(contexto, "COMANDOS_E_EXECUTORES").items():
            if classe in comandos_e_executores:
                raise ValueError(
                    "Cada comando deve estar na lista de comandos e executores apenas uma vez"
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
    uow: UnidadeDeTrabalhoAbstrata,
) -> MessageBus:
    """
    Função responsável por instanciar o Message Bus com todos os comandos e
    eventos de todos os contextos da aplicação
    """

    comandos_e_executores = COMANDOS_E_EXECUTORES
    eventos_e_executores = EVENTOS_E_EXECUTORES

    return MessageBus(
        unidade_de_trabalho=uow,
        eventos_e_executores=eventos_e_executores,
        comandos_e_executores=comandos_e_executores,
    )
