"""create posts table

Revision ID: d30ced832fbc
Revises: 80ffe6605267
Create Date: 2025-03-11 11:48:11.291145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd30ced832fbc'
down_revision: Union[str, None] = '80ffe6605267'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass

def downgrade() -> None:
    """Downgrade schema."""
    pass