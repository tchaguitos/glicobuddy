from libs.ddd import Comando, Evento

from typing import Dict, Type, List, Callable

from contextos.usuarios.dominio.comandos import CriarUsuario
from contextos.usuarios.servicos.executores import criar_usuario

from contextos.usuarios.dominio.eventos import UsuarioCriado, EmailAlterado
from contextos.usuarios.servicos.executores import enviar_email_de_confirmacao


COMANDOS_E_EXECUTORES: Dict[Type[Comando], List[Callable]] = {
    CriarUsuario: [criar_usuario],
}

EVENTOS_E_EXECUTORES: Dict[Type[Evento], List[Callable]] = {
    UsuarioCriado: [enviar_email_de_confirmacao],
    EmailAlterado: [enviar_email_de_confirmacao],
}
