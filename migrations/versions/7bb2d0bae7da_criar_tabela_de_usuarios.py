"""criar_tabela_de_usuarios

Revision ID: 7bb2d0bae7da
Revises: 
Create Date: 2022-12-26 18:58:22.889879

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID

revision = "7bb2d0bae7da"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "usuario",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, unique=True),
        sa.Column("email", sa.String(155), unique=True, nullable=False),
        sa.Column("senha", sa.String(255), nullable=False),
        sa.Column("nome_completo", sa.String(255), nullable=False),
        sa.Column("data_de_nascimento", sa.Date(), nullable=False),
        sa.Column(
            "data_criacao_utc",
            sa.DateTime(),
            server_default=sa.func.current_timestamp(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_unique_constraint(
        columns=["email"],
        table_name="usuario",
        constraint_name="constraint_usuario_email",
    )


def downgrade() -> None:
    op.drop_constraint(
        type_="unique",
        table_name="usuario",
        constraint_name="constraint_usuario_email",
    )
    op.drop_table("usuario")
