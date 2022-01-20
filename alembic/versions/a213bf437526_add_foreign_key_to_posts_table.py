"""add foreign key to posts table

Revision ID: a213bf437526
Revises: b0e8629e6974
Create Date: 2022-01-20 19:13:40.199763

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a213bf437526'
down_revision = 'b0e8629e6974'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users',
                          local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')

    pass


def downgrade():
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
