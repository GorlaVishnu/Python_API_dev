"""add last few columns to posts table

Revision ID: 0261f5aa0777
Revises: 4ccd81919d05
Create Date: 2025-03-11 13:18:46.201816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0261f5aa0777'
down_revision: Union[str, None] = '4ccd81919d05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    
