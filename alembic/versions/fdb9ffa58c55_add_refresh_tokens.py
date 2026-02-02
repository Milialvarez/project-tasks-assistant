"""add refresh tokens

Revision ID: fdb9ffa58c55
Revises: 6e5d9e91f41a
Create Date: 2026-02-02 11:27:40.582548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdb9ffa58c55'
down_revision: Union[str, Sequence[str], None] = '6e5d9e91f41a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
