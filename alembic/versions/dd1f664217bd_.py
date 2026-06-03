"""empty message

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
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
