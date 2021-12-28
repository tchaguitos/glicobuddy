from contextos.glicemias.dominio.entidades import Glicemia
from contextos.glicemias.dominio.comandos import CriarGlicemia, EditarGlicemia

from config import DEFAULT_SESSION_FACTORY
from contextos.glicemias.repositorio import repo_dominio

def criar_glicemia(comando: CriarGlicemia):
    session = DEFAULT_SESSION_FACTORY()
    repo = repo_dominio.SqlAlchemyRepository(session)

    glicemia_criada = Glicemia.criar(
        valor=comando.valor,
        horario_dosagem=comando.horario_dosagem,
        observacoes=comando.observacoes,
        primeira_do_dia=comando.primeira_do_dia,
        criado_por=comando.criado_por,
    )

    repo.adicionar(glicemia_criada)
    session.commit()

    return glicemia_criada


def editar_glicemia(comando: EditarGlicemia):
    session = DEFAULT_SESSION_FACTORY()
    repo = repo_dominio.SqlAlchemyRepository(session)

    glicemia = comando.glicemia

    glicemia_editada = glicemia.editar(
        editado_por=comando.editado_por,
        novos_valores=comando.novos_valores,
    )

    repo.adicionar(glicemia_editada)
    session.commit()

    return glicemia_editada
