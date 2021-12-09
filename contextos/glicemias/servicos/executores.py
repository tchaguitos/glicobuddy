from contextos.glicemias.dominio.entidades import Glicemia
from contextos.glicemias.dominio.comandos.glicemias import CriarGlicemia


def criar_glicemia(comando: CriarGlicemia):
    glicemia_criada = Glicemia.criar(
        valor=comando.valor,
        horario_dosagem=comando.horario_dosagem,
        observacoes=comando.observacoes,
        primeira_do_dia=comando.primeira_do_dia,
        criado_por=comando.criado_por,
    )

    return glicemia_criada
