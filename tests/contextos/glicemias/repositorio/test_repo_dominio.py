from datetime import datetime
from freezegun import freeze_time

from contextos.glicemias.dominio.objetos_de_valor import TipoDeGlicemia
from libs.tipos_basicos.identificadores_db import IdUsuario

from contextos.glicemias.dominio.entidades import Glicemia
from contextos.glicemias.repositorio.repo_dominio import RepoDominioGlicemias
from libs.tipos_basicos.numeros import ValorDeGlicemia
from libs.tipos_basicos.texto import Email

from tests.contextos.usuarios.mock import mock_criar_usuario


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_adicionar_glicemia(session, usuario_salvo):
    session.execute("DELETE FROM glicemia")

    repo = RepoDominioGlicemias(session)

    usuario = usuario_salvo

    glicemia = Glicemia.criar(
        tipo=TipoDeGlicemia.jejum,
        valor=ValorDeGlicemia(120),
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="primeira glicemia do dia",
        criado_por=IdUsuario(usuario.id),
    )

    repo.adicionar(glicemia)
    session.commit()

    rows = session.execute("SELECT * FROM glicemia")

    registros = list(rows)

    assert len(registros) == 1
    assert registros[0].id == glicemia.id


@freeze_time(datetime(2021, 8, 27, 16, 20))
def test_repositorio_remover_glicemia(session):
    session.execute("DELETE FROM glicemia")

    repo = RepoDominioGlicemias(session)

    usuario = mock_criar_usuario(
        email=Email("outro.usuario@teste.com"),
        session=session,
        salvar_no_db=True,
    )

    glicemia = Glicemia.criar(
        valor=ValorDeGlicemia(120),
        tipo=TipoDeGlicemia.jejum,
        horario_dosagem=datetime(2021, 8, 27, 8, 15),
        observacoes="primeira glicemia do dia",
        criado_por=IdUsuario(usuario.id),
    )

    repo.adicionar(glicemia)
    session.commit()

    rows = session.execute(f"SELECT * FROM glicemia WHERE criado_por = '{usuario.id}'")

    assert len(list(rows)) == 1

    repo.remover(glicemia)
    session.commit()

    rows = session.execute(f"SELECT * FROM glicemia WHERE criado_por = '{usuario.id}'")

    assert len(list(rows)) == 0
