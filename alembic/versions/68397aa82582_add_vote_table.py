"""Add Vote Table

Revision ID: 68397aa82582
Revises: 584896593f24
Create Date: 2022-12-22 16:41:25.852231

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '68397aa82582'
down_revision = '584896593f24'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('posts',
                    'id',
                    sa.PrimaryKeyConstraint('id'))
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'],
                                            ['posts.id'],
                                            ondelete='CASCADE',
                                            onupdate='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'],
                                            ['users.id'],
                                            ondelete='CASCADE',
                                            onupdate='CASCADE'))


def downgrade() -> None:
    op.drop_table('votes')
