"""create real estates table

Revision ID: c6a3ff19d1b5
Revises: 
Create Date: 2022-12-05 16:05:21.869221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6a3ff19d1b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('real_estates', sa.Column('id', sa.Integer(
    ), nullable=False, primary_key=True), sa.Column('name', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('real_estates')
    pass
