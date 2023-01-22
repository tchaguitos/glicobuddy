"""criar_tabela_de_glicemias

Revision ID: 32edaf8a7599
Revises: 7bb2d0bae7da
Create Date: 2022-12-26 19:57:14.472781

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = "32edaf8a7599"
down_revision = "7bb2d0bae7da"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "glicemia",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, unique=True),
        sa.Column("valor", sa.Integer()),
        sa.Column("observacoes", sa.String(255)),
        sa.Column("primeira_do_dia", sa.Boolean()),
        sa.Column("horario_dosagem", sa.DateTime()),
        sa.Column("criado_por", sa.ForeignKey("usuario.id", ondelete="CASCADE")),
        sa.Column(
            "data_criacao", sa.DateTime(), server_default=sa.func.current_timestamp()
        ),
        sa.Column(
            "ultima_vez_editado_por", sa.ForeignKey("usuario.id", ondelete="CASCADE")
        ),
        sa.Column("data_ultima_edicao", sa.DateTime()),
        sa.Column("ativo", sa.Boolean(), default=True),
        sa.Column("deletado", sa.Boolean(), default=False),

        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(("criado_por",), ["usuario.id"]),
        sa.ForeignKeyConstraint(("ultima_vez_editado_por",), ["usuario.id"]),
    )

    op.create_index(
        index_name="idx_glicemia_criado_por",
        table_name="glicemia",
        columns=["criado_por"],
    )


def downgrade() -> None:
    op.drop_table("glicemia")
