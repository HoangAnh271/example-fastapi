"""add description column to real_estates table

Revision ID: fe472ee43b37
Revises: c6a3ff19d1b5
Create Date: 2022-12-05 16:16:13.365518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe472ee43b37'
down_revision = 'c6a3ff19d1b5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('real_estates', sa.Column(
        'description', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('real_estates', 'description')
    pass
