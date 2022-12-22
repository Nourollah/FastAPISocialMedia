"""First Level of Schemas

Revision ID: 21cfa6afd90b
Revises: 
Create Date: 2022-12-22 14:56:23.771340

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '21cfa6afd90b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.INTEGER(),
                              autoincrement=True,
                              nullable=False),
                    sa.Column('title',
                              sa.VARCHAR(),
                              autoincrement=False,
                              nullable=False),
                    sa.Column('content',
                              sa.VARCHAR(),
                              autoincrement=False,
                              nullable=False),
                    sa.Column('published',
                              sa.BOOLEAN(),
                              server_default=sa.text('true'),
                              autoincrement=False,
                              nullable=False),
                    sa.Column('created_at',
                              postgresql.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),
                              autoincrement=False,
                              nullable=False),
                    sa.PrimaryKeyConstraint('id', name='posts_pkey'),
                    postgresql_ignore_search_path=False)
    op.create_index('ix_posts_id', 'posts', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_posts_id', table_name='posts')
    op.drop_table('posts')
