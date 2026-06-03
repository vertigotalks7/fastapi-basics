""" add user table

Revision ID: dd1f664217bd
Revises: 9513a618f1ed
Create Date: 2026-03-19 10:13:04.089332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd1f664217bd'
down_revision: Union[str, Sequence[str], None] = '9513a618f1ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )  
    pass


def downgrade() -> None:
    op.drop_table('users')
    """Downgrade schema."""
    pass
