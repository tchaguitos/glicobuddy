from uuid import uuid4
from datetime import datetime
from freezegun import freeze_time

from contextos.glicemias.dominio.entidades import Auditoria, Glicemia
from contextos.glicemias.dominio.comandos import CriarGlicemia, EditarGlicemia
from contextos.glicemias.servicos.executores import criar_glicemia, editar_glicemia
from contextos.glicemias.dominio.objetos_de_valor import ValoresParaEdicaoDeGlicemia

from contextos.glicemias.repositorio import repo_dominio


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_criar_glicemia(session):
    repo = repo_dominio.SqlAlchemyRepository(session)

    id_usuario = uuid4()
    horario_dosagem = datetime(2021, 8, 27, 10, 15)

    registros_no_banco = repo.consultar_todos()
    assert len(registros_no_banco) == 0

    comando = CriarGlicemia(
        valor=98,
        horario_dosagem=horario_dosagem,
        observacoes="glicose em jejum",
        primeira_do_dia=True,
        criado_por=id_usuario,
    )

    glicemia_criada = criar_glicemia(comando=comando)

    registros_no_banco = repo.consultar_todos()
    assert len(registros_no_banco) == 1
