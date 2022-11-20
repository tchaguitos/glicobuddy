from libs.ddd import Comando, Evento

from typing import Dict, Type, List, Callable

from contextos.glicemias.dominio.comandos import (
    CriarGlicemia,
    EditarGlicemia,
    RemoverGlicemia,
)
from contextos.glicemias.servicos.executores import (
    criar_glicemia,
    editar_glicemia,
    remover_glicemia,
)


COMANDOS_E_EXECUTORES: Dict[Type[Comando], List[Callable]] = {
    CriarGlicemia: [criar_glicemia],
    EditarGlicemia: [editar_glicemia],
    RemoverGlicemia: [remover_glicemia],
}

EVENTOS_E_EXECUTORES: Dict[Type[Evento], List[Callable]] = {}
