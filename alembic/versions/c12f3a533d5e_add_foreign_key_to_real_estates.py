"""add foreign-key to real_estates

Revision ID: c12f3a533d5e
Revises: 7081859a1223
Create Date: 2022-12-05 16:39:12.556604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c12f3a533d5e'
down_revision = '7081859a1223'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('real_estates', sa.Column(
        'owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('real_estaes_users_fk', source_table="real_estates", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('real_estates_users_fk', table_name="real_estates")
    op.drop_column('real_estates', 'owner_id')
    pass
