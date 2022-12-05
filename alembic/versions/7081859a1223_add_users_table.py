"""add users table

Revision ID: 7081859a1223
Revises: fe472ee43b37
Create Date: 2022-12-05 16:22:42.375561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7081859a1223'
down_revision = 'fe472ee43b37'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
