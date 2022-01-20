"""add all cols to posts table

Revision ID: 41da074130e2
Revises: a213bf437526
Create Date: 2022-01-20 19:23:34.965212

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '41da074130e2'
down_revision = 'a213bf437526'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default="TRUE", nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
