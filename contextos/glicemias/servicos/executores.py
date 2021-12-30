from contextos.glicemias.dominio.entidades import Glicemia
from contextos.glicemias.dominio.comandos import CriarGlicemia, EditarGlicemia, RemoverGlicemia

from contextos.glicemias.repositorio.repo_dominio import SqlAlchemyRepository

def criar_glicemia(comando: CriarGlicemia, repo: SqlAlchemyRepository, session):
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


def editar_glicemia(comando: EditarGlicemia, repo: SqlAlchemyRepository, session):
    glicemia = repo.consultar_por_id(id=comando.glicemia_id)

    glicemia_editada = glicemia.editar(
        editado_por=comando.editado_por,
        novos_valores=comando.novos_valores,
    )

    repo.adicionar(glicemia_editada)
    session.commit()

    return glicemia_editada


def remover_glicemia(comando: RemoverGlicemia, repo: SqlAlchemyRepository, session):
    glicemia = repo.consultar_por_id(id=comando.glicemia_id)

    repo.remover(glicemia)
    session.commit()

    return glicemia.id
