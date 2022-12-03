"""Initialize Batch entity

Revision ID: ad6ba1747c12
Revises:
Create Date: 2022-12-04 02:19:16.547463

"""
from alembic import op
import sqlalchemy as sa


revision = "ad6ba1747c12"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "batches",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("batch_id", sa.String(length=50), nullable=False),
        sa.Column("sku", sa.String(length=50), nullable=False),
        sa.Column("total_quantity", sa.SmallInteger(), nullable=False),
        sa.Column("eta", sa.Date(), nullable=True),
        sa.Column("allocated_order_lines", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("batch_id"),
    )


def downgrade() -> None:
    op.drop_table("batches")
