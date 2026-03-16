"""adding more columns to posts table

Revision ID: 9513a618f1ed
Revises: f474ddad966c
Create Date: 2026-03-16 00:21:04.229326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9513a618f1ed'
down_revision: Union[str, Sequence[str], None] = 'f474ddad966c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    """Downgrade schema."""
    pass
