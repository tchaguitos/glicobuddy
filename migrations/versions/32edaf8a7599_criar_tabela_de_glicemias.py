"""criar_tabela_de_glicemias

Revision ID: 32edaf8a7599
Revises: 7bb2d0bae7da
Create Date: 2022-12-26 19:57:14.472781

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID, ENUM

# revision identifiers, used by Alembic.
revision = "32edaf8a7599"
down_revision = "7bb2d0bae7da"
branch_labels = None
depends_on = None


def upgrade() -> None:
    from contextos.glicemias.dominio.objetos_de_valor import TipoDeGlicemia

    tipo_de_glicemia = ENUM(
        "jejum",
        "casual",
        "pre_prandial",
        "pos_prandial",
        name="tipo_de_glicemia",
        schema="public",
        create_type=False,
    )
    tipo_de_glicemia.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "glicemia",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, unique=True),
        sa.Column("valor", sa.Integer(), nullable=False),
        sa.Column("observacoes", sa.String(255), nullable=True),
        sa.Column(
            "tipo",
            tipo_de_glicemia,
            nullable=False,
            default="jejum",
        ),
        sa.Column("horario_dosagem", sa.DateTime(), nullable=False),
        sa.Column(
            "criado_por",
            UUID(as_uuid=True),
            sa.ForeignKey("usuario.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "data_criacao",
            sa.DateTime(),
            server_default=sa.func.current_timestamp(),
            nullable=False,
        ),
        sa.Column(
            "ultima_vez_editado_por",
            UUID(as_uuid=True),
            sa.ForeignKey("usuario.id", ondelete="CASCADE"),
        ),
        sa.Column("data_ultima_edicao", sa.DateTime()),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        index_name="idx_glicemia_criado_por",
        table_name="glicemia",
        columns=["criado_por"],
    )


def downgrade() -> None:
    op.drop_index(
        index_name="idx_glicemia_criado_por",
        table_name="glicemia",
    )
    op.drop_table("glicemia")
    op.execute("DROP TYPE tipo_de_glicemia")
