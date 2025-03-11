"""add content column to posts table

Revision ID: 746ffb82edf0
Revises: d30ced832fbc
Create Date: 2025-03-11 12:09:36.866580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '746ffb82edf0'
down_revision: Union[str, None] = 'd30ced832fbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')