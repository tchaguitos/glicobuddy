from contextos.glicemias.dominio.entidades import Glicemia
from contextos.glicemias.dominio.comandos import CriarGlicemia, EditarGlicemia


def criar_glicemia(comando: CriarGlicemia):
    glicemia_criada = Glicemia.criar(
        valor=comando.valor,
        horario_dosagem=comando.horario_dosagem,
        observacoes=comando.observacoes,
        primeira_do_dia=comando.primeira_do_dia,
        criado_por=comando.criado_por,
    )

    return glicemia_criada


def editar_glicemia(comando: EditarGlicemia):
    glicemia = comando.glicemia

    glicemia_editada = glicemia.editar(
        editado_por=comando.editado_por,
        novos_valores=comando.novos_valores,
    )

    return glicemia_editada
