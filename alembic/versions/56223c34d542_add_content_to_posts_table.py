"""add content to posts table

Revision ID: 56223c34d542
Revises: 41c84bd63345
Create Date: 2022-01-20 18:54:28.039067

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '56223c34d542'
down_revision = '41c84bd63345'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
