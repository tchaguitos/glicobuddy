from uuid import UUID

from libs.dominio import Dominio
from libs.unidade_de_trabalho import UnidadeDeTrabalhoAbstrata

from contextos.glicemias.dominio.entidades import Glicemia
from contextos.glicemias.dominio.comandos import (
    CriarGlicemia,
    EditarGlicemia,
    RemoverGlicemia,
)


def criar_glicemia(comando: CriarGlicemia, uow: UnidadeDeTrabalhoAbstrata) -> Glicemia:
    with uow(Dominio.glicemias):
        nova_glicemia = Glicemia.criar(
            valor=comando.valor,
            tipo=comando.tipo,
            horario_dosagem=comando.horario_dosagem,
            observacoes=comando.observacoes,
            criado_por=uow.usuario,
        )

        uow.repo_dominio.adicionar(nova_glicemia)
        uow.commit()

    return nova_glicemia


def editar_glicemia(
    comando: EditarGlicemia, uow: UnidadeDeTrabalhoAbstrata
) -> Glicemia:
    with uow(Dominio.glicemias):
        glicemia: Glicemia = uow.repo_consulta.consultar_por_id(id=comando.glicemia_id)

        glicemia_editada = glicemia.editar(
            editado_por=uow.usuario,
            novos_valores=comando.novos_valores,
        )

        uow.repo_dominio.atualizar(glicemia_editada)
        uow.commit()

    return glicemia_editada


def remover_glicemia(comando: RemoverGlicemia, uow: UnidadeDeTrabalhoAbstrata) -> UUID:
    with uow(Dominio.glicemias):
        glicemia = uow.repo_consulta.consultar_por_id(id=comando.glicemia_id)

        uow.repo_dominio.remover(glicemia)
        uow.commit()

    return glicemia.id
