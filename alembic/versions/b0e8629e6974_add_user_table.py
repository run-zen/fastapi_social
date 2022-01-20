"""add user table

Revision ID: b0e8629e6974
Revises: 56223c34d542
Create Date: 2022-01-20 18:59:20.250970

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b0e8629e6974'
down_revision = '56223c34d542'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
