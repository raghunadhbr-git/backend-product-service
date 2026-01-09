"""orders flow v1

Revision ID: b47eac32f068
Revises: 3b7de2e4aa7e
Create Date: 2026-01-08
"""

from alembic import op
import sqlalchemy as sa

revision = "b47eac32f068"
down_revision = "3b7de2e4aa7e"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("products") as batch_op:
        batch_op.add_column(
            sa.Column(
                "stock",
                sa.Integer(),
                nullable=False,
                server_default="0"
            )
        )


def downgrade():
    with op.batch_alter_table("products") as batch_op:
        batch_op.drop_column("stock")
