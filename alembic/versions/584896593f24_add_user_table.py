"""Add User Table

Revision ID: 584896593f24
Revises: 21cfa6afd90b
Create Date: 2022-12-22 16:36:47.664995

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '584896593f24'
down_revision = '21cfa6afd90b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',
                              sa.Integer(),
                              nullable=False),
                    sa.Column('name',
                              sa.String(length=64),
                              nullable=False),
                    sa.Column('email',
                              sa.String(),
                              nullable=False),
                    sa.Column('password',
                              sa.String(),
                              nullable=False),
                    sa.Column('created_at',
                              sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table('users')

