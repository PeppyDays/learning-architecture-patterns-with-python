"""Added index on sku

Revision ID: 8831260306e6
Revises: ad6ba1747c12
Create Date: 2022-12-05 00:46:28.599678

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "8831260306e6"
down_revision = "ad6ba1747c12"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(op.f("ix_batches_sku"), "batches", ["sku"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_batches_sku"), table_name="batches")
