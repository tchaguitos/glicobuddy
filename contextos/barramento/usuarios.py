from libs.ddd import Comando, Evento

from typing import Dict, Type, List, Callable

from contextos.usuarios.dominio.comandos import (
    CriarUsuario,
    EditarUsuario,
    AutenticarUsuario,
    AlterarEmailDoUsuario,
)
from contextos.usuarios.servicos.executores import (
    criar_usuario,
    editar_usuario,
    autenticar_usuario,
    alterar_email_do_usuario,
)

from contextos.usuarios.dominio.eventos import UsuarioCriado, EmailAlterado
from contextos.usuarios.servicos.executores import enviar_email_de_confirmacao


COMANDOS_E_EXECUTORES: Dict[Type[Comando], List[Callable]] = {
    CriarUsuario: [criar_usuario],
    EditarUsuario: [editar_usuario],
    AutenticarUsuario: [autenticar_usuario],
    AlterarEmailDoUsuario: [alterar_email_do_usuario],
}

EVENTOS_E_EXECUTORES: Dict[Type[Evento], List[Callable]] = {
    UsuarioCriado: [enviar_email_de_confirmacao],
    EmailAlterado: [enviar_email_de_confirmacao],
}
