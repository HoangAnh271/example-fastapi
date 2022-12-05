"""add last few columns to real_estates table

Revision ID: a054317791da
Revises: c12f3a533d5e
Create Date: 2022-12-05 16:46:40.122088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a054317791da'
down_revision = 'c12f3a533d5e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('real_estates', sa.Column(
        'price', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('real_estates', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('real_estates', 'price')
    op.drop_column('real_estates', 'created_at')
    pass
