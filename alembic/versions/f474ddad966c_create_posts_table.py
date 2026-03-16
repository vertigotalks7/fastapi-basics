"""create posts table?

Revision ID: f474ddad966c
Revises: 
Create Date: 2026-03-15 23:58:02.486628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f474ddad966c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False)
                    # sa.Column('content', sa.String(), nullable=False),
                    # sa.Column('created_at', sa.DateTime(), nullable=False),
                    # sa.Column('updated_at', sa.DateTime(), nullable=False)
                    )
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_table('posts')
    """Downgrade schema."""
    pass
