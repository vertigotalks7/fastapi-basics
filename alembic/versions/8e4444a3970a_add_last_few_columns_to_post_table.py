"""add last few columns to post table

Revision ID: 8e4444a3970a
Revises: 1bf1b982767b
Create Date: 2026-06-03 11:48:29.573150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e4444a3970a'
down_revision: Union[str, Sequence[str], None] = '1bf1b982767b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()'))) 
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at') 
    pass
